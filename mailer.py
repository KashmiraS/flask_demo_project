import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
#send back mail to
mail_body_object = MIMEMultipart('alternatief')

mail_body_object['Subject'] = "MAIL SUBJECT"

mail_body_object['From'] = 'SENDER <bagwan.akib.64@gmail.com>'#from_adres

mail_body_object['To'] ='RECIVER <bagwan.akib.64@gmail.com>'
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"

html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
      <h2> Here is the <a href="http://www.python.org">link</a> you wanted.<h2>
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

mail_body_object.attach(part1)
mail_body_object.attach(part2)
#boodskap = MIMEText("<h1>Hierdie is die boodskap gedeelte vanie epos</h1>", 'plain')
boodskap = MIMEText("<h1>Hierdie is die boodskap gedeelte vanie epos</h1>", 'html')
mail_body_object.attach(boodskap)

try:
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('oneadsakib@gmail.com','shashi11149')
    mail.sendmail('oneadsakib@gmail.com','bagwan.akib@gmail.com',mail_body_object.as_string())
    print('MAIL SENT')
except smtplib.SMTPHeloError:
    print ('The server responded weird stuff to my login request, please try again')
except smtplib.SMTPAuthenticationError:
    #DEVELOPER SIDE
    print ('Your account name or password is incorrect, please try again using the correct stuff')
except smtplib.SMTPException:
    print('NO Internet')
except Exception as e:
    if str(e)=='[Errno 11001] getaddrinfo failed':
        print('MAIL PORT NOT WORKING or INTERNET PROBLEM')
    else:
        print('Unknown ERROR'+str(e)) 
