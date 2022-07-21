# -------------------------------------------------------------------------
# Made with LOVE By Gilad Gershon
# Licensed under the MIT License.
# --------------------------------------------------------------------------

from flask import Flask, render_template, request
from webapp.requestprocessor import RequestsProcessor
app = Flask(__name__, static_folder="../static", template_folder="../templates")
import redis
import random
import string
from werkzeug.utils import secure_filename
from decouple import config


#Redis Connection
r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


#get letter num (see short course name on README file)
letters_num  = int(config("SHORT_COURSE_NAME_NUM_LETTERS"))

#Error message (Validation Failed)
error = [{'title': 'Opss..',
             'content': 'Something wrong, please check your form and try again.'},
            ]


#App route - index.html
@app.route("/")
def index():
    return render_template('index.html')




#Post request from certification form
@app.route("/api/entity", methods=["POST"])
def handler_entity_action():
 try:   
    action = request.args.get("action")
    params = {key: request.form.get(key) for key in request.form.keys()}     #Get Keys from form
    f = request.files['file']                                                #Get xlsx file
    file_name = f.filename                                                   #Set file name
    file_format = file_name.split(".",1)[1]                                  #Get file format (for validation)
    
    if action == "go": 
        if file_format == 'xlsx' or file_format == 'xls':                    #validate the file format, if the file format isnt excel file, return error and dont save the file
         #set parameters from trom the form
         member_email = params.pop("member_email")
         course_name = params.pop("course_name")
         course_dates = params.pop("course_dates")
         random_num = ( ''.join(random.choice(string.digits) for i in range(4)) )
         uniq_file_name = random_num+f.filename

         short_course_name = course_name[0 : letters_num]
         redis_hash_name = short_course_name + '_' + random_num
         path = "./studentlist/"
         f.save(path+ secure_filename(uniq_file_name)) #save the xslx file to ./studentlist folder
         
         #write the parameters to redis
         r.hmset(redis_hash_name, {
         "course_name": course_name,
         "short_course_name": short_course_name,
         "course_dates": course_dates,
         "member_email": member_email,
         "file_name": uniq_file_name,
         "finish": 'false',   
         "random_num": random_num 
         })
         
         #set redis hash name
         r.set('redis_hash_name', redis_hash_name)
         
         #Trigger the Request Processor
         RequestsProcessor().genrate_certifications()
         
         #Return OK with students number
         students_num = r.hget(redis_hash_name, "students_num")
         ok = [{'title': 'Great!',
             'content': 'We start to working on it,we have '+students_num+' students to proccess, when we finish we will send you an email as you mention: '+member_email},
            ]
         return render_template('index.html', messages=ok)       
 
 except Exception as error:
   #Return Error
  return render_template('index.html', messages=error)   



 
  



