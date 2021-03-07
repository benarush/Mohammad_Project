Hello Mobileye and Welcome to MPB . 
There is not front-end in this project, only clean REST-API views.

DB decision - SQLlite
i use sqlite to keep it simple for this project. 

7.c) arbitrary rule - i think that it will be sensible for the post-title to be 
unique.

Run Instractions:
option 1 - Run Directly from current os , 
simply run command - python or python3 manage.py runserver 0.0.0.0:8000

option 2 - Run From Docker 
i attached the image, but i added also the Dockerfile and the Docker-compose.yml with 
the dependencies libraries in case you want to build yourself . 

IMPORTENT - I build a bot that responsible tם דtream data to DB and check the API calls.
to run the bot - python manage.py automatebot --action=realperform  . RECOMMENDED!

Testing API instractions: 
option 1 - from TestingAPI.py file . 
Eazy and simple , at the end of the file there is function calls with a print of the output, 
just choose one and remove the comment :)

option 2 - POSTMAN 
here is all the postman example for all API end-points 
[
	Create post 
	POST Method
	url - http://127.0.0.1:8000/postAPI/
		Header:
		|________key_______|________________________Value____________________|
		|  Authorization   |  Token 1131826114b74ffb36bfc2082c515491f7aa70f6 |
		|__________________|_________________________________________________|

		Body : 
		{
			"title": "hellloooo",
			"content": "nice try"
		}

	Update post 
	PUT METHOD 
	url - http://127.0.0.1:8000/postAPI/
		Header:
		|________key_______|________________________Value____________________|
		|  Authorization   |  Token 1131826114b74ffb36bfc2082c515491f7aa70f6 |
		|__________________|_________________________________________________|

		Body : 
		{
			"post_id": "944" , 
			"title": "go go og",
			"content": "hello"
		}

	Delete post
	DELETE METHOD
	url - http://127.0.0.1:8000/postAPI/
		Header:
		|________key_______|________________________Value____________________|
		|  Authorization   |  Token 1131826114b74ffb36bfc2082c515491f7aa70f6 |
		|__________________|_________________________________________________|

		Body : 
		{
			"post_id": "944" , 
		}
		
	Create User:
	POST METHOD
	url - http://127.0.0.1:8000/postAPI/
		Body:
		{
			"username": "TestTestUser",
			"password": "TestUserHi",
			"email": "TestUser@gogogo.com"
		}

	Get UserToken
	POST METHOD
	url - http://127.0.0.1:8000/login/
		Body: 
		{
		"username": "TestTestUser",
		"password": "TestUserHi"
		}
		
	Get all posts with all data
	GET METHOD
	url - http://127.0.0.1:8000/postAPI/
		BODY: None

	Create post like
	POST METHOD 
	url - http://127.0.0.1:8000/post_like/
		Body : 
		{
			"post": 944
		}
]


