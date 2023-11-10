from flaskprojectsecond.App import app, models, USERS, POSTS, REACTIONS
import json
from flask import Response, request
from http import HTTPStatus


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    author_id = data["author_id"]
    text = data["text"]
    if not models.User.is_valid_id(author_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    post_id = len(POSTS)
    post = models.Post(post_id, author_id, text)
    POSTS.append(post)
    user = USERS[author_id]
    user.write_post(post)
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        status=HTTPStatus.CREATED,
        mimetype="apllication/json",
    )
    return response

@app.get('/posts/<int:post_id>')
def get_post(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = POSTS[post_id]
    response = Response(
        json.dumps({
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json'
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def add_reactions(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response(
            "Поста с таким номером не существует", status=HTTPStatus.NOT_FOUND
        )
    reaction_id = len(REACTIONS)
    data = request.get_json()
    author_of_reaction = data['user_id']
    reaction_text = data['reaction']
    if not models.Reaction.is_emojy(reaction_text):
        return Response('Такой реакции нет', status=HTTPStatus.BAD_REQUEST)
    reaction = models.Reaction(reaction_id, author_of_reaction, reaction_text)
    REACTIONS.append(reaction)
    reaction.emojize()
    post = POSTS[post_id]
    post.add_reaction(reaction.emojy)
    user = USERS[post.author_id]
    user.get_reactions(1)
    return Response(status=HTTPStatus.OK)
