# FastAPI Task Manager

这是一个基于 FastAPI 的任务管理系统。

## 快速开始

```bash
pip install -r requirements.txt
uvicorn main:app --reload

从创建项目到推送项目到github全流程
1.创建项目文件夹
2.
# 1. 初始化 git 仓库
git init -b main

# 2. 添加所有文件
git add .

# 3. 提交代码
git commit -m "initial commit: FastAPI Hello World"#更改的内容

3.github上创建一个仓库aaa

4.
# 替换成你的 GitHub 仓库地址
git remote add origin https://github.com/你的用户名/aaa.git

# 推送（第一次需要设置 upstream）
git push -u origin main

5🔁 以后每次推送，只需要这一步：
git add .
git commit -m "你的修改描述"
git push

脚本路由表
GET      /                                        read_root
GET      /docs                                    swagger_ui_html
GET      /docs/oauth2-redirect                    swagger_ui_redirect
POST     /login                                   login
GET      /metrics                                 metrics
GET      /openapi.json                            openapi
GET      /redoc                                   redoc_html
POST     /tasks                                   create_task
GET      /tasks                                   list_tasks
GET      /tasks/admin/{task_id}                   admin_get_task
POST     /tasks/create                            create_task
GET      /tasks/{task_id}                         get_task
POST     /users                                   register_user
