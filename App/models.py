import re
from abc import ABC, abstractmethod
from flaskprojectsecond.App import USERS, POSTS
import emoji


class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0, posts=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = [] if posts == None else posts

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def is_valid_id(user_id):
        return isinstance(user_id, int) and 0 <= user_id < len(USERS)

    def write_post(self, post):
        self.posts.append(post)

    def show_message_of_posts(self):
        result = []
        for post in self.posts:
            result.append(post.text)
        return result

    def get_reactions(self, number):
        self.total_reactions += number

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions

    def __gt__(self, other):
        return self.total_reactions > other.total_reactions

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
        if emoji.is_emoji(reaction):
            self.reactions.append(reaction)

    def __lt__(self, other):
        return len(self.reactions) < len(other.reactions)

    def __gt__(self, other):
        return len(self.reactions) > len(other.reactions)


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



