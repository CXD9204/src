package main

//https://www.bookstack.cn/read/beego-2.0-zh/quickstart-router.md
import (
	"fmt"

	"github.com/beego/beego/v2/server/web"
)

type MainController struct {
	web.Controller
}

//重写get请求
func (this *MainController) Get() {
	this.Ctx.WriteString("hello world")
}

//重写post请求
func (this *MainController) Post() {
	this.Ctx.WriteString("这是一个post请求")
}
func main() {
	web.Router("/ping/", &MainController{})
	web.Router("/hi/", &MainController{})
	fmt.Println("hello,world")
	//在conf目录下的app.conf修改监听端口和项目名称
	web.Run()

}
