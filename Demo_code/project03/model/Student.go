package model

import "fmt"

type Student struct {
	Name    string
	Age     int
	Gender  string
	Address string
	Email   string
	Note    string
}

//工厂函数 返回一个student实例
func Factory(name string, age int, gender string, address string, email string, note string) Student {
	return Student{
		Name:    name,
		Age:     age,
		Gender:  gender,
		Address: address,
		Email:   email,
		Note:    note,
	}
}

//打印学生信息
func (stu Student) GetStuInfo() string {
	info := fmt.Sprintf("%v\t%v\t%v\t%v\t%v\t%v\t", stu.Name, stu.Age, stu.Gender, stu.Address, stu.Email, stu.Note)
	return info
}
