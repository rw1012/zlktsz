import os
SECRET_KEY=os.urandom(24)
HOSTNAME='localhost'
DATEBASE='zlktsz'
USERNAME='root'
PASSWORD=''
DB_URI='mysql+pymysql://{}:{}@{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,DATEBASE)
SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
SQLALCHEMY_TRACK_MODIFICATIONS=False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False