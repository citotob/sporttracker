rd /q /s .\apps\userinfo\__pycache__\
rd /q /s .\apps\userinfo\migrations\

echo "删除__pycache__和migrations"
pause
python manage.py makemigrations userinfo
python manage.py migrate
python manage.py createsuperuser