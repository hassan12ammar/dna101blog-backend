#!/bin/bash

# Activate the virtual environment using the Fish shell
source pharmace_venv/bin/activate

# Run the Django development server
python manage.py runserver

# Wait for the server to be stopped
wait