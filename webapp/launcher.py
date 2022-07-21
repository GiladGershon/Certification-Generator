import subprocess
import sys
import redis
from multiprocessing import Process

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


#lunch process
def task():
  redis_hash_name = r.get('redis_hash_name')
  rng = int(r.hget(redis_hash_name, 'students_num'))
  count =0
  print('we have '+str(rng)+' students to process')
  for x in range(rng):
      count +=1
      if count == rng:
          r.hset(redis_hash_name, 'finish', 'true')
      p = subprocess.Popen([sys.executable, 'webapp/process.py'])
      p.wait()
      
# entry point
if __name__ == '__main__':
    # create a process
    process = Process(target=task)
    # run the process
    process.start()
    print('launcher.py get the job and lanuch a proccess!')
    process.join()

