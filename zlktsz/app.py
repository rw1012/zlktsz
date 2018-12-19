from flask import Flask,render_template,request,url_for,redirect,session
import config
from models import User,Question,Answer
from exts import db
from decorator import login_required
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
#定义首页路由
@app.route('/')
def index():
    content={
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**content)
#定义登录页面路由
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        #在已注册信息表中查找是否有此user对比判断，有的话就可登录
        user=User.query.filter(User.telephone==telephone,User.password==password).first()
        if user:
        #登录后保存用户的信息，使用session设置31天不需要登录
            session['user_id']=user.id
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return '手机或密码错误，请查证后登录'
#定义注册页面路由
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
       telephone=request.form.get('telephone')
       username=request.form.get('username')
       password1=request.form.get('password1')
       password2=request.form.get('password2')

        #手机号码验证，如果被注册啦，就不能注册了
       user=User.query.filter(User.telephone==telephone).first()
       if user:
           return '该手机号已被注册，请更换手机号或前往登陆'
       else:
            #如果手机号未被注册，此时应判断输入的两次密码是否一致
           if password1!=password2:
               return '两次密码输入不一致,请重新输入'
           else:
               user=User(telephone=telephone,username=username,password=password1)
               db.session.add(user)
               db.session.commit()
           #如果注册成功，跳转到登录页面
               return redirect(url_for('login'))

#注销用户信息，退出登录，删除session信息即可
@app.route('/logout/')
def logout():
    session.pop('user_id')
    #del session['user_id']
    #session.clear
    return redirect(url_for('login'))
#定义发布问答页面路由
@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        question=Question(title=title,content=content)
        user_id=session.get('user_id')
        user=User.query.filter(User.id==user_id).first()
        #print(user.id )
        question.author=user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
#问题详情页面
@app.route('/detail/<question_id>/',methods=['GET','POST'])
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()

    return render_template('detail.html',question=question_model)
#添加评论,加上登录装饰器
@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content=request.form.get('answer_content')
    question_id=request.form.get('question_id')

    answer=Answer(content=content)
    user_id=session['user_id']
    user=User.query.filter(User.id==user_id).first()
    answer.author=user
    question=Question.query.filter(Question.id==question_id).first()
    answer.question=question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))
#定义上下文处理函数，一定得return一个字典形式，全局均可使用
@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
