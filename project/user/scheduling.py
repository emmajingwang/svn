import schedule
import time
from .svn import svn

def task(account,email):
        
    schedule.every().day.at("13:17").do(svn,account,email)
    while True:
        schedule.run_pending()
        time.sleep(1)