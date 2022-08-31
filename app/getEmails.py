import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from table import Table


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Lists the user's Gmail messages.
    """
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

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        msg_response = service.users().messages()
        results = msg_response.list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
    

        if not messages:
            print("No messages found.")
        else:
            print("Message snippets:")

            table = Table()

            # if table is created
            if table.create_table():
                for message in messages:
                    msg_dict = msg_response.get(userId='me', id=message['id']).execute()
                    msg_headers = msg_dict['payload']['headers']

                    # get from email from email message header
                    msg_from = filter(lambda hdr: hdr['name'] == 'From', msg_headers)
                    msg_from = list(msg_from)[0]
                    print(msg_from.get('value'))

                    # get subject from email message header
                    msg_subject = filter(lambda hdr: hdr['name'] == 'Subject', msg_headers)
                    msg_subject = list(msg_subject)[0]
                    print(msg_subject.get('value'))

                    # get date from email message header
                    msg_date = filter(lambda hdr: hdr['name'] == 'Date', msg_headers)
                    msg_date = list(msg_date)[0]
                    print(msg_date.get('value'))

                    email, subject, date_received = (
                        msg_from.get('value', ''), 
                        msg_subject.get('value', ''), 
                        msg_date.get('value', '')
                    )

                    # remove (UTC) from date_received string
                    received_date_replaced = date_received.replace("(UTC)", "")

                    # check data already exists
                    # if not create email data
                    if not table.check_row_exists(email, subject, received_date_replaced):
                        table.create_email(email, subject, received_date_replaced)

                # close table cursor and connection
                table.closeConnection()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()