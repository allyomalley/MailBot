import ssl
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
import argparse
import keyring
import getpass

class MailBot(object):

	def __init__(self, recipient, sender):
		self.recipient = recipient
		self.sender = sender

	def send(self, msg):
		port = 465
		smtp_server = "smtp.gmail.com"
		context = ssl.create_default_context()
		pw = self.fetchSenderPassword()
		if (pw == None):
			print('Failed to fetch password - are you sure it exists?')
			return
		try:
			with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
				server.login(self.sender, pw)
				server.sendmail(self.sender, self.recipient, msg.as_string())
		except smtplib.SMTPException as e:
			print(str(e))
		except Exception as e:
			print(e)

	def fetchSenderPassword(self):
		try:
			pw = keyring.get_password('MailBot', self.sender)
			return pw
		except Exception as e:
			print('Failed to fetch password for ' + self.sender)
			return None

	def setStaticFields(self, msg, subject):
		msg['From'] = self.sender
		msg['To'] = self.recipient
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = subject
		return msg

	def sendMailWithData(self, subject, data):
		if (data != ""):
			msg = MIMEText(data)
			msg = self.setStaticFields(msg, subject)
			self.send(msg)

	def sendMailWithFile(self, subject, file):
		if (len(file) > 0):
			msg = MIMEMultipart()
			msg = self.setStaticFields(msg, subject)
			part = MIMEBase('application', "octet-stream")
			with open (file, "r") as f:
				part.set_payload(f.read())

			part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(file))
			msg.attach(part)
			self.send(msg)

def storeSenderPassword(address):
	try:
		# Testing...
		keyring.set_password('MailBot', address, getpass.getpass())
		keyring.get_password('MailBot', address)
		print('Successfully stored password for ' + address)
	except Exception as e:
		print('Failed to store password for ' + address)
		pass

def deleteSenderPassword(address):
	try:
		keyring.delete_password('MailBot', address)
		print('Deleted password for ' + address)
	except Exception as e:
		print('Failed to delete password - are you sure it exists?')
		print(e)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="MailBot",
	)

	required_group = parser.add_mutually_exclusive_group(required=True)
	required_group.add_argument(
		'-s',
		'--store',
		action='store_true',
		dest='store',
		help='Store a sender account password.',
	)
	required_group.add_argument(
		'-d',
		'--delete',
		action='store_true',
		dest='delete',
		help='Delete a sender account password.',
	)

	parser.add_argument(
		'--sender',
		help='Email address of the sender account.',
		type=str,
		required=True
	)

	args = parser.parse_args()
	sender = args.sender
	if args.store:
		storeSenderPassword(sender)
	elif args.delete:
		deleteSenderPassword(sender)
