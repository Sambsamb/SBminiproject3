# Mini Project 3
>INF601 - Advanced Programming in Python
>
>Sam Boutros
> 
> Prof. Zeller
> 
>FHSU - Fall 2022
>
>10/23/2022
>
This is a Flask project to deploy a small web app. This 'bigfoot' App is a Web App for posting big foot sightings :) 

## Initialize the database
First you need to initialize the database:
```Python
flask --app bigfoot init-db
```
## Run locally
To run this app locally use:
```Python
flask --app bigfoot --debug run
```
## Testing
To run the tests, use the pytest command
```Python
pytest
```
You should see output like:
```Python
=========================================================== test session starts ===========================================================
platform win32 -- Python 3.10.6, pytest-7.1.3, pluggy-1.0.0
rootdir: D:\myFolder\SBminiproject3-BigFoot, configfile: setup.cfg, testpaths: tests
collected 24 items

tests\test_auth.py ........                                                                                                          [ 33%]
tests\test_blog.py ............                                                                                                      [ 83%]
tests\test_db.py ..                                                                                                                  [ 91%]
tests\test_factory.py ..                                                                                                             [100%]

=========================================================== 24 passed in 3.25s ============================================================ 
```
To measure the code coverage of the tests, use the coverage command to run pytest instead of running it directly:
```Python
coverage run -m pytest
```


