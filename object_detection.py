import csv
import pdb
import subprocess as sp
import urllib
import os
import time
import imghdr

file1 = open('./data/NewYork.csv', 'rb')
file2 = open('./data/NewYork_object_detection_final.csv', 'ab')

reader = csv.reader(file1)
writer = csv.writer(file2)

i = 1

model_path = './mymodel'
classifier_path = './tensorflow/models/image/imagenet/my_classify_image.py'

for row in reader:
	if i==1:
		writer.writerow(row + ['image_class1', 'prob1', 'image_class2', 'prob2', 'image_class3', 'prob3'])
		flag = False
	elif i>23570 and row[3] != 'Normal':
		filename = row[11].split('/')[-1]
		urllib.urlretrieve(row[11], filename)
		file_type = imghdr.what(filename)
		if file_type == 'jpeg':
			temp = sp.Popen(['python', classifier_path, '--model_dir', model_path, '--image_file', filename], stdout=sp.PIPE, stderr=sp.PIPE)
			out, err = temp.communicate()
			results = out.split('\n')[-7:-1]
			image_classes = results[0::2]
			class_probs = results[1::2]

			for j in range(len(class_probs)):
				class_probs[j] = class_probs[j].split('=')[1][1:-1]

			print 'Image ' + str(i) + ' top class: ' + image_classes[0] + '\t' + class_probs[0]
			writer.writerow(row + [image_classes[0], class_probs[0], image_classes[1], class_probs[1], image_classes[2], class_probs[2]])

		removeRetryCount = 0
		while removeRetryCount < 3:
			time.sleep(1) # try to sleep to make the time for the file not be used anymore
			try:
				os.remove(filename)
				break
			except:
				print 'exception when trying to remove file: ' + filename
				removeRetryCount += 1
	i += 1


# pdb.set_trace()