from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456Farid25.@localhost/shoe_makers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.secret_key = 'secret key'

# Init db
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
