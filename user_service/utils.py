from datetime import datetime
import time
import random

def create_cert_number():
    return str(random.randrange(1, 1000000)).rjust(6, '0')
        
def create_timestamp_ttl(second=180):
    return int(time.mktime(datetime.now().timetuple())) + second