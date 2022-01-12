from rq import Connection, Queue
from datetime import datetime, timedelta
from redis import Redis
from deneme import funct# added import!
redis_conn = Redis()
q = Queue(connection=redis_conn)
job = q.enqueue_in(timedelta(seconds=10), funct)

#scheduler.schedule(
  #  scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
   # func=funct,                     # Function to be queued               
    #interval=45,                   # Time before the function is called again, in seconds 
#)