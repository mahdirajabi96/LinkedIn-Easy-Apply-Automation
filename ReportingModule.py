# import smtplib

# server = smtplib.SMTP('smtp.gmail.com', 587)

# #Next, log in to the server


# #Send the mail
# msg = "Hello!" # The /n separates the message from the headers
# server.sendmail("you@gmail.com", "udaybhaskar578@gmail.com", msg)
EmailID = '' #your gmail id
Password = ''#your gmail password
Recipient = EmailID

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
