import datetime
import time

start_time = datetime.datetime.now()
start_next = start_time + datetime.timedelta(hours=2.45)
print(start_time)
print(start_next)
diff = start_time - start_next
print(diff // datetime.timedelta(seconds=1))
time.sleep(diff)
print('Finish')
# while datetime.datetime.now() < start_next:
#     print('wait 30 sec')
#     time.sleep(30)
# print('Finish at ', datetime.datetime.now())
