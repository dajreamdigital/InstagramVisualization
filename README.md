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

##Install Tensorflow
### Ubuntu/Linux 64-bit, CPU only:
(tensorflow)$ pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.8.0-cp27-none-linux_x86_64.whl

### Ubuntu/Linux 64-bit, GPU enabled. Requires CUDA toolkit 7.5 and CuDNN v4.  For other versions, see "Install from sources" below.
(tensorflow)$ pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.8.0-cp27-none-linux_x86_64.whl

### Mac OS X, CPU only:
(tensorflow)$ pip install --upgrade https://storage.googleapis.com/tensorflow/mac/tensorflow-0.8.0-py2-none-any.whl

## Copy Image Classify file to TensorFlow root inside venv
+ $ cp my_classify_image.py venv/lib/python2.7/site-packages/tensorflow/models/image/

## Run the application
+ $ python index.py

+ Go to http://127.0.0.1:5000/ to see the running app.
