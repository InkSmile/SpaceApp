# Installation

First of all copy git repository

```bash
git clone https://github.com/InkSmile/SpaceApp.git
```

Then you need to install [Docker](https://docs.docker.com/engine/install/)

After you need to run docker-compose file

```bash
docker-compose up --build
```

Wait until docker buil your project. In your browser enter url http://127.0.0.1:8000

Open postman if you want to test api endpoints

Endpoints:

http://127.0.0.1:8000/v1/auth/sign-up/	#sign up user with email and password

http://127.0.0.1:8000/v1/auth/activate/	#then you go to email you used for sign up and 	copy token from url and insert into your request body, for example ```"token": "asdnajksd"```

http://127.0.0.1:8000/v1/auth/verify/	# verify JWT	

http://127.0.0.1:8000/v1/auth/refresh/	#refresh JWT token


Also if you want to use admin panel you have enter into your docker container. You can do it by using command

```bash
docker exec -it django_api bash
```
Then
```bash
cd application/
```
```bash
python manage.py createsuperuser
```
and fulfill the fields

After successful creation you can go to your admin page
http://127.0.0.1:8000/admin/


