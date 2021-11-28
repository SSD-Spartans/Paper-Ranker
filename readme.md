# Paper Ranker

----

## Steps to Run the project

- Create virtual env with following command
    > python3 -m venv venv
- Activate the virtual env with following command
    > source venv/bin/activate
- Install requirements with following command
    > pip3 install -r requirements.txt
- Make migrations to db with following command
    > pip3 manage.py makemigrations
- Migrate the db with following command
    > pip3 manage.py migrate
- Run the Django project with following command
    > python3 manage.py runserver
- You can access the web application at url
    > http://localhost:8000/

---

## Admin/Superuser Creation

- Run following command and add all necessary fields to create admin/superuser
    > python3 manage.py createsuperuser

## Admin Endpoints

- "/delete-db" deletes all paper details and conference details
- "/add-conference" adds all conference with their corresponding rankings in db
