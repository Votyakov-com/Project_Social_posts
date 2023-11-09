from flask import Flask

app = Flask(__name__)
USERS = []
POSTS = []
REACTIONS = []

from flaskprojectsecond.App import views_all, views, models
