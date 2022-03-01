# django-recipe-exercise

## Description

CRUD API created using Docker, Django, DRF and Postgres that allows you to CRUD recipes and add/delete ingredients to it.


## Installation

Once you download the project run the following to download the images and build the application:

```
docker-compose build
```

## Usage

To start the application:

```
docker-compose up
```

After that the API will run on 127.0.0.1:8000

###Examples:

Get recipes
```
GET http://127.0.0.1:8000/api/recipe/recipes
```

Get recipes filtered by name substring
```
GET http://127.0.0.1:8000/api/recipe/recipes?name='Pizz'
```

Get recipe 
```
GET http://127.0.0.1:8000/api/recipe/recipes/{recipe_id}
```

Create a new recipe
```
POST http://127.0.0.1:8000/api/recipe/recipes
```

Update recipe
```
PATCH http://127.0.0.1:8000/api/recipe/recipes/{recipe_id}
```

Delete recipe
```
DELETE http://127.0.0.1:8000/api/recipe/recipes/{recipe_id}
```

## Tests

Automated tests have been implemented. You can run them doing the following:

```
docker-compose run app sh -c "python manage.py test"
```