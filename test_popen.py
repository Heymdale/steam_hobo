import subprocess as sp
import time

def subproc_func():
    with sp.Popen(['ping', '-c', '10', '8.8.8.8']):
        print('something')
        sp.call(['killall', 'ping'])
        time.sleep(60)



subproc_func()
print('something2')
