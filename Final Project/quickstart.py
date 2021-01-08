#!/usr/bin/env python
# coding: utf-8

# In[165]:


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import json
from datetime import datetime
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib  
from email import encoders
from email.mime.text import MIMEText
import base64


# In[166]:



# If modifying these scopes, delete the file token.pickle.
SCOPES = 'https://mail.google.com/'
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service
    service = build('gmail', 'v1', credentials=creds)
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
if __name__ == '__main__':
    main()


# In[167]:


#CREATE, SEND EMAIL
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
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}
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
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    return message


# In[168]:


#GOOGLE DRIVE API
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
if gauth.credentials is None:
    gauth.LocalWebserverAuth() # Authenticate if they're not there
elif gauth.access_token_expired:
    gauth.Refresh() # Refresh them if expired
else: 
    gauth.Authorize() # Initialize the saved creds
gauth.SaveCredentialsFile("mycreds.txt") # Save the current credentials to a file
drive = GoogleDrive(gauth)


# In[169]:


#UPLOAD FILE SETTING
def newFolder():
    file_list = drive.ListFile({"q": "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for file1 in file_list:
        print('Your existing folders: '+file1['title'])
    createFolder=input('Do you want to create a new folder? No or Yes')
    folderName=input('Enter folder name: ')
    if(createFolder=='Yes' or createFolder=='yes'):
        folder = drive.CreateFile({'title' : folderName, 'mimeType' : 'application/vnd.google-apps.folder'})
        folder.Upload()
        return folder['id']
    else:
        for file1 in file_list:
            if file1['title']==folderName:
                return file1['id'] 
def getPath():
    folder=newFolder() 
    path=input('Enter file path to upload:' )
    body=''
    entries = os.listdir(path)
    for entry in entries:
        pathN = r'{}'.format(path)
        pathN=pathN+'\\'+entry       
        fileLink=uploadFile(entry,folder,pathN)
        body+=entry+' has been uploaded at ' + fileLink+'\n'
    user=(service.users().getProfile(userId='me').execute())
    emailAddress=user['emailAddress']
    message= create_message(emailAddress,emailAddress,'Your files have been uploaded!',body)
    send_message(service,'me',message)
    print('Da gui email')


# In[170]:


#UPLOAD FILE
def uploadFile(entry,folder,path):
    print(entry,folder)
    time= datetime.now()
    timeName=time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    file1 = drive.CreateFile({'title': timeName+entry, 'parents': [{'id': folder}]})  # Create GoogleDriveFile instance with title 
    file1.SetContentFile(path) # Set content of the file from given path
    file1.Upload()
    return file1['alternateLink']
getPath()


# In[ ]:





# In[ ]:




