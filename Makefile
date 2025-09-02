run:
	python manage.py runserver

mig:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic

shell:
	python manage.py shell

