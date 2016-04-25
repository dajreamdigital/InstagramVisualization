# InstagramVisualization
Visualizing Instagram data and Filter Recommendation for Instagram images.

## Instructions for running the app :

### Install virtualenv
+ $ sudo su # You probably need to be root to do this.
+ $ apt-get install python-virtualenv


### Initialize virtualenv and install dependencies
+ $ cd app
+ $ virtualenv venv
+ $ . venv/bin/activate
+ $ pip install -r requirements.txt

### Copy Image Classify file to TensorFlow root inside venv
+ $ cp my_classify_image.py venv/lib/python2.7/site-packages/tensorflow/models/image/

### Run the application
+ $ python index.py

+ Go to http://127.0.0.1:5000/ to see the running app.
