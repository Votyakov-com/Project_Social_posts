from flask import Flask

app = Flask(__name__)
USERS = []

from flaskprojectsecond.App import views_all, views, models
