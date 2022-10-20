## 后端 （python+django）
### 版本要求
```
python >= 3.7
django >= 3.0
```
### 安装依赖
```
cd backend/
pip install -r requirements.txt
```
### 数据库设置 
```
找到文件 backend/k8s/settings
找到DATABASES段设置正确的即可
```
### 初始化
```
cd backend/
python manage.py makemigrations
python manage.py migrate
```

### 启动
```
# 进到项目目录 
python manage.py runserver 8000
```

### review
```
# 文件tree
├── README.md
├── app
│   ├── admin.py
│   ├── apps.py
│   ├── json_response.py
│   ├── models.py
│   ├── page.py
│   ├── tests.py
│   ├── view
│   │   ├── api.py
│   │   ├── k8s_ssh.py
│   │   └── login.py
│   └── views.py
├── k8s
│   ├── asgi.py
│   ├── routing.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
```

