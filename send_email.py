import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def create_message(sender, to, subject, message_text):
  """Create a message for an email.
Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
def notif():
  notification('pythonsslcheck@gmail.com', 'parteg7@gmail.com', 'Scuccess!', 'Mr. Herold launched my project!')

def send_message(service, user_id, message):
  """Send an email message.
Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
    print('Message Id: {}'.format(message['id']))
    return message
  except:
    print ('An error occurred')

def notification(sender, to, subject, notification):
  #Sender is the sender email, to is the receiver email, subject is the email subject, and notification is the email body message. All the text is str object.
  SCOPES = 'https://mail.google.com/'
  message = create_message(sender, to, subject, notification)
  creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
  if os.path.exists('token.json'):
      creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.json', 'w') as token:
          token.write(creds.to_json())
  service = build('gmail', 'v1', credentials=creds)
  send_message(service, sender, message)