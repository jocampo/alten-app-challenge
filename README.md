# Alten App Challenge
-----------------------
This repository holds my solution for the Alten App Challenge.

You can visit the hosted version (which auto-deploys on each push) [here](https://jocampo-alten-app-challenge.herokuapp.com/).

## Table of Contents

- [Approach](#approach)
- [Installation](#installation)

## Approach

The idea here is to give the "Hotel IT Team" a platform to build and configure upon. The solution
includes a RESTful API with 3 resources:
- Guest `(/api/v1/guests)`
- Room `(/api/v1/rooms)`
- Reservation `(/api/v1/reservations)`

Each one of these has the usual CRUD operations (following the usual routing for each operation).
For a more complete reference, please check out the [Swagger UI page](https://jocampo-alten-app-challenge.herokuapp.com/swagger).

This allows the users to create users, rooms and assign them to a reservation.

An additional route exists in order to check the availability of a room without necessarily creating a reservation (which also performs this check).
- Check Room Availability -> `(/api/v1/check_room_availability)`

## Installation

1. Download the repository and install the dependencies with pipenv:

```sh
pipenv install
```

2. Set up a database instance (either through heroku or another instance)
### Using a Heroku Postgres instance
By default, this project uses a Heroku Postgres deployment and grabs the connection string
by leveraging the `Heroku CLI` during runtime (i.e. `heroku config:get DATABASE_URL -a jocampo-alten-app-challenge`).
Heroku cycles this connection string periodically, so it's necessary to fetch the value on runtime instead of putting
it on a config file.

In order to have your own Heroku Postgres instance, [create an app on heroku](https://devcenter.heroku.com/articles/creating-apps)
and then follow [these steps](https://devcenter.heroku.com/articles/heroku-postgresql).

Remember, you'll need to install the `Heroku CLI` if you want to go this route. You can find
a guide [here](https://devcenter.heroku.com/articles/heroku-cli).

### Using a different DB / installation
However, if you wish to use another database/instance, you can set up the following **OS environment variable**, which
the app will give priority to, if it's set.

variable name: `DATABASE_URL` -> value `postgresql://...`

The app will read that variable during runtime and use that connection string if it exists.

### Database Schema
In order to make working as a collaborative team as easy as possible for the "Hotel IT department",
I have set up database migrators through [Alembic](https://alembic.sqlalchemy.org/en/latest/).

These migrators handle the DDL and create the tables that the app needs.

In order to run all migrators, simply type:
```sh
alembic upgrade head
```
If you wish to revert a migrator, you can go back 1 revision with:
```sh
alembic downgrade -1
```
or you can also revert all of them with:
```sh
alembic downgrade base
```
#### Creating a new migrator
In order to create a new migrator (if you wish to alter a table or create a new one, for example),
type the following:
```sh
alembic revision -m "change description"
```
This will create a new migrator file in the `/alembic/versions/` folder, which you can then modify
with the desired changes. (Make sure to add both an implementation for `upgrade` and `downgrade`! in case
you need to revert a change in the future).

### Starting the Flask app
You're almost there! now you need to type the following to start the server. From the project root, type
the following:
```sh
flask run
```
Flask uses the `5000` port by default, so you should be able to open the url: `http://127.0.0.1:5000/`
and see something similar to this:
![local.png](/readme_files/local.png)
