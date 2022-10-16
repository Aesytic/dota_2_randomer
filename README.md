# Dota 2 Randomer

## Overview
This is a Dota 2 Hero randomer (for those who don't want to suffer the unforgiving consequences of locking in a hero they hate). By using this app, you can request a random hero multiple times with no consequences. Heroes can also be excluded to ensure that your random will never include heroes that you do not want to play.

## Requirements
This app requires `Python >= 3.6`. Package requirements are captured in `requirements.txt`.

## Installation
1. In the root directory of this repo, run:
```pip3 install -r requirements.txt```
2. In the `db` directory, run DB migrations and create the DB file by running the following:
```alembic upgrade head```
3. Insert heroes into the DB (scripts/tooling to automate this coming soon)
4. Run the following command to start the app:
```python3 run_server.py```
5. Using curl or any other HTTP client, send a GET request to the endpoint `localhost:8000/random/hero`. This will return a random hero 
