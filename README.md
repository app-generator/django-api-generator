# [Django API Generator](https://github.com/app-generator/django-api-generator)

The tool is able to `generate APIs` using **Django & DRF** stack with a minimum effort.

> Actively supported by [AppSeed](https://appseed.us/) via `Email` and `Discord`.

<br />

## How to use it

<br />

> **Step #1** -  Install the package via `PIP` 

```bash
$ pip install django-api-manager
// OR
$ pip install git+https://github.com/app-generator/django-api-generator.git
```

<br />

> **Step #2** -  `Register the model` in `core/settings.py` (API_GENERATOR section)

```python
API_GENERATOR = {
    'books': "Book", # <-- Books model provided as sample
}
```

<br />

> **Step #3** - `Migrate Database`

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> **Step #4** - `Generate API` 

```bash
$ python manage.py generate-api
```

The code is generated under the `api` folder in the root of the project.

<br />

> **Step #5** - `Use API` 

If the managed model is Books, the API interface is `/api/books/` and all CRUD methods are available. 

<br />

---
[Django API Generator](https://github.com/app-generator/django-api-generator) - Open-source library provided by **[AppSeed](https://appseed.us/)**
