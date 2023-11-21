# Udacity Full Stack Capstone Project

Final project for the Udacity Full Stack Web Developer course.
URL for the API: xxxxxxxxxxxxxxxxxx

## General Specifications

* 2 Models: Teams and Players
* Endpoints: Get, POST, PATCH AND DELETE
* 2 Roles: Club and Viewer
* 10 Permissions: GET Team/Player, POST Team/Player, Patch Team/Player, DELETE Team/Player

## Dependencies

* __Python__
* __Flask__
* __SQLAlchemy__
```bash
pip install -r requirements.txt
```

## Run the Server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb capstone
createdb capstone
python capstone_test.py
```

## API Documentation

### Roles

Club
* Permissions: GET Team/Player, POST Team/Player, Patch Team/Player, DELETE Team/Player

Viewer
* Permissions: GET Team/Player

### Endpoints

#### GET '/teams'

* Fetches a dictionary with teams and players of that team
* Roles required: Club or Viewer
* Body: None
* Response:

```
{
    "Teams": [
        {
            "id": 1,
            "name": "Barcelona",
            "players": [
                {
                    "id": 1,
                    "name": "Pedri",
                    "team_id": 1
                },
                {
                    "id": 2,
                    "name": "Gavi",
                    "team_id": 1
                }
            ],
            "total_players": 2
        }
    ],
    "success": true
}
```

#### GET '/players'

* Fetches a dictionary with all players and their team id
* Roles required: Club or Viewer
* Body: None
* Response:
```
{
    "Players": [
        {
            "id": 1,
            "name": "Pedri",
            "team_id": 1
        },
        {
            "id": 2,
            "name": "Gavi",
            "team_id": 1
        }
    ],
    "success": true,
    "total_players": 2
}
```

#### POST '/teams'

* Creates a new team
* Roles required: Club
* Body:
```
{
    "name": "Barcelona"
}
```
* Response:
```
{
    "success": true,
    "team_id": 1,
    "team_name": "Barcelona"
}
```

#### POST '/players'

* Creates a new player with a team attached
* Roles required: Club
* Body:
```
{
    "name": "Pedri",
    "team_id": 1
}
```
* Response:
```
{
    "player_id": 1,
    "player_name": "Pedri",
    "success": true,
    "team_id": 1
}
```

#### PATCH '/teams/int:id'

* Updates a team name
* Roles required: Club
* Body:
```
{
    "name": "Real Madrid"
}
```
* Response:
```
{
    "new_team": "Real Madrid",
    "old_team": "Barcelona",
    "success": true
}
```

#### PATCH '/players/int:id'

* Updates the team id (changing club)
* Roles required: Club
* Body:
```
{
    "team_id": "2"
}
```
* Response:
```
{
    "new_team": "2",
    "old_team": 1,
    "success": true
}
```

#### DELETE '/teams/int:id

* Deletes the team and the players of that team
* Roles required: Club
* Body: None
* Response:
```
{
    "deleted_players": [
        "Gavi",
        "Ter Stegen"
    ],
    "deleted_team": "Liverpool",
    "success": true
}
```

#### DELETE '/players/int:id'

* Deletes the player
* Roles required: Club
* Body: None
* Response
```
{
    "deleted_player": "Pedri",
    "success": true
}
```