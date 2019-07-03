# USAGE
# python liveness_demo.py

# import the necessary packages
from imutils.video import VideoStream
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
from fr_utils import*

confidence1 = 0.6

# Load the network
protoPath = os.path.sep.join(['face_detector', "deploy.prototxt"])
modelPath = os.path.sep.join(
    ['face_detector', "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# Load the model
model = load_model('liveness.model')

# Load the pickle lists
known_face_encodings = load_pickle("encodings.pickle")  # List w/ encodings
known_face_names = load_pickle("names.pickle")  # List w/ names
le = pickle.loads(open('le.pickle', "rb").read())


# Initialize the variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
flag = True
face_encoded = []
vs = VideoStream(src=0).start()
time.sleep(2.0)
spoof_list = []
name_list = []
id_threshold = 10
spoof_threshold = 30

flag = True
flag_2 = True



while flag == True:
    while len(spoof_list) < spoof_threshold:
        frame_spoof = vs.read()
        spoof = anti_spoof(frame_spoof, [], confidence1,
                        protoPath, modelPath, model, le, net)
        if spoof != None:
            spoof_list.append(spoof)
    if spoof_list.count('real') > 0.2*spoof_list.count('fake'):
        print("Spoof detection test passed")
        while flag_2 == True:
            frame_id = vs.read()
            name = face_rec(frame_id, known_face_encodings,
                        known_face_names, face_locations, face_encodings,
                        face_names, process_this_frame, face_encoded)
            if name != None: 
                name_list.append(name)                  
            if len(name_list) >= id_threshold:
                print("Welcome {}!".format(max(set(name_list), key=name_list.count)))
                flag_2 = False
        flag = False
    else:
        print("Spoof attempt detected.")
        flag = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stop()

