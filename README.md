The project is built with python Flask web framework and is deployed to Azure service at the following address:

http://christmas-songs-website.azurewebsites.net/

The website allows a user to create an account, log into a personal account, check the list of all available songs, add/remove songs to the personal playlist, watch the song video and associated lyrics.

-------------------------------------------------------------

Signup page checks the following:

- whether the entered username is already in use and shows the corresponding error message;
- whether the entered email address is already in use and shows the corresponding error message;
- whether the password is correctly entered twice;
- once all the necessary details have been filled in, the user gets redirected to the 'Log in' page with the message of the account creation.

-------------------------------------------------------------

Login page allows the user to log in using the username and password.

-------------------------------------------------------------

Account page provides the following features:

- after the user has logged in, a personalized "Welcome to your account, {username}" message is shown;
- shows a list of songs the user previously added from the 'All songs' page;
- allows to check the song page by clicking on the song name;

-------------------------------------------------------------

All songs page consists of the following:

- provides the list of songs added by the website admin to the database;
- allows the user to add/remove a particular song to the account;
- if the song is already added to the user's account, the button 'Remove' will be shown;
- if the song is not yet added to the user's account, the button 'Add' will be shown;
- it is possible to check the song page by clicking on its title;

-------------------------------------------------------------

Song page:

- provides the song title, Youtube video, lyrics.