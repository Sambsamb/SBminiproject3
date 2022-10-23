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
The following PowerShell automation will install this Web App on a Windows server:
```PowerShell
# Get AZSBTools PowerShell module
Set-PSRepository -Name PSGallery -InstallationPolicy Trusted 
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 
Remove-Module AZSBTools -Force -EA 0 
Install-Module AZSBTools -Force -AllowClobber -SkipPublisherCheck # -Scope CurrentUser
Import-Module AZSBTools -DisableNameChecking -Force 
Get-Module AZSBTools

# Install Python if not installed
Install-Python

# Create an environment
New-Item -Path .\ -Name bigfoot -EA 0 
Set-Location .\bigfoot
py -3 -m venv venv

# Activate the environment
.\venv\Scripts\activate

# Update pip
python -m pip install --upgrade pip

# Install Flask
pip install Flask

# Install bigfoot
$AppName  = 'bigfoot'
$DistName = 'bigfoot-1.0.0-py3-none-any.whl'
$DistURL  = "https://github.com/Sambsamb/SBminiproject3/blob/master/dist/$($DistName)?raw=true"
Invoke-WebRequest -Uri $DistURL -OutFile ".\$DistName"
pip install $DistName

# Initialize the DB
flask --app $AppName init-db

# Set a secret key, save to config.py in the instance folder
$Key = New-Password 
"SECRET_KEY = '$Key'" | Out-File .\venv\var\bigfoot-instance\config.py

# Install waitress
pip install waitress

# Run the web App
waitress-serve --call "$($AppName):create_app"
```

