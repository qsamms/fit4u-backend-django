Instructions for setting up environment:

Clone the repo: 
'''
git clone https://github.com/qsamms/fit4u-backend-django.git
'''

Create a virutal environemnt in the root directory: 
'''
python -m venv venv
'''

Activate the environment: 
'''
source /venv/bin/activate
'''

Install project dependencies: 
'''
pip install -r requirements.txt
'''

Easiest way to install MySQL is using homebrew, if you don't have it on your machine download here: 
'''
https://brew.sh/
'''

Then install MySQL using brew:
'''
brew install mysql
'''

If you haven't before, you'll need to set up a root user/password with MySQL, once this is done the MySQL server can be started:
'''
brew services start mysql
'''

Then you'll have to add the MySQL user and password environment variables so they aren't plaintext in the code.
To do this, add the following lines to the activate file in the /venv/bin folder:
'''
export MYSQL_USERNAME="root"
export MYSQL_PASSWORD="rootpassword"
'''

To verify everything has worked correctly run the following commands: 
'''
python manage.py runserver
python manage.py migrate
'''

The migrations should be correctly applied and the server should start on port 8000
