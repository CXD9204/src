package main

import (
	"fmt"
	"goCode/project03/service"
)

type ViewStu struct {
	Key     string
	Flag    bool
	service *service.ServiceStu
}

//显示菜单选项
func (view *ViewStu) ShowMainMenu() {
	fmt.Println("主菜单")
	for {
		fmt.Println("------选项1\t添加学生信息------")
		fmt.Println("------选项2\t删除学生信息------")
		fmt.Println("------选项3\t更新学生信息------")
		fmt.Println("------选项4\t显示学生信息------")
		fmt.Println("------选项5\t退出学生系统------")
		fmt.Println("------选择:------")
		fmt.Scanln(&view.Key)
		switch view.Key {
		case "1":
			view.AddView()
		case "2":
			view.DelStuView()
		case "3":
			fmt.Println("------序号3\t更新学生信息------")
		case "4":
			view.ShowStuView()
		case "5":
			view.ExieView()
		default:
			fmt.Println("------输入错误,请选择(1-5):------")

		}
		//退出系统,退出当前for循环
		if !view.Flag {
			return
		}

	}

}

//退出系统
func (this *ViewStu) ExieView() {
	fmt.Println("请确认是否要退出?y/n:")
	mark := ""
	for {
		fmt.Scanln(&mark)
		if mark == "y" || mark == "Y" || mark == "N" || mark == "n" {
			break
		}
		fmt.Println("输入错误,请输入y or n")
	}
	//判定是否退出
	if mark == "y" || mark == "Y" {
		fmt.Println("已退出系统")
		this.Flag = false
		return
	}

}

//添加信息
func (view *ViewStu) AddView() {
	view.service.AddService()
}

//根据名称删除学生
func (this *ViewStu) DelStuView() {
	name := ""
	fmt.Println("请输入删除学生姓名:")
	fmt.Scanln(&name)
	flag := this.service.DelStuService(name)
	if flag {
		fmt.Println("删除成功")
	} else {
		fmt.Println("取消删除")
	}

}

//更新信息
func (this *ViewStu) UpdateStuView() {
	name := ""
	fmt.Println("输入修改的学生姓名:")
	fmt.Scanln(&name)
	this.service.UpdateStuService(name)

}

//显示所有信息
func (view *ViewStu) ShowStuView() {
	view.service.ShowStuList()
}

func main() {
	view := ViewStu{
		Key:  "",
		Flag: true,
	}
	view.service = service.FactoryService()
	view.ShowMainMenu()

	// service.FactoryService()

}
