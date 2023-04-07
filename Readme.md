# DNA101 Blog API
DNA101 Blog is a web application that allows users to create and share blogs and courses on various topics related to BioMedical Informatics.

## Technologies
The following technologies were used in this project:

* Django
* Ninja Framework
* SQLite
* JWT Authentication

## Setup

To run this project, you will need Python 3.x and pip installed.

### Clone the repository:

```sh
git clone https://github.com/hassan12ammar/dna101blog-backend.git
```

```sh
cd dna101blog-backend
```

### Create a virtual environment and activate it:

```sh
python -m venv dna101blog_venv
```

```sh
source dna101blog_venv/bin/activate
```

#### if you use **fish**

```sh
$ source dna101blog_venv/bin/activate.fish
```

### Install dependencies:

```sh
pip install -r requirements.txt
```

### Run migrations:

```sh
python manage.py migrate
```

### runserver to start the project

```sh
python manage.py runserver
```


