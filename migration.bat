@echo off
echo Running makemigrations for Django apps...

py .\manage.py makemigrations common app hydrogeological hydromelioratical hydrometeorological

py .\manage.py migrate

pause