# -------------------------------------------------------------------------
# Made with LOVE By Gilad Gershon
# Licensed under the MIT License.
# --------------------------------------------------------------------------
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import codecs
from string import Template
from decouple import config
import os

smtp_server  = config("SMTP_SERVER")
port         = config("SMTP_PORT")
sender_email = config("SENDER_EMAIL")
password     = config("SMTP_PASSWORD")


# Create a secure SSL context
context = ssl.create_default_context()
server = smtplib.SMTP(smtp_server,port)
server.ehlo()
server.starttls(context=context) # Secure the connection
server.ehlo() 
server.login(sender_email, password)


      
def sendemail(student_email, student_name, course_name, cert_file):
  if config("USE_SHORT_COURSE_NAME") is True:
    course_name = course_name[0 : int(config("SHORT_COURSE_NAME_NUM_LETTERS"))]
    br = ''
  else:
        br = '<br>' #incase the course name is not short, print the course name in new line in the email.
  # Try to log in to server and send email
  try:

      message = MIMEMultipart("alternative")
      message["Subject"] = f"Certifiaction of completion: {course_name}" #Email Subject
      message["From"] = sender_email
      message["To"] = student_email                                             #Student Email

      

      # Plain text in case that the client can't read HTML
      text = f"""\
    Hi {student_name}, Congratulation of completion the course {course_name}!
    We happy to attach to this email the certification of completion
  """

      template = codecs.open("./static/files/email_template.html", 'r')
      extract = Template(template.read())
      html =  extract.substitute(student_name=student_name, course_name=course_name, br=br)

        # Open PDF file in binary mode
      with open(cert_file, "rb") as attachment:
          # Add file as application/octet-stream
          # Email client can usually download this automatically as attachment
          part = MIMEBase("application", "octet-stream")
          part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
      encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
      part.add_header(
          "Content-Disposition",
          f"attachment; filename= {cert_file}",
        )
      
      # Turn these into plain/html MIMEText objects
      part1 = MIMEText(text, "plain")
      part2 = MIMEText(html, "html")
      



      # Add HTML/plain-text parts to MIMEMultipart message
      # The email client will try to render the last part first
      message.attach(part1)
      message.attach(part2)
      message.attach(part)

      server.sendmail(
          sender_email, student_email, message.as_string()
      )

  except Exception as e:
    #in case of error - remove cert file
    os.remove(cert_file) 
    print(e)

    
    
    
def memberemail(member_email, course_name):
  if config("USE_SHORT_COURSE_NAME") is True:
        course_name = course_name[0 : int(config("SHORT_COURSE_NAME_NUM_LETTERS"))]

  # Try to log in to server and send email
  try:
      message = MIMEMultipart("alternative")
      message["Subject"] = f"Certifiaction of completion: {course_name}"
      message["From"] = sender_email
      message["To"] = member_email

      # Plain text in case that the client can't read HTML
      text = f"""\
    Hi,
    we just want to let you know that we finish to send the certification of the course {course_name}.
  """

      # Turn these into plain/html MIMEText objects

      message.attach(MIMEText(text, "plain"))
      
      server.sendmail(
          sender_email, member_email, message.as_string()
      )

  except Exception as e: 
    print(e)
  finally:
    #LOGOUT SMTP server
    server.quit() 