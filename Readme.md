# Data Transfer System

## Description
Data Transfer System allows to transfer files and URL addresses in a secure way.
The application provides logged-in users the form accepting a file or an URL that should be protected. After uploading the data the user reciev a link and password which allow to access the protected data. The generated link is valid for 24 hours. It could be accessed both registered and unregistered users.
The application also provides API. A secured part for adding new elements, and an unsecured one to enter the password. In addition, there is a secured endpoint which provides information on the number of items of each type, added every day, that have been visited at least once.

## Regular URLs
	/
	/<unique_slag>

## API endpoints
	/api/statistics/
	/api/add-file/
	/api/add-url/
	/api/get-data/<unique_slug>/<password>

## Requirements
	pip3 install django
	pip3 install djangorestframework
	pip3 install markdown
	gunicorn
	django-heroku

## Running the application
	$ python3 manage.py migrate
	$ python3 manage.py runserver
