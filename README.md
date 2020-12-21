# DataRepProject
A repo with just the relevant files for the project

Here I am copying just the relevant files for the project from my other folder.

## This repository contains:

## Instructions on running the project:

## Files contained






- `python -m venv venv`

- `pip install -r requirements.txt` to load a file of packages. I don't need to do this everytime once the virtual environment has been created

- `source venv/bin/activate`

- `export FLASK_APP=application`

- `export FLASK_ENV=development`

- `flask run`

- `deactivate` to leave the virtual environment and go back to using the system wide environment.
---

These are the instructions I used for first getting it up and running. 
On the command line terminal:

- `mkdir webApp`
- `cd webApp`
- `touch .gitignore`
- `echo /venv > .gitignore`
- `touch README.md`
- `python -m venv venv`
- `source venv/bin/activate`
- `pip freeze`
- `pip install flask`
- `pip freeze > requirements.txt`

The requirements.txt file contains the requirements including `requests` and `python-mysql-connector`





