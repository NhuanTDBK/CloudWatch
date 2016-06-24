import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("cloudwatchbkhn", "thivccontest")
#https://www.google.com/settings/security/lesssecureapps : Turn on

def message(subject, msg):
    # header  = "From: {}\n" % from_addr
    # header += "To: {}\n". format(','.join(to_addr_list))
    # header += "Cc: {}\n". format(','.join(cc_addr_list))
    header = "Subject: {}\n\n". format(subject)
    msg = header + msg
    return msg

def sendemail(msg):
	""" Send alert from list mails to other list mails
	"""	
	server.sendmail(["cloudwatchbkhn@gmail.com"], ["cloudwatchbkhn@gmail.com"], message("ALERT CLOUDWATCH", msg))
	
if __name__ == '__main__':
	msg = "CPU over 80%"
	sendemail(msg)
	server.quit()