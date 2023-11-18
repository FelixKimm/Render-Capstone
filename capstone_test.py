from app import create_app
from models import setup_db, Team, Player
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

club_headers= {'Authorization': f'Bearer {os.environ["CLUB_AUTH_TOKEN"]}'}
viewer_headers = {'Authorization': f'Bearer {os.environ["VIEWER_AUTH_TOKEN"]}'}

class CapstoneTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'capstone_test'
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        self.example_team = {"name": "cortinas"}
        self.example_player = {"name": "Test player", "team_id": 3}

    def tearDown(self):
        pass

    #VIEWER TEST
    def test_get_teams(self):
        res = self.client().get('/teams', headers=viewer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_teams_error(self):
        res = self.client().get('/teams')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_get_players(self):
        res = self.client().get('/players', headers=viewer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_players_error(self):
        res = self.client().get('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    #FORBIDDEN TEST(POST, PATCH, DELETE)

    def test_forbidden_post(self):
        res = self.client().post('/teams', headers=viewer_headers, json=self.example_team)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')

    def test_forbidden_delete(self):
        res = self.client().delete('/teams/13', headers=viewer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')

    def test_forbidden_patch(self):
        res = self.client().patch('/teams/5', headers=viewer_headers, json=self.example_team)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')

    #CLUB TEST
    #TEST TEAMS ENDPOINT
    def test_get_teams(self):
        res = self.client().get('/teams', headers=club_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_teams_error(self):
        res = self.client().get('/teams')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_post_teams(self):
        res = self.client().post('/teams', headers=club_headers, json=self.example_team)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_teams_error(self):
        res = self.client().post('/teams')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_delete_teams(self):
        res = self.client().delete('/teams/13', headers=club_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_teams_error(self):
        res = self.client().delete('/teams/12312312')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_patch_teams(self):
        res = self.client().patch('teams/7', headers=club_headers, json=self.example_team)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_teams_error(self):
        res = self.client().patch('/teams/7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')        

    #TEST PLAYERS ENDPOINT
    def test_get_players(self):
        res = self.client().get('/players', headers=club_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_players_error(self):
        res = self.client().get('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_post_players(self):
        res = self.client().post('/players', headers=club_headers, json=self.example_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_players_error(self):
        res = self.client().post('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_delete_players(self):
        res = self.client().delete('/players/7', headers=club_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_players_error(self):
        res = self.client().delete('/players/12312312')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_patch_players(self):
        res = self.client().patch('/players/6', headers=club_headers, json=self.example_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_players_error(self):
        res = self.client().patch('/players/7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')  


if __name__ == "__main__":
    unittest.main()