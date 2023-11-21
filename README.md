# Udacity Full Stack Capstone Project

Final project for the Udacity Full Stack Web Developer course.
URL for the API: xxxxxxxxxxxxxxxxxx

## General Specifications

* Models with:


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

## API Documentation for the Capstone Project