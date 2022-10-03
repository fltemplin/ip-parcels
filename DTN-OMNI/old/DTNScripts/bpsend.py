import os
import subprocess
import time

start_time = time.time()
for filename in os.listdir("./"):
	#print "Sending file: " + filename
	send = subprocess.check_output(("bpsendfile","ipn:4.1","ipn:5.1", filename))
	time.sleep(1.1)
print("%s seconds" % (start_time))
#print("%s seconds" % (time.time() - start_time))
