
# MailBot
Tool to automatically email results from your Python scripts to your inbox as text or as a file attachment, storing the sender email account's password securely in the keychain.

## Overview

MailBot can be imported into Python projects to simplify integrating email sending into your scripts. When initializing MailBot, the class requires you to pass the desired sender email address and recipient email address as arguments. When invoking the send mail method, you can choose to send your results as an attached file, or as plaintext in the message body.

The use of this tool requires that you setup a free GMail account, and that this account has enabled the *'Allow Less Secure App Access'* setting (More on setup below). The password of the sender account is required to send mail from the command line - instead of hardcoding a sensitive password in code or storing it in memory, MailBot provides a quick method to securely provide and store the password in your system's keychain.


## Installation

This script must be run with Python3 - to my knowledge, the imported SMTP libraries required are not compatible with Python2.x.

*Required Packages:*

```
smtplib
email
argparse
keyring
```

Install Steps:

```
git clone https://github.com/allyomalley/MailBot.git
cd MailBot
sudo pip3 install -r requirements.txt
```

I have only tested this script on macOS and Linux - the code should work on a Windows machine, but I have not been able to test it.


## Setup

Before you can use MailBot, you'll need to have a GMail account that will be sending the emails setup. You can sign up for a free account [here](https://accounts.google.com/SignUp)

**IMPORTANT**

You *MUST* enable the sender account's *'Allow Less Secure App Access'* setting in order to use MailBot - Google's security measures will block account access from Python/other scripts by default otherwise. See more information [here](https://support.google.com/accounts/answer/6010255).

If your sender account has 2FA enabled, you will also need to change your settings to allow *'Sign in using App Passwords'.* You can see the steps [here](https://myaccount.google.com/lesssecureapps). When you are creating the app specific password, you can specify the 'Custom (Other)' app. You can then use the generated password instead of your account's password.

If you are still running into issues, you may need to try these two additional steps:

https://accounts.google.com/b/2/DisplayUnlockCaptcha
https://mail.google.com/mail/#settings/fwdandpop

Once your GMail account is setup, you need to configure MailBot's access to send emails from the account. In order to store the account's password in the keychain, you can run the script directly with the *-s* or *--store* flag like this:

```
python3 mailbot.py -s --sender mysenderaccount@gmail.com
```

You will then be prompted for the account's password - This prompt uses Python's 'getpass' module to handle the password more securely than passing it as an argument or otherwise typing it in. 

If you ever want to remove the password from the keychain, you can use the *-d* or *--delete* option like so:

```
python3 mailbot.py -d --sender mysenderaccount@gmail.com
```


## Usage

You can import MailBot into your other scripts like this:

```
import mailbot
```

(Make sure that the MailBot script is either located in the same directory, or that you've added it to your path)

Now, you can initialize a MailBot instance by providing your sender and desired recipient addresses:

```
bot = mailbot.MailBot("myrecipientemail@gmail.com", "mysenderaccount@gmail.com")
```

There are two methods for sending mail - *'sendMailWithData'*, and *'sendMailWithFile'*. Pass them the desired subject of the message, along with either the text for the body or the path of the file to be attached.

```
bot.sendMailWithData("Recon Scan Results", "hello\nfriend\n")
bot.sendMailWithFile("Recon Scan Results", "testmail.txt")
```

