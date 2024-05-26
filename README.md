Technologies Used:
Python Standard Libraries:
--http.server 
--http.cookies 
--urllib.parse 
--socketserver 
--psycopg2

Database Interaction:

psycopg2 to connect with a Postgres DB and get/post/put user data in a table users

GET

--Register Page: Serves the registration HTML page
--Login Page: Serves the login HTML page
--Logged-in Page: Serves a profile HTML page for logged-in users
--Logout: Clears the session cookie and redirects to the login page, still not working correctly
--Update Data Page: Serves an HTML page for updating user data

POST 

--Register: Extracts user registration details from the POST data. Validates password confirmation. Checks if the username already exists in the database. Inserts new user details into the database if validation passes. Redirects to the login page upon successful registration.

--Login: Extracts login credentials from the POST data. Validates the credentials against the database. Sets a cookie and redirects to the logged-in page if validation passes (still not working when logging out). Responds with an error if user doesnt exist.

--Update Data: Checks for a valid username cookie. Extracts updated user data from the POST data. Validates password confirmation. Updates user details in the database if validation passes. Redirects to the logged-in page upon successful update.

structure:

-backend
--config.py: creds of the DB
--db.py: connection to the DB and initilizing the table if it doesnt exist
--server.py: the server handeling the get/post requests
--test.py: tests some get/post requests of the server
-frontend
--html
---login.html : the login form
---register.html : the register form
---profile.html : redirect page once succesful log in
---update_data.html : form to update the names and password of the logged in user


TO RUN THE SERVER:

head in the backend folder and run : server.py
and add the credentials to your own DB
