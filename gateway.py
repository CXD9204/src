from wsgiref.simple_server import make_server


def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b'<h1>HELLO,WORLD</h1>']

#中间件
def middleware(environ, start_response):
    environ.update({"hello": "world"})
    response = application(environ, start_response)
    print(environ.get('hello'))
    return response


wsgi_server = make_server("localhost", 8008, middleware)
print("http://localhost:8008/")
wsgi_server.serve_forever()  # 直运行
