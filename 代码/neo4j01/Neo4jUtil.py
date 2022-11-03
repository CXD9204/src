#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
from neo4j import GraphDatabase


# from CommUtil import decrypt


class App:

    def __init__(self, uri, user, password):
        self.user = user
        if password:
            self.pwd = password
            self.driver = GraphDatabase.driver(uri, auth=(self.user, self.pwd))
        else:
            self.driver = GraphDatabase.driver(uri)

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    # 新增指标属性
    @staticmethod
    def _write_transaction(tx, cql):
        tx.run(cql)

    def write_transaction(self, cql):
        with self.driver.session() as session:
            session.write_transaction(self._write_transaction, cql)

    @staticmethod
    def _read_transaction(tx, cql):
        result = tx.run(cql)
        values = []
        for record in result:
            values.append(record.values())
        return values

    def read_transaction(self, cql):
        with self.driver.session() as session:
            result = session.read_transaction(self._read_transaction, cql)
        return result

    # 根据ID 获取指标名称和对象类型
    def get_metric_info(self, indexId):
        '''
        :param indexIs: 指标ID
        :return:
        '''
        cql = "match(n:指标) where n.指标ID=%s return n.object_type as object_type,n.指标名称 as metric_name" % (indexId)
        print(cql)
        obj_type = ''
        metric_name = ''
        with self.driver.session() as session:
            result = session.run(cql).data()
        if result[0]:
            metrics = result[0].get('metric_name')
            obj_type = result[0].get('object_type')
            metric_name = metrics
        return obj_type, metric_name

    def acquire_solution(self, conclusion, metric):
        result = dict()
        indexId = metric.get('indexId')
        obj_type, metric_name = self.get_metric_info(indexId)
        # cql = "match (n:运维经验) where n.object_type='%s' and n.`指标项`='%s'  return n.tag,n.故障名称,n.value,n.指标描述,n.解决方案,n.方案来源" % (
        #     obj_type, metric_name)
        cql = "match (n:运维经验) where n.object_type='%s' and n.`指标项`='%s'  return n" % (
            obj_type, metric_name)

        with self.driver.session() as session:
            dataset = session.run(cql).data()[0]
            dataList = dataset.get('n')
            result['indexId'] = indexId
            result['tag'] = dataList['tag']
            result['fault_name'] = dataList['故障名称']
            result['refer'] = dataList['value']
            result['metric_desc'] = dataList['故障描述']
            result['solution'] = dataList['解决方案']
            conclusion.append(result)
            return conclusion

    # 指标分析
    def analysis_metric(self, metricList):
        '''
        :param app  neo4j的实例化对象
        :param metricList:
        :return:
        '''
        conclusion = []
        for metric in metricList:
            indexId = metric.get('indexId')
            value = metric.get('value')
            symbol = metric.get('symbol')
            # 如果标志符号为空,则直接获取运维经验
            if symbol is None:
                self.acquire_solution(conclusion, metric)
                return conclusion
            # 获取对象类型与指标名称
            obj_type, metric_name = self.get_metric_info(indexId)

            '''从neo4j的运维经验中获取故障类型 故障名称以及解决方案   最后转化为字典格式的数据 添加到类表中并返还数据'''
            cql = "match (n:运维经验) where n.object_type='%s' and n.`指标项`='%s' and %s %s n.value return n.tag,n.故障名称,n.value,n.指标描述,n.解决方案" % (
                obj_type, metric_name, value, symbol)
            result = {}
            with self.driver.session() as session:
                result1 = session.run(cql)
                result1 = result1.peek()
                if result1 is None:
                    pass
                    # print("未查询到结果值,请手动执行CQL语句")
                else:
                    dataList = result1.values()
                    result['indexId'] = indexId
                    result['tag'] = dataList[0]
                    result['fault_name'] = dataList[1]
                    result['refer'] = dataList[2]
                    result['metric_desc'] = dataList[3]
                    result['solution'] = dataList[4]
                    conclusion.append(result)
            # except Exception as e:
            # print(str(e))
        return conclusion

    # 多指标判断，获取外部参数值与基线值判断关系
    def relation_symbol(self, metrices):
        '''
        :param metrices:指标参数列表集合，将判断关系添加到指标字典中
        :return: metrices
        '''
        check = list()
        for metric in metrices:
            name = metric.get("metric")
            with self.driver.session() as session:
                cql = f'match (n:运维经验) where n.`指标项`="{name}" return n.故障描述'
                result = session.run(cql)
                result = result.peek()
                if result is None:
                    continue
                else:
                    # 获取neo4j内部基线值的判断关系：>，<
                    desc = result.values()
                    if "大于" in desc or "接近" in desc or "超过" in desc:
                        metric["symbol"] = ">"
                        check.append(metric)
                    elif "小于" in desc or "低于" in desc or "不超过" in desc:
                        metric["symbol"] = "<"
                        check.append(metric)
                    else:
                        pass
        return check

    # 多指标分析 联合查询分析
    def muti_metrices_analysis(self, metrices):
        '''
        :param metrices: 多指标列表字典，[{},{},{}]
        :return:
        '''
        metrice_list = self.relation_symbol(metrices)
        cql = ""
        for metric in metrice_list:
            cql += f'\n match(n:运维经验)where {metric.get("value")} {metric.get("symbol")} n.refer return n.tag,n.solution\n union'
        # 去除尾部的union字符串以及头部的换行:\n
        CQL = cql.rstrip("union").lstrip("\n")
        with self.driver.session() as session:
            result = session.run(CQL)
            result = result.peek()
            if result is None:
                print("未查询到结果值,请手动执行CQL语句")
            else:
                result_value_list = result.value()
                print(result_value_list)

    # 多指标分析
    def muti_metrices_analysis2(self, metrices):
        '''
        :param metrices: 多指标列表字典，[{},{},{}]
        :return:
        '''
        metric = self.relation_symbol(metrices)
        cql = f'match(n:运维经验)where n.`指标项`={metric["name"]} and {metric.get("value")} {metric.get("symbol")} n.value ' \
              f'return n.tag,n.指标项,n.value,n.故障描述,n.方案来源,n.解决方案'
        with self.driver.session() as session:
            result = session.run(cql)
            result = result.data()['n']
            if result is None:
                result1 = session.run(
                    f'match(n:运维经验)where n.`指标项`={metric["name"]} and {metric.get("value")} {metric.get("symbol")} n.value ' \
                    f'return n.tag,n.指标项,n.valle,n.故障描述,n.方案来源,n.解决方案').data()['n']
                msg = f"阈值:{None},采集值:{None},其他参考项:{None} \n"
            else:
                msg = f"阈值:{result['value']},采集值:{metric['value']},检测指标:{result['指标项']},解决方案:{result['解决方案']},方案来源:{result['方案来源']}"
