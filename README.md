# [Django API Generator](https://github.com/app-generator/django-api-generator)

The tool is able to `generate APIs` using **Django & DRF** stack with a minimum effort.

> Actively supported by [AppSeed](https://appseed.us/) via `Email` and `Discord`.

<br />

## How to use it

<br />

> **Step #1** - Install the package via `PIP` 

```bash
$ pip install django-api-generator
// OR
$ pip install git+https://github.com/app-generator/django-api-generator.git
```

<br />

> **Step #2** Update Configuration, include the new APP

```python
INSTALLED_APPS = [
    'django_api_gen',            # Django API GENERATOR  # <-- NEW
    'rest_framework',            # Include DRF           # <-- NEW 
    'rest_framework.authtoken',  # Include DRF Auth      # <-- NEW   
]
```

<br />

> **Step #3** - `Register the model` in `core/settings.py` (API_GENERATOR section)

```python
API_GENERATOR = {
    # pattern: 
    # API_SLUG -> Import_PATH 
    'books'  : "app1.models.Book",
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

<br />

> **Step #4** - `Migrate Database`

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> **Step #5** - `Generate API` 

```bash
$ python manage.py generate-api
```

The code is generated under the `api` folder in the root of the project.

<br />

> **Step #6** - `Use API` 

If the managed model is Books, the API interface is `/api/books/` and all CRUD methods are available. 

<br />

---
[Django API Generator](https://github.com/app-generator/django-api-generator) - Open-source library provided by **[AppSeed](https://appseed.us/)**
