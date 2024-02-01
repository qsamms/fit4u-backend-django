Instructions for setting up environment:

Clone the repo: 
<pre>
git clone https://github.com/qsamms/fit4u-backend-django.git
</pre>

You'll need to install MySQL and start it up before running the server, easiest way to install MySQL (if you're on macOS) is using homebrew, if you don't have it on your machine download here: 
<pre>
https://brew.sh/
</pre>

Then install MySQL using brew:
<pre>
brew install mysql
</pre>

If you haven't before, you'll need to set up a root user/password with MySQL, once this is done the MySQL server can be started:
<pre>
brew services start mysql
</pre>

Create a virutal environemnt in the root directory: 
<pre>
python -m venv venv
</pre>

Activate the environment: 
<pre>
source /venv/bin/activate
</pre>

Install project dependencies: 
<pre>
python -m pip install -r requirements.txt
</pre>

Then you'll have to add the MySQL user and password environment variables so they aren't plaintext in the code.
To do this, add the following lines to the `activate` script in the /venv/bin director
<pre>
export MYSQL_USERNAME="YOUR_MYSQL_USERNAME"
export MYSQL_PASSWORD="YOUR_MYSQL_PASSWORD"
</pre>

You'll also need to add the google oauth client id and client secret in order to allow users to sign in with google, 
add these values as environment variables in the `activate` script in /venv/bin directory 
<pre>
export GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
export GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"

To verify everything has worked correctly run the following commands: 
<pre>
python manage.py migrate
python manage.py runserver
</pre>

The migrations should be correctly applied and the server should start on port 8000
