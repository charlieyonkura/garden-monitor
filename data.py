import time
import os

time_delay = 10 # in minutes
days = 365
counter = 0
total_img_count = days * 1440 / time_delay

def take_picture():
	path = "/home/pi/Desktop/garden-monitor-new/static/images"
	image_name = 'image'
	
	global counter
	counter +=1
	
	if os.path.exists(path) == False:
		os.mkdir(path)

	data = "fswebcam " + path + "/" + image_name + (str)(counter) + ".jpg"
	os.system(data)
	
	
while counter < 5:
	
	take_picture()
	
	time.sleep(3) # in seconds
