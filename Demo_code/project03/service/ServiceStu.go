package service

import (
	"fmt"
	"goCode/project03/model"
)

type ServiceStu struct {
	num int
	stu []model.Student
}

//初始化一个ServiceStu

//服务层工厂函数
func FactoryService() *ServiceStu {
	student := &ServiceStu{}
	student.num++
	Student := model.Factory("tom", 20, "m", "beijing", "tomcat@qq.com", "nothing")
	student.stu = append(student.stu, Student)
	return student

}

//打印所有学生名单
func (service *ServiceStu) ShowStuList() {
	fmt.Println("--------学生信息如下--------")
	fmt.Println("Name\tAge\tGender\tAddress\tEmail\tNote\t")
	for i := 0; i < len(service.stu); i++ {
		fmt.Println(service.stu[i].GetStuInfo())

	}

}

//添加
func (this *ServiceStu) AddService() {
	name := ""
	age := 0
	gender := ""
	address := ""
	email := ""
	note := ""
	fmt.Println("输入姓名:")
	fmt.Scanln(&name)
	fmt.Println("输入年龄:")
	fmt.Scanln(&age)
	fmt.Println("输入性别:")
	fmt.Scanln(&gender)
	fmt.Println("输入地址:")
	fmt.Scanln(&address)
	fmt.Println("输入邮箱:")
	fmt.Scanln(&email)
	fmt.Println("备注:")
	fmt.Scanln(&note)
	stu := model.Factory(name, age, gender, address, email, note)
	this.stu = append(this.stu, stu)

}

//根据学生名称找到对应的下标
func (this *ServiceStu) FindById(name string) int {
	index := -1
	for i, stu := range this.stu {
		if stu.Name == name {
			index = i
		}
	}
	return index
}

//根据名称删除学生
func (this *ServiceStu) DelStuService(name string) bool {
	Stus := this.stu
	flag := false
	choice := ""
	for index, stu := range Stus {
		if stu.Name == name {
			fmt.Printf("确认要删除%v?请输入y/n \n", index)
			fmt.Scanln(&choice)
		}
		//删除切片
		if choice == "y" {
			this.stu = append(this.stu[:index], this.stu[(index+1):]...)
			flag = true
		} else {
			flag = false
		}
	}
	return flag
}

//更新信息
func (this *ServiceStu) UpdateStuService(name string) {
	for _, stu := range this.stu {
		if stu.Name == name {

		} else {
			fmt.Println("未找到指定目标")
		}
	}

}
