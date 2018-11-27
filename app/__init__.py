from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '63483d93977177f94771262462df57fb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'info'

from app import views

# Load data from json

# from app.models import Post 
# import json

# with open('post.json') as f:
# 	data = f.read()
# 	jsondata = json.loads(data)
# 	for item in jsondata:
# 		post = Post(title=item['title'], content=item['content'], user_id=int(item['user_id']))
# 		db.session.add(post)
# 	db.session.commit()

# Delete table's content

# conn = sqlite3.connect('./site.db')
# cur = conn.cursor()
# sql = "DELETE FROM post"
# cur.execute(sql)
# conn.commit()