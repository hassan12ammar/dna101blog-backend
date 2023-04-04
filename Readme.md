# GoCardless sample application

## Setup

The first thing to do is to clone the repository:

```sh
git clone [Repo URL]
```

```sh
cd dna101blog
```

### Create a virtual environment to install dependencies in and activate it:

```sh
python -m venv dna101blog_venv
```

```sh
source dna101blog_venv/bin/activate
```

#### if you use fish

```sh
source dna101blog_venv/bin/activate.fish
```

### Then install the dependencies:

```sh
pip install -r requirements.txt
```

### Once `pip` has finished downloading the dependencies:
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

### runserver to start the project
```sh
python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/admin`.

