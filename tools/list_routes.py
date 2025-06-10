#tools/list_routers.py
from importlib import import_module#动态导入模块 import app.main
from fastapi import FastAPI

def get_app() -> FastAPI:
    return import_module("app.main").app

def list_routes(app:FastAPI):
    rows=[]
    for route in app.router.routes:
        methods = ",".join(sorted(route.methods - {"HEAD","OPTIONS"}))
        path = route.path
        name = route.name
        rows.append((methods,path,name))
    return sorted(rows,key=lambda x:x[1])
    
if __name__ == "__main__":
    app=get_app()
    routes = list_routes(app)
    with open("tools/routes.txt","w",encoding="utf-8") as f:
        for method,path,name in routes:
            f.write(f"{method:8} {path:40} {name}\n")
        print(f"✓ 共列出 {len(routes)} 条路由，结果保存在 tools/routes.txt")  
