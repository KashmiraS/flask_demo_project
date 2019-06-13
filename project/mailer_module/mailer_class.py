import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
#send back mail to

def send_mail(subject,user_name,mail_id,body):
    mail_body_object = MIMEMultipart('alternatief')
    mail_body_object['Subject'] = subject
    mail_body_object['From'] = 'PROJECT SYSTEM <bagwan.akib.64@gmail.com>'#from_adres
    mail_body_object['To'] =f'{user_name} <{mail_id}>'
    #text = body#"Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body, 'html')
    #part2 = MIMEText(html, 'html')

    mail_body_object.attach(part1)
    #mail_body_object.attach(part2)
    #boodskap = MIMEText("<h1>Hierdie is die boodskap gedeelte vanie epos</h1>", 'plain')
    boodskap = MIMEText("<h1>Project Management system.</h1>", 'html')
    mail_body_object.attach(boodskap)

    try:
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('oneadsakib@gmail.com','shashi11149')
        mail.sendmail('oneadsakib@gmail.com',mail_id,mail_body_object.as_string())
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
