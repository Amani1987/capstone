# Backend API For Casting Agency App
### Motivation for project
This is the capstone project for the udacity full stack nanodegree program.

## Getting Started
### Installing Dependencies
Python 3.6 or 3.7
Follow instructions to install the latest version of python for your platform in the python docs

### Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running:

pip install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

### Running the server
In order to run the server locally, firstly navigate to the project directory, then execute:

export FLASK_APP=app
export FLASK_APP=development
flask run

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to src/app.py directs flask to use the app.py` file to run the application.

Besides, the server has also been deployed on the Heroku cloud platform, you can access the application via the following URL:

https://casting-agency5.herokuapp.com/

### Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, create a database and add an env variable 'DATABASE_URL' which is your postgres connection url, run migrations using:

flask db init
flask db migrate
flask db upgrade
Running the server
From within the your directory first ensure you are working using your created virtual environment.


## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models
Movies with attributes title and release date Actors with attributes name, age and gender


### Casting Assistant:
username : assisstant@yahoo.com
password : Ud@city20
#### Roles
view:actors
view:movies

### Casting Director:
username : director@yahoo.com
password : Ud@city20
#### Roles
All permissions a Casting Assistant has
create:actor
delete:actor
update:actor
update:movie

### Executive Producer:
username : producer@yahoo.com
password : Ud@city20
#### Roles
All permissions a Casting Director has
create:movie
delete:movie

## Endpoints
GET '/' : 
This endpoint returns a JSON object representing what could be the home page
"Welcome to The Great Casting Agency"

GET /movies: 
Requires permission get:movies
Retrieves a list of all the movies

GET /actors:
Requires permission get:actors
Retrieves a list of all the actors

DELETE /actor/<actor_id>:
Requires permission delete:actor
Delete actor with the specified actor id from the DB

DELETE /movie/<movie_id>
Requires permission delete:movie
Delete movie with the specified movie id from the DB

POST /actor:
Requires permission post:actor
Post an actor to the DB
JSON body format
{
	"name": "Mark Hamill", 
	"age": 68,
	"gender": "Male"
}

POST /movie:
Requires permission post:movie
Post a movie to the DB
JSON body format
{
    "title": "Star Wars: A New Hope",
    "release_date": "1977"
}

PATCH /actor/<actor_id>:
Requires permission patch:actor
Edit an existing actor with the specified actor id
Same JSON format as POST

PATCH /movie/<movie_id>:
Requires permission patch:movie
Edit an existing movie with the specified movie id
Same JSON format as POST


## API Reference
The API will return three types of errors:

400 – bad request
401 - not authorized
404 – resource not found
405 - method not allowed
422 – unprocessable
500 - internal server error



