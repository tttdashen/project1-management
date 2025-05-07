#day1
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
#day2
#步骤一：定义路径参数接口
@app.get("/users/{user_id}")#/users/{user_id}：路径中带变量
def read_user(user_id:int):#user_id: int：自动转换类型，访问 /users/123 会传入 123#
    return{"user_id":user_id}#FastAPI 会自动帮你处理参数类型，错误类型（如 /users/abc）会返回 422 错误

#步骤二：定义带查询参数的接口
@app.get("/items")
def read_items(skip:int=0,limit:int=10):#可以设置默认值，不传参数也不会报错
    #访问 /items/?skip=5&limit=20.skip 和 limit 是查询参数（URL 中 ? 后面的部分）
    return{"skip":skip,"limit":limit}

@app.get("/books/{book_id}")
def get_book(book_id:int,detail:bool=False):#要求输入的book_id为整数型，输入的datail为布尔型
    return{"book_id":book_id,"detail":detail}
