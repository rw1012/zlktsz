#####装饰器文件
from flask import Flask,url_for,redirect,session
from functools import wraps
#登录限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
       user_id=session.get('user_id')
       if user_id:
           return func(*args,**kwargs)
       else:
           return redirect(url_for('login'))
    return wrapper