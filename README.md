# Certification Generator
The app allows educational organizations to send emails with a graduation certificate to students attached as a PDF file.

GUI\
<img
  src="https://giladstaticweb.blob.core.windows.net/public/gui.gif"
  alt="GIF"
  title="GUI"
  style="display: inline-block; margin: 2 auto; width: 800px">


CERTIFICATION\
<img
  src="https://giladstaticweb.blob.core.windows.net/public/certex.png"
  alt="GIF"
  title="GUI"
  style="display: inline-block; margin: 2 auto; width: 800px">


1. Upload an Excel file with the student's name and email.
2. Choose course name and dates
3. Click Go
4. The app takes the student's full name, the course name, and dates and generates certification by Docx template, and saves a new docx file for each student.
5. The app converts the docx to pdf and sends the certification as an attachment file with a friendly email to the students.
6. When all the mail sends, the member gets an email that the job is done.

Flow

![flow](https://giladstaticweb.blob.core.windows.net/public/pics.png)

Email\
<img
  src="https://giladstaticweb.blob.core.windows.net/public/emails.png"
  alt="GIF"
  title="GUI"
  style="display: inline-block; margin: 2 auto; width: 1200">


## Installation:
The app has two versions:
1. Docker Container
2. Run on your local machine

### Set the .env file
- If you wish to run the app on a docker container you can modify the .env:\
for the docker container set DOCKER_OR_LOCAL to "docker"\
If you wish to run the app on a machine set DOCKER_OR_LOCAL to "local"
- set the SMTP credentials on the .env file: SMTP SERVER, SMTP PORT, SENDER EMAIL and SMTP PASSWORD.


### Docker Container Installation:
(You need [Docker](https://www.docker.com/get-started/) installed)
1. Set the .env file to run docker (DOCKER_OR_LOCAL="docker")
2. Edit the email template and the certification template:\
Email Template: static/files/email_template.html\
Certification Docx template: static/files/certification_template.docx

3. build the image
```bash
docker build -t certification-gen:latest .
```
4. run the image

```bash
docker run -d -p 80:80 certification-gen:latest
```


### Local Machine:
Requirements:
1. [Python 3.8+](https://www.python.org/downloads/)
2. [Redis](https://redis.io/docs/getting-started/) 

1. Install requirements
```bash
pip install -r requirements.txt
```
2. Set the .env file to run local (DOCKER_OR_LOCAL="local")
3. Start the Redis server
3. Run
```bash
Python run.py webapp
```



## License
[MIT](https://choosealicense.com/licenses/mit/)
