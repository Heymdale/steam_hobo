import subprocess as sp
import time

with sp.Popen(['ping', '-c', '10', '8.8.8.8']) as proc2:
    print('something')
    time.sleep(2)
    sp.call(['killall', 'ping'])
print('something2')

sp.Popen(['ping', '-c', '10', '8.8.8.8'])
print('something3')
time.sleep(2)
print('something4')