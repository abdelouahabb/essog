import smtplib

def send_email(client, link, pin):
	to = client
	gmail_user = 'alabdelouahab@gmail.com'
	gmail_pwd = 'miawmiaw'
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