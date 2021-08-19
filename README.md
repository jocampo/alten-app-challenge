# Alten App Challenge
This repository holds my solution for the Alten App Challenge.

You can visit the hosted version (which auto-deploys on each push) [here](https://jocampo-alten-app-challenge.herokuapp.com/).

## Table of Contents

- [Approach](#approach)
- [Installation](#installation)
- [Deployment](#deployment)
- [Tech Used](#tech-used)
- [Next Steps](#next-steps)

## Approach

The idea here is to give the "Hotel IT Team" a platform to build and configure upon. The solution
includes a RESTful API with 3 resources:
- Guest `(/api/v1/guests)`
- Room `(/api/v1/rooms)`
- Reservation `(/api/v1/reservations)`

Each one of these has the usual CRUD operations (following the usual routing for each operation).
For a more complete reference, please check out the [Swagger UI page](https://jocampo-alten-app-challenge.herokuapp.com/swagger).

This allows the end users to create users, rooms and assign them to a reservation.

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
and then follow [these steps](https://devcenter.heroku.com/articles/heroku-postgresql), you can always choose a free plan here.

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

3. In order to run all migrators, simply type:
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
4. You're almost there! now you need to type the following to start the server. From the project root, type
the following:
```sh
flask run
```
Flask uses the `5000` port by default, so you should be able to open the url: `http://127.0.0.1:5000/`
and see something similar to this:

![local.png](/readme_files/local.png)

## Deployment

This app is currently configured to auto-deploy on a Heroku app whenever a push is made to the `main` branch of this git repo.

Whenever a deployment happens, all the missing migrators are executed (if any). This ensures that the database isn't out of sync with the app models.

Additionally, we use [Green Unicorn](https://gunicorn.org/) as a WSGI server to our Flask app in our rudimentary production environment. We need this interface in order boot up multiple worker instances of our app(thus being able to handle more requests at a time).

Lastly, we use the free tier of Heroku Postgres for our Heroku app.

## Ideas in order to achieve 99.99% uptime
"4 nines" means a bit less than 1 hour of downtime per year. In order to achieve that, the following changes would need to be implemented:
 - Set up monitoring for the uptime and performance of the app, as well as alerts of the resource availability of the web and database servers. This would allow the IT department to preemptively tackle issues such as disk-space running out or server's memory being at full capacity for a long period of time.
    - A separate, serverless function can be implemented to measure the response time of the app, by making a simple request to the app.
    We could invoke this function every minute and create thresholds to alert the IT department if the response time is higher than X ms.
- TODO: add more here

## Tech Used
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) (and several add-ons to make things easier)
- [SQLAlchemy](https://www.sqlalchemy.org/) (+ [psycopg2](https://pypi.org/project/psycopg2/))
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Gunicorn](https://gunicorn.org/)
- [Pytest](https://docs.pytest.org/en/6.2.x/)
- [Heroku](https://www.heroku.com)

## Next Steps
The following steps (if time was not a constraint) for the app would be:
- Increase unit test coverage (right now only a couple of components per layer have been unit tested).
- Integrate the unit tests into a Continous Integration environment.
- Only auto-deploy to Heroku if the unit tests pass in the CI.
- For collaboration, Heroku can be leveraged to deploy branches in PRs, which would be useful for reviewers.
- Add logging to the app.
- Add monitoring to the app.
- Enforce code format with [Black](https://github.com/psf/black).
- Adding a cache layer so that we don't hit the DB every time. Updating it as needed