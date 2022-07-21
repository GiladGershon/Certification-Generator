# -------------------------------------------------------------------------
# Made with LOVE By Gilad Gershon
# Licensed under the MIT License.
# --------------------------------------------------------------------------

import pandas as pd
import itertools 
import subprocess
from flask import request
import sys
import os
import redis
from multiprocessing import Process

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)



class RequestsProcessor:     
  @staticmethod
  def genrate_certifications():
    
    redis_hash_name = r.get('redis_hash_name')
    path = "./studentlist/"

   ###Date format manipulation
   
    date = r.hget(redis_hash_name, 'course_dates')
    start_month = date[3:5] 
    end_month = date[16:18]
    start_year = date[6:10]
    end_year =  date[19:23]
      
    #build dates string base on some rules:
    if start_year != end_year:                                                            #The course dates are cross-year (DD/MM/YYYY - DD/MM/YYYY)
      newdate = date
    elif start_month == end_month:                                                        #The course is on the same month and the same year (DD-DD/MM/YYYY)
      newdate = date[0:2]+'-'+date[13:15]+'/'+date[3:5]+'/'+date[6:11]
    elif start_month != end_month:                                                        #The course is on the same year but not on the same month (DD/MM-DD/MM/YYYY)
      newdate = date[0:2]+'/'+start_month+'-'+date[13:15]+'/'+end_month+'/'+date[6:11]
    r.hset(redis_hash_name, "course_dates", newdate) #PUT new date after formating them
      
    #Write students to redis:
    form_name = pd.read_excel(path+r.hget(redis_hash_name, "file_name")) #import the name file
    name_list  = form_name['name'].to_list() #convert name column to list
    email_list = form_name['email'].to_list() #convert email column to list
    r.hset(redis_hash_name, 'students_num', len(name_list)) #Write to redis the number of students we have to proccess
    random_num = r.hget(redis_hash_name, "random_num")      #Get the proccess random num
      
    for (n, e) in itertools.zip_longest(name_list, email_list):
      r.lpush('name_list_'+random_num, n)
      r.lpush('email_list_'+random_num, e) 
   
    os.remove('./studentlist/'+r.hget(redis_hash_name, 'file_name')) #delete student file (we dont need the file anymore, all the data on redis.)
    r.set('process', 0)                                              #set proccess=0
    p = subprocess.Popen([sys.executable, 'webapp/launcher.py'])       #Triger luncher.py
     


    
    
    
