from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = "AlphaBeta"
app.config['WTF_CSRF_SECRET_KEY'] = "SecretKey"

from app import routes
