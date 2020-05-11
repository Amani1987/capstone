import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import setup_db, Movie, Actor, db

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        self.database_path = "postgres://postgres:1@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqa3hNRU01UlRKQ05EQXdRalkxTjBGRU1qSkNPVE5DTlROQ016VTRRalZDTURNMFJVSTFRZyJ9.eyJpc3MiOiJodHRwczovL25ld2RldmVsb3Blci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDA2MTg1NGIxNGMwYzEyODBlNDY0IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4ODg4MTQ0OCwiZXhwIjoxNTg4ODg4NjQ4LCJhenAiOiJkV01NdnU0ajl5ZmcyNGF5T2czUXZSM05FNzFkanNVcyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.JYeYU8se7shG-J073iSlaOzWVGYwF95Wt9HpPKIikWfISWgTw02C90sJ7A5z1R1AVRKKjIpAhF9buoSSGWtngjrtcCpfUx4JoYYGr01XJ6GL1m5PmoSTTHEzaOyXTEtJf2gxnBqxxDxtxsDdTyJ2fokdnyB9ipHl8ctGtJa-yOSaQ3hiQwi4tqD9CoaoFcK1oeKX6W25k5sAm8DAh0GS-qziH1kBMnrisIRbBQ-5ubUfV0OfUREMFcBbzkuQQssVv6wMGD_CoWxTk2Br2HVROtksV2VKMgRhJBwsNps5FzAJ3t6mo8FZk1vNX2aK-RISzjXOAdm7jwjB2gP3p8B2ZA'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqa3hNRU01UlRKQ05EQXdRalkxTjBGRU1qSkNPVE5DTlROQ016VTRRalZDTURNMFJVSTFRZyJ9.eyJpc3MiOiJodHRwczovL25ld2RldmVsb3Blci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDBhODgxY2MxYWMwYzE0OGZhMGE3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4ODg4OTg1OSwiZXhwIjoxNTg4ODk3MDU5LCJhenAiOiJkV01NdnU0ajl5ZmcyNGF5T2czUXZSM05FNzFkanNVcyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiY3JlYXRlOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.PlrXG0g77Aox4JglWFDv8mvpdBsFZ11S9L-zLSyLE28Ny-CIAqSNkvnx0_6Cj4hcKoo9UwqliS8pnv3NJhyoaI7-2bR7aq2_o-suICVcYlvBOJ7XYYtEdL1RK-kUaLVD9OvMUuwD8uBwKoJgKWzJCeEeSL9XjzuNigR3nbhv_L7Ox4BJCaBGqthGHJllPGoW6LdInL0YLZK55kHOLP_jv_MAXjp6NcTXKka18oLLvGBaxlaHHDNLHp_X0pvGJGA9oX--n_DxkG9vdTqCKoF5NsE32ghHn159P6aPyWBrucwjMQea2tAoH8004lLZXbx4AgM8ctSMSPabunFEORwZgQ'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqa3hNRU01UlRKQ05EQXdRalkxTjBGRU1qSkNPVE5DTlROQ016VTRRalZDTURNMFJVSTFRZyJ9.eyJpc3MiOiJodHRwczovL25ld2RldmVsb3Blci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNDBhODgxY2MxYWMwYzE0OGZhMGE3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4ODkzNTQ0NCwiZXhwIjoxNTg4OTQyNjQ0LCJhenAiOiJkV01NdnU0ajl5ZmcyNGF5T2czUXZSM05FNzFkanNVcyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiY3JlYXRlOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.e62vhBI_LBrdyG7nnAeYcCSDU29aBqkAcY56x8eSqrdF7uuuMwrXAkXBQPsnV6LwOyWvX5is3CbqijwcTZg37ECXLOKvvOcCZNde4o-_2mR_11975XP8bsm7muy6vLOvYynQcePX6F_Vj3a_nxyFVTHYJbrFXFOJUj1bwhW_7oBWXDudaBWOlK4Pif3YfgeTyX9RbaDjhrYTvK9wcsqe9klVEQlZ150smIIpMUWLQqxrfjqCcKGCxhXjmv4u_eF853E4HNU1wF3TDqaBeEzSZTqwmOVWdaJsmzeKcpBIdgWe61PLkdGd_2vrX6rzmIxtx3YHu6W3Yw2WC7A8gxQKYg'
        }

        self.movie = {
            'title': 'The Godfather',
            'release_date': '1972'
        }

        self.new_movie = {
            'title': 'Toy Story 4',
            'release_date': '2019'
        }

        self.actor = {
            'name': 'Leonardo DiCaprio',
            'age': '46',
            'gender': 'Male'
        }

        self.new_actor = {
            'name': 'Meryl Streep',
            'age': '71',
            'gender': 'Female'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #Seed test data
        self.client().post('/movies', json=self.movie, headers=self.executive_producer_header)
        self.client().post('/actors', json=self.actor, headers=self.executive_producer_header)  

    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
        pass

    # Test GET Actors
    def test_get_actors_public(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 401)

    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_director(self):
        res = self.client().get('/actors', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_producer(self):
        res = self.client().get('/actors', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    # Test GET Movies
    def test_get_movies_public(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 401)

    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_director(self):
        res = self.client().get('/movies', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_producer(self):
        res = self.client().get('/movies', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    # Test POST Actor
    def test_post_actors_public(self):
        res = self.client().post('/actors', json=self.new_actor)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_director(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor, headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_post_actors_producer(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor, headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test POST Movie
    def test_post_movies_public(self):
        res = self.client().post('/movies', json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_assistant(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_director(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.director_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_producer(self):
        original_count = len(Movie.query.all())

        res = self.client().post('/movies', json=self.new_movie, headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test PATCH Actor
    def test_patch_actors_public(self):
        res = self.client().patch('/actors/1', json={'age': "71"})

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_assistant(self):
        res = self.client().patch('/actors/1', json={'age': "71"}, headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_director(self):
        res = self.client().patch('/actors/1', json={'age': "71"}, headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_producer(self):
        res = self.client().patch('/actors/1', json={'age': "71"}, headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_does_not_exist(self):
        res = self.client().patch('/actors/1000', json={'age': "43"}, headers=self.producer_header)
        
        self.assertEqual(res.status_code, 404)

    def test_patch_actors_no_data(self):
        res = self.client().patch('/actors/1', headers=self.producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test PATCH Movie
    def test_patch_movies_public(self):
        res = self.client().patch('/movies/1', json={'title': "The Witch"})

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_assistant(self):
        res = self.client().patch('/movies/1', json={'title': "The Witch"}, headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_director(self):
        res = self.client().patch('/movies/1', json={'title': "The Witch"}, headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_producer(self):
        res = self.client().patch('/movies/1', json={'title': "The Witch"}, headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_does_not_exist(self):
        res = self.client().patch('/movies/1000', json={'title': "Updated Title"}, headers=self.producer_header)
        
        self.assertEqual(res.status_code, 404)

    def test_patch_movies_no_data(self):
        res = self.client().patch('/movies/1', headers=self.producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test DELETE Actor
    def test_delete_actors_public(self):
        res = self.client().delete('/actors/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_assistant(self):
        res = self.client().delete('/actors/1', headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_director(self):
        res = self.client().delete('/actors/1', headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_producer(self):
        res = self.client().delete('/actors/1', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test DELETE Movie
    def test_delete_movies_public(self):
        res = self.client().delete('/movies/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_assistant(self):
        res = self.client().delete('/movies/1', headers=self.assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_director(self):
        res = self.client().delete('/movies/1', headers=self.director_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_producer(self):
        res = self.client().delete('/movies/1', headers=self.producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=self.producer_header)
        
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()