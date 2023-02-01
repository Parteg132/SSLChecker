from datetime import datetime
import OpenSSL
import ssl

import schedule
import time
import sys

import send_email

n = len(sys.argv)
if n != 2:
  print("Please provide an email you want to send notifications to.")
  exit()

EMAIL = str(sys.argv[1])
#this is the email that the notification will be sent to
URL_FILE_PATH = "pages.csv"
#in the .csv file provide the urls of pages which ssls you want to monitor (in format www.<page-name>.com or <page-name>.com)
SSL_FILE_PATH = "ssls.csv"
#file with local ssl certificates (must be .pem or .crt format) to be checked

def check_send_remote(t, p):
  today = datetime.today().date()
  d = (t - today).days
  if d == 31:
    send_email.notification('pythonsslcheck@gmail.com', EMAIL, 'Notification - Cerificate expiry of {}'.format(p), 'Certificate of page: {} will expire in 31 days!'.format(p))
    return 31
  elif d == 14:
    send_email.notification('pythonsslcheck@gmail.com', EMAIL, 'Notification - Cerificate expiry of {}'.format(p), 'Warning! Certificate of page: {} will expire in 14 days!'.format(p))
    return 14
  elif d == 0:
    send_email.notification('pythonsslcheck@gmail.com', EMAIL, 'Notification - Cerificate expiry of {}'.format(p), 'Warning!!! Certificate of page: {} has expired!!!'.format(p))
    return 0
  else:
    return 1

def check_send_local(t, f):
  today = datetime.today().date()
  d = (t - today).days
  if d == 31:
    send_email.notification('pythonsslcheck@gmail.com', EMAIL, 'Notification - Local cerificate expiry', 'Certificate from file: {} will expire in 31 days!'.format(f))
    return 31
  elif d == 14:
    send_email.notification('pythonsslcheck@gmail.com', EMAIL, 'Notification - Local cerificate expiry', 'Warning! Certificate from file: {} will expire in 14 days!'.format(f))
    return 14
  elif d == 0:
    send_email.notification('pythonsslcheck@gmail.com', EMAIL, 'Notification - Local cerificate expiry', 'Warning!!! Certificate from file: {} has expired!!!'.format(f))
    return 0
  else:
    return 1

def notif():
  send_email.notification('pythonsslcheck@gmail.com', 'parteg7@gmail.com', 'Scuccess!', 'Mr. Herold launched my project!')

def remote_ssl_date(p):
  cert=ssl.get_server_certificate((p, 443))
  x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
  bytes=x509.get_notAfter()
  timestamp = datetime.strptime(bytes.decode('utf-8'), '%Y%m%d%H%M%S%z').date()
  return timestamp

def local_ssl_date(file):
  with open(file, "r") as cert_file:
    cert_text = cert_file.read()
  x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_text)
  bytes=x509.get_notAfter()
  timestamp = datetime.strptime(bytes.decode('utf-8'), '%Y%m%d%H%M%S%z').date()
  print("Expiry date of file {} is:".format(file) ,timestamp)
  return timestamp



def main():
  try:
      f = open(URL_FILE_PATH, "r")
  except:
      f = open(URL_FILE_PATH, "w")
      f = open(URL_FILE_PATH, "r")
    
  fileLines = f.readlines()
  f.close()
  if len(fileLines) == 0:
    print("No pages specified in pages.csv file")
  else:
    for p in fileLines:
      p = p.strip()
      timestamp = remote_ssl_date(p)
      check_send_remote(timestamp, p)
  notif()

  try:
      f = open(SSL_FILE_PATH, "r")
  except:
      f = open(SSL_FILE_PATH, "w")
      f = open(SSL_FILE_PATH, "r")
    
  fileLines = f.readlines()
  f.close()
  if len(fileLines) == 0:
    print("No certificates specified in ssls.csv file")
  else:
    for c in fileLines:
      c = c.strip()
      timestamp = local_ssl_date(c)
      check_send_local(timestamp, c)

if __name__ == "__main__":
  schedule.every().day.at("17:00").do(main)
  while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute