import re
from abc import ABC, abstractmethod

class User:
    def __init__(self, id, first_name, last_name, email, total_reations=0, posts=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reations
        self.posts = [] if posts == None else posts
        self.history = []

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)