import unittest
import smtplib
from unittest.mock import patch, mock_open
from email.mime.multipart import MIMEMultipart

import index

class TestEmailSender(unittest.TestCase):
    @patch('smtplib.SMTP')
    def test_sutup_smtp_server(self, mock_smtp):
        smtp_server = 'smtp.gmail.com'
        port = 587
        sender_email = 'sherzik99@gmail.com'
        password = 'test_password'

        server = index.setup_smtp_server(smtp_server, port, sender_email, password)

        mock_smtp.assert_called_with(smtp_server, port)
        server.starttls.assert_called()
        server.login.assert_called_with(sender_email, password)


    def test_create_email_message(self):
        sender_email = "test@example.com"
        to = "recipient@example.com"
        subject = "Test Subject"
        body = "Test Body"

        # Call the function
        msg = index.create_email_message(sender_email, to, subject, body)

        # Check if the message has the correct attributes
        self.assertEqual(msg['From'], sender_email)
        self.assertEqual(msg['To'], to)
        self.assertEqual(msg['Subject'], subject)
        self.assertIn(body, msg.as_string())

    @patch('index.open', new_callable=mock_open, read_data="Test Body")
    def test_attach_file_to_email(self, mock_file):
        msg = MIMEMultipart()
        file_path = "image.jpg"

        # Call the function
        index.attach_file_to_email(msg, file_path)

        # Check if the file was attached to the message
        self.assertTrue(msg.is_multipart())
        self.assertEqual(len(msg.get_payload()), 1)

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        server = mock_smtp.return_value
        sender_email = "test@example.com"
        to = "recipient@example.com"
        msg = MIMEMultipart()

        # Call the function
        index.send_email(server, sender_email, to, msg)

        # Check if the email was sent
        server.sendmail.assert_called_with(sender_email, to, msg.as_string())
        server.quit.assert_called()

    def test_handle_email_error(self):
        # Call the function
        try:
            raise Exception("Test Exception")
        except Exception as e:
            index.handle_email_error(e)

if __name__ == '__main__':
    unittest.main()
