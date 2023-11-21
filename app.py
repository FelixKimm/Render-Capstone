import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth

from models import setup_db, Team, Player



def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    # @app.route('/')
    # def index():
    #     # return "Available endpoints: /teams or /players"
    #     teams = Team.query.all()
    #     for team in teams:
    #         print(f"Team Name: {team.name}")
    #         print("Players:")
    #         for player in team.players:
    #             print(f"-{player.name}")
    #         print("\n")
    #     return "a"

    # TEAM ENDPOINTS

    @app.route('/teams', methods=['GET'])
    @requires_auth('get:team')
    def get_teams(payload):
        teams = Team.query.all()

        if len(teams) == 0:
            return 'There are no teams in the database!'

        formatted_teams = []
        for team in teams:
            team_data = team.format()
            team_data['total_players'] = len(team.players)
            formatted_teams.append(team_data)

        return {
            'success': True,
            'Teams': formatted_teams
        }
    
    @app.route('/teams', methods=['POST'])
    @requires_auth('post:team')
    def create_team(payload):
        body = request.get_json()

        new_name = body.get('name')
        
        if not ('name' in body):
            abort(422)
        
        try:
            team = Team(name=new_name)

            team.insert()

            return jsonify ({
                'success': True,
                'team_id': team.id,
                'team_name': team.name
            })
            
        except:
            abort(422)

    @app.route('/teams/<int:team_id>', methods=['DELETE'])
    @requires_auth('delete:team')
    def delete_team(payload, team_id):
        try:
            team = Team.query.get(team_id)

            if team is None:
                print("This team id does't exist")
                abort(404)

            players_on_team = team.players
            players_deleted = [player.name for player in players_on_team]

            # Delete all players associated with a particular team before deleting the team
            for player in players_on_team:
                player.delete()

            team.delete()

            return jsonify({
                'success': True,
                'deleted_team': team.name,
                'deleted_players': players_deleted
            })
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            abort(422)

    @app.route('/teams/<int:team_id>', methods=['PATCH'])
    @requires_auth('patch:team')
    def patch_team(payload, team_id):
        body = request.get_json()
    
        patch_team = Team.query.get(team_id)
        old_name = patch_team.name

        patch_name = body.get('name')

        if patch_name is None:
            abort(404)
        
        if patch_name:
            patch_team.name = patch_name

        patch_team.update()

        return jsonify ({
            'success': True,
            'old_team_name': old_name,
            'new_team_name': patch_name
        }) 


    # PLAYER ENDPOINTS

    @app.route('/players', methods=['GET'])
    @requires_auth('get:player')
    def get_players(payload):
        players = Player.query.order_by(Player.team_id).all()

        if len(players) == 0:
            return 'There are no players in the database!'

        formatted_players = [player.format() for player in players]

        return {
            'success': True,
            'Players': formatted_players,
            'total_players': len(players)
        }


    @app.route('/players', methods=['POST'])
    @requires_auth('post:player')
    def create_player(payload):
        body = request.get_json()

        new_name = body.get('name')
        team_id = body.get('team_id')

        if not ('name' in body and 'team_id' in body):
            abort(422)

        team = Team.query.get(team_id)
        if not team:
            print('There is no team with this id')
            abort(404)
        try:
            player = Player(name=new_name, team_id=team_id)

            player.insert()

            return jsonify({
                'success': True,
                'player_id': player.id,
                'player_name': player.name,
                'team_id': player.team_id
            })
        except:
            abort(422)

    @app.route('/players/<int:player_id>', methods=['DELETE'])
    @requires_auth('delete:player')
    def delete_player(payload, player_id):
        try:
            player = Player.query.get(player_id)

            if player is None:
                print("This player id does't exist")
                abort(404)
            
            player.delete()

            return jsonify ({
                'success': True,
                'deleted_player': player.name
            })

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            abort(422)

    @app.route('/players/<int:player_id>', methods=['PATCH'])
    @requires_auth('patch:player')
    def patch_player(payload, player_id):
        body = request.get_json()

        patch_player = Player.query.get(player_id)
        old_team = patch_player.team_id

        patch_team_id = body.get('team_id')

        if patch_player is None:
            print("There is no team with this id")
            abort(404)

        if patch_team_id:
            patch_player.team_id = patch_team_id

        patch_player.update()

        return jsonify ({
            'success': True,
            'old_team': old_team,
            'new_team': patch_team_id
        }) 

    # ERROR HANDLERS

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({"success": False, "error": 401, "message": "Unauthorized"}), 401

    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({"success": False, "error": 403, "message": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500, "message": "server error"}), 500
    
    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({"success": False, "error": 401, "message": "server error"}), 401

    return app

app = create_app()