import smtplib
'''
sadly this is blocking, i try to make it unblocking.
this will use your gmail account to send emails, you are limited to http://support.google.com/a/bin/answer.py?hl=en&answer=166852
'''
def send_email(client, link, pin):
	to = client
	gmail_user = 'emailerdz@gmail.com'
	gmail_pwd = 'QwertY1234' #thanks gmail for free accounts ;)
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Recuperation du mot de passe \n'
	msg = header + '\n Veuillez cliquer sur le lien http://localhost:8000/reset/{0} , \nLe code PIN est {1} \n\n'.format(link, pin)
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done!'
	smtpserver.close()
