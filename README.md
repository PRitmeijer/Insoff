# INSOFF
INSOFF Project

## Overview

There is nothing yet here!

## Dependencies

- PostgreSQL 10 and higher (for development phase sqlite3 is used, so no need to worry about PostgreSQL yet) 

## Installation

For a fresh installation. Open a terminal and execute:

```bash
git clone git@github.com:PPRitmeijer/Insoff.git
cd Insoff/tmp
python -m venv env
env/scripts/activate
cd ..
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py compress --force
python manage.py runserver

```

Make sure when deploying to production that the env variables are set to production:
```
set DJANGO_SETTINGS_MODULE=insoff.settings.production
```
