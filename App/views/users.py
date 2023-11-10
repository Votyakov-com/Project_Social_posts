from flaskprojectsecond.App import app, models, USERS
import json
from flask import Response, request, url_for
from http import HTTPStatus
import matplotlib.pyplot as plt


@app.post("/users/create")
def creater():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    for user in USERS:
        if user.email == email:
            return Response(
                "Пользователь с такой почтой уже существует",
                status=HTTPStatus.BAD_REQUEST,
            )
    if not models.User.is_valid_email(email):
        return Response("Неправильно введена почта", status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.show_message_of_posts(),
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get('/users/<int:user_id>/posts')
def sort_post(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    posts_of_user = user.posts
    if len(posts_of_user) == 0:
        return Response('У этого пользователя нет постов', status=HTTPStatus.NOT_FOUND)
    type_of_sorting = request.get_json()['sort']
    if type_of_sorting != 'asc' and type_of_sorting != 'desc':
        return Response('Такого вида сортировки не существует', status=HTTPStatus.BAD_REQUEST)
    if type_of_sorting == 'asc':
        result = sorted(posts_of_user)
    else:
        result = sorted(posts_of_user, reverse=True)
    dict_of_posts = dict()
    dict_of_posts['posts'] = []
    for post in result:
        mydict = dict({
            "id": post.id,
            "author_id": post.author_id,
            "text": post.text,
            "reactions": post.reactions,
        })
        dict_of_posts['posts'].append(mydict)
    return Response(
        json.dumps(dict_of_posts),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )


@app.get('/users/leaderboard')
def get_leaderboard():
    type_visualisation = request.get_json()['type']
    if type_visualisation != 'list' and type_visualisation != 'graph':
        return Response('Такой опции не существует', status=HTTPStatus.BAD_REQUEST)
    list_of_users = USERS
    if type_visualisation == 'list':
        type_of_sorting = request.get_json()['sort']
        if type_of_sorting != 'asc' and type_of_sorting != 'desc':
            return Response('Такого вида сортировки не существует', status=HTTPStatus.BAD_REQUEST)
        if type_of_sorting == 'asc':
            result = sorted(list_of_users)
        else:
            result = sorted(list_of_users, reverse=True)
        dict_of_posts = dict()
        dict_of_posts['users'] = []
        for user in result:
            mydict = dict({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "reactions": user.email,
                "total_reactions": user.total_reactions,
            })
            dict_of_posts['users'].append(mydict)
        return Response(
            json.dumps(dict_of_posts),
            status=HTTPStatus.OK,
            mimetype='application/json',
        )
    else:
        fig, ax = plt.subplots()
        user_names = [f'{user.first_name} {user.last_name} ({user.id})' for user in USERS]
        user_total_reactions = [user.total_reactions for user in USERS]
        ax.bar(user_names, user_total_reactions)
        ax.set_ylabel('User total reactions', fontsize=12)
        ax.set_xlabel('User name', fontsize=12)
        ax.set_title('User list by total reactions', fontsize=15)
        plt.savefig(
            'App/static/users_reactions.png')
        return Response(
            f'<img src={url_for("static", filename="users_reactions.png")}>',
            status=HTTPStatus.OK,
            mimetype='text/html',
        )
