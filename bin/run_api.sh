#!/bin/bash
FLASK_ENV=development UI_FOLDER=$(pwd)/dist FLASK_APP=./src/api pipenv run flask run
