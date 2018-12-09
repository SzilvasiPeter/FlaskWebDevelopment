import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '63483d93977177f94771262462df57fb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.index'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

# Import Blueprint
from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main

# Register Blueprint
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

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