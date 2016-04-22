import csv
import pdb
import subprocess as sp
import urllib
import os
import time
import imghdr

def retrieve_class(url):
    # url = "https://upload.wikimedia.org/wikipedia/commons/5/5d/RedRoo.JPG"
    i=1

    model_path = 'imagemodel'
    classifier_path = 'venv/lib/python2.7/site-packages/tensorflow/models/image/my_classify_image.py'

    print "Here", url
    filename = "static/images/test.jpg"
    print "Filename",filename
    urllib.urlretrieve(url, filename)
    file_type = imghdr.what(filename)
    print file_type
    if file_type == 'jpeg':
        temp = sp.Popen(['python', classifier_path,  '--model_dir', model_path, '--image_file', filename], stdout=sp.PIPE, stderr=sp.PIPE)
        out, err = temp.communicate()
        print err
        results = out.split('\n')[-7:-1]
        image_classes = results[0::2]
        class_probs = results[1::2]

        for j in range(len(class_probs)):
            class_probs[j] = class_probs[j].split('=')[1][1:-1]

        print 'Image ' + str(i) + ' top class: ' + image_classes[0] + '\t' + class_probs[0]
        return image_classes[0].replace(',','|').replace('(','|').replace(';','|').split('|')[0]
