from fastapi import FastAPI #调用函数，fastapi是文件名（不含.py），FastAPI是函数名
# 创建 FastAPI 应用实例
app = FastAPI()
@app.get('/hello')#定义一个路径为/hello的get请求接口，当浏览器访问 http://127.0.0.1:8000/hello 时，就会触发绑定的那个函数执行。
def read_hello():
    # 接口返回 JSON 数据
    return {'message':'Hello world'}
'''
示例：欢迎接口
@app.get('/hello')
def say_hello():
    return {'msg':'Hello FastAPI!'}
访问 /hello,返回
{"msg": "Hello FastAPI!"}

示例：获取用户姓名
@app.get('/user/name')
def get_user(name:str):
    return {'username':name}
访问 /user/jack，返回：
{"username": "jack"}
'''