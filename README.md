# DjangoChatApp

This Django App Contains:
1. Signup for new user
2. Login
3. Logout
4. Chat Rooms
5. Online Users
6. Personal Chat with online users
7. Suggest friends based on users.json file data from an algorithm which suggests from similar age and interests


SetUp Instruction:
1. Clone Repository
2. Set up virtual environment: (cmd: python -m venv virtualenvname)
3. install libraries from requirements.txt, reverify installation of django, channels, daphne, djangorestframework
4. Set up database: (cmd: python manage.py makemigrations -> then -> python manage.py migrate)
5. Run tests: (cmd: python manage.py test)
6. Run application: (cmd: python manage.py runserver)


Online Hosting on AWS EC2:
1. Permanent Deployment could not be done properly
2. However, it is deployed to run well on an ip adrress
3. Url for testing: http://13.49.67.243:8000/
4. Note: This link will work only when this ec2 instance is running on aws on my computer (it will mostly be on for next few days)
5. Feel free to test on multiple browsers and also if the instance is not running, ping me on abhishant11@gmail.com, so that i can rerun it for testing
6. Credentials to access admin: url: http://13.49.67.243:8000/admin/ username: admin, password: Aws2345#

Snapshots of App: Can be found in Snapshots directory
