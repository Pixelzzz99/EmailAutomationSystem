import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders 

def setup_smtp_server(smtp_server, port, sender_email, password):
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)
    return server

def create_email_message(sender_email, recipient_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    return message

def attach_file_to_email(msg, file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
    msg.attach(part)

def send_email(server, sender_email, to, msg):
    text = msg.as_string()
    server.sendmail(sender_email, to, text)
    server.quit()
    print("Email sent successfully!")

def handle_email_error(error):
    print('Failed to send email:', error)

body = open('message.txt', 'r').read()

smtp_server = 'smtp.gmail.com'
port = 587
sender_email = 'sherzik99@gmail.com'
password = open('password.txt', 'r').read()
to = 'sherzik99@gmail.com'
subject = "Test Subject"
file_path = 'image.jpg'

server = setup_smtp_server(smtp_server, port, sender_email, password)
message = create_email_message(sender_email, to, subject, body)
attach_file_to_email(message, file_path)

try:
    send_email(server, sender_email, to, message)
except Exception as error:
    handle_email_error(error)



