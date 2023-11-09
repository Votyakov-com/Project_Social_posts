import re
from abc import ABC, abstractmethod
from flaskprojectsecond.App import USERS, POSTS
import emoji


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

    @staticmethod
    def is_valid_id(user_id):
        return isinstance(user_id, int) and 0 <= user_id < len(USERS)


class Post:
    def __init__(self, id, author_id, text, reactions=None):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = [] if reactions == None else reactions

    @staticmethod
    def is_valid_id(post_id):
        return isinstance(post_id, int) and 0 <= post_id < len(POSTS)

    def add_reaction(self, reaction):
        if isinstance(reaction, str):
            self.reactions.append(reaction)


class Reaction:
    def __init__(self, id, author_of_reaction_id, text):
        self.id = id
        self.author_of_reaction_id = author_of_reaction_id
        self.text = text
        self.emojy = None

    @staticmethod
    def is_emojy(emojy: str):
        return emoji.is_emoji(emoji.emojize(f':{emojy}:'))

    def emojize(self):
        if self.is_emojy(self.text):
            result = emoji.emojize(f':{self.text}:')
            self.emojy = result



