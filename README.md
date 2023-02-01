# This is a project for Information and Communications Technology infrastructure management course 2022-2023 on Wroclaw University of Science and Technology

## Project Subject: A simple tool for monitoring ssl certificate's (both local and remote) expiry dates with email notifications
## Project Author: Bartosz Maslicki

### How does it work:

My project works with the intention that it's going to run 24/7 and check the certificates expiry dates ones a day and has 3 possible notifiactions: 
- when a certificate will expire in 31 days
- when a certificate will expire in 14 days
- when a certificate has expired.

The project sends the notifications to an email address that is specified when starting the app.
Example:
```
py main.py yourEmail@gmail.com
```
The credentials.json holds credentials to GmailAPI workspace for the app to be authorized when starting the app the first time. After that - every other startup shouldn't require signing in to the account that sends notifications (in my case it's pythonsslchecker@gmail.com) because the token is stored in token.json file (if there are any errors with sending the email delete the token.json file and authorize again the credentials for pythonsslcheck account are in the .txt file).

In file **pages.csv** provide a list of page URLs whose SSLs you want to check (use page.com or www.page.com format)

In file **ssls.csv** provide a list of certificates files paths that you want to check (files should be in base64 format [.crt and .pem satisfy that requirement])

***If no page is specified in pages.csv then the app will simply ignore the remote check part. Same goes for the local check***

### How to make it work:

In order to make it work you need to install some packages after you've pulled the project from GitHub. You can do it using those commands:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install pyopenssl
```
If you need any other packages your IDE is most probably going to highlight them for you.

If you want to use a different gmail account that sends the notifications, you'll need to create a new account for it and follow this tutorial: [GmailAPI setup with python notification examples](https://towardsdatascience.com/automatic-notification-to-email-with-python-810fd357d89c).

The app is mainly made for Linux machines (of course it still works on Windows, it's just a little more unstable) because it uses a scheduler package to make it run ones a day. With this in mind you should start it using a different app to make it work in the background for example:
```
nohup python3.10.2 main.py &
```

