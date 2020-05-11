import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import Actors, Movies, set_up_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

# -------------------------------------------------------------#
# CORS Headers
# -------------------------------------------------------------#
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    set_up_db(app)

    @app.route('/')
    def homepage():
        return jsonify({
            'Casting Agency': "Welcome to The Great Casting Agency",
        })

# -------------------------------------------------------------#
# GET controllers
# -------------------------------------------------------------#

    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def get_movies():
        all_movies = Movies.query.all()
        movie_list = []
        for movie in all-movies:
            movie_list.append(movie.format())
        return jsonify({
            'success': True,
            'movies': movie_list,
            'total movies': len(movie_list)
        }),200

    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def actorList():
        all_actors = Actors.query.all()
        actor_list = []
        for actor in all_actors:
            actor_list.append(actor.format())
        return jsonify({
            'success': True,
            'movies': actor_list,
            'total movies': len(actor_list)
        }),200
# -------------------------------------------------------------#
# PATCH controllers
# -------------------------------------------------------------#

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(movie_id):
        body = request.get_json()
        title = data.get('title')
        release_date = data.get('release_date')
        try:
            get_movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if get_movie is None:
                abort(404)
            if title and release_date is None:
                abort(422)
            if title is not None:
                get_movie.title = title
            if release_date is not None:
                get_movie.release_date = release_date
            get_movie.update()
            return jsonify({
                'success': True,
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def any_actor(actor_id):
        body = request.get_json()
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        try:
            get_actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if get_actor is None:
                abort(404)
            if name and age and gender is None:
                abort(422)
            if name is not None:
                get_actor.name = name
            if age is not None:
                get_actor.age = age
            if gender is not None:
                get_actor.gender = gender
            get_actor.update()
            return jsonify({
                'success': True,
            })
        except Exception:
            abort(422)

    
# -------------------------------------------------------------#
# DELETE controllers
# -------------------------------------------------------------#

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id):
        try:
            specific_movie = Movies.query.get(movie_id)
            if specific_movie is None:
                abort(404)
            specific_movie.delete()
            movie_data = Movies.query.all()
            movie_list = []
            for movie in movie_data:
                movie_list.append(movie.format())

            return jsonify({
                'success': True,
                'deleted': specific_movie.id,
                'movies': movie_list,
                'total movies': len(movie_list)
            })

        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(actor_id):
        try:
            specific_actor = Movies.query.get(actor_id)
            if specific_actor is None:
                abort(404)
            specific_actor.delete()
            actor_data = Actors.query.all()
            actor_list = []
            for actor in actor_data:
                actor_list.append(actor.format())

            return jsonify({
                'success': True,
                'deleted': specific_actor.id,
                'actors': actor_list,
                'total actors': len(actor_list)
            })

        except Exception:
            abort(422)

# -------------------------------------------------------------#
# POST contollers
# -------------------------------------------------------------#

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie():
        body = request.get_json()
        try:
            title = body.get('title')
            release_date = body.get('release_date')

            specific_movie = Movies(title=title, release_date=release_date)
            specific_movie.insert()

            movie_data = Movies.query.all()
            movie_list = []
            for movie in movie_data:
                movie_list.append(movie.format())

            return jsonify({
                'success': True,
                'movies': movie_list,
                'total movies': len(movie_list)
            })

        except Exception:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor():
        body = request.get_json()
        try:
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            specific_actor = Actors(name=name, age=age, gender=gender)
            specific_actor.insert()

            actor_data = Actors.query.all()
            actor_list = []
            for actor in actor_data:
                actor_list.append(actor.format())

            return jsonify({
                'success': True,
                'movies': actor_list,
                'total movies': len(actor_list)
            })

        except Exception:
            abort(422)

# ----------------------------------------------------------------------------#
# Error Handling
# ----------------------------------------------------------------------------#
    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "not authorized"
        }), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'reason': "resource not found",
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'reason': "unprocessable",
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'reason': "bad request",
        }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 405,
            'reason': "method not allowed",
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500


    return app

APP = create_app()

# ----------------------------------------------------------------------------#
# Launch
# ----------------------------------------------------------------------------#
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
