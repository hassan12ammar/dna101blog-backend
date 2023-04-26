# DNA101 API
DNA101 Blog is a web application that allows users to create and share blogs and courses on various topics related to BioMedical Informatics.

DNA101 Blog is a Django/Django Ninja backend that serves as an online blog for BioMedical Informatics students to share courses and blogs about the specialty.
<br>

## Django/Django Ninja Backend
The website is built with Django and uses NinjaAPI to handle the RESTful API. The website includes features such as user authentication, profile management, Blog listing, and Course listing. It provides a RESTful API for interacting with your data and can be easily integrated into your frontend or mobile application.
<br>

## Features
* Authentication and authorization using JWT
* RESTful API for data management
* Admin panel with friendly interface

# Installation and Setup

To run this project, you will nee#d Python 3.x and pip installed.


### Clone the repository:

```sh
git clone https://github.com/hassan12ammar/dna101blog-backend.git
```

```sh
cd dna101blog-backend
```

### First Start:
To make it easier for you to get started with the project, a first_start.sh script has been included in the project. This script does the following:

To run the script, simply execute:

```sh
./first_start.sh
```

### Running the Server:
After the initial setup is done, you can run the server using the start.sh script:

```sh
./start.sh
```

## Creating a New Superuser
To access the admin panel, you will need to create a superuser first:

```sh
python manage.py createsuperuser
```

# API Documentation
API documentation is available at http://localhost:8000/api/docs. You can use the Swagger UI to explore the API and test endpoints.
<br>

# Admin Panel
The admin panel is available at http://localhost:8000/admin. You can use it to manage the database and perform CRUD operations on the models. The admin panel is only accessible to superusers.

By defualt the first_start.sh will create a superuser with:

Email: **mg@gm.com**
Password: **string12**

# License
This project is licensed under the MIT License. Feel free to use and modify it as per your requirements.
<br>

# Contributing
Contributions are welcome! If you have any feature requests, bug reports, or pull requests, please feel free to open an issue or a pull request.
