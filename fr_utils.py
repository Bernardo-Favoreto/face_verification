#from merge import*
import os
import cv2
import pickle
from keras.preprocessing.image import img_to_array
import numpy as np
import face_recognition 
from imutils.video import VideoStream
import time
import imutils

known_face_encodings = []
known_face_names = []
def update_or_create_known_people():
    """
    This will update the names and encodings pickle file.
    """
    for name in os.listdir('images/known_people'):
        identity = ''.join(filter(str.isalpha, name[:-4]))
        img = face_recognition.load_image_file('images/known_people/' + str(name)) # This will load the image file
        encoded_img = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoded_img)
        known_face_names.append(identity)
    save_pickle(known_face_names, "names.pickle")
    save_pickle(known_face_encodings, "encodings.pickle")
    print("Pickle files sucessfuly generated/updated!")


def save_pickle(item, pickle_name):
    pickle_out = open(pickle_name, "wb") #Write bytes
    pickle.dump(item, pickle_out)
    pickle_out.close()

def load_pickle(pickle_file):
    pickle_in = open(pickle_file, "rb") #Read bytes
    pickle_file = pickle.load(pickle_in)
    return pickle_file

def avg_array(list_of_arrays):
    b = np.zeros(list_of_arrays[0].shape)
    for array in list_of_arrays:
        b += array
    return b/len(list_of_arrays)


"""
If you are using for the first time, or have updated your images folder and want to update your pickle files,
simply uncomment the command below and run from your command prompt "python utils.py"
The next time you run face_rec_vX your pickle files will be correctly loaded (i.e. the updated versions)
NOTE: don't forget to comment it again after using!
"""
#update_or_create_known_people()



def anti_spoof(frame, out_list, confidence1, protoPath, modelPath,
                model, le, net, len_threshold):



    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > confidence1:
            # compute the (x, y)-coordinates of the bounding box for
            # the face and extract the face ROI
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the detected bounding box does fall outside the
            # dimensions of the frame
            startX = max(0, startX)
            startY = max(0, startY)
            endX = min(w, endX)
            endY = min(h, endY)

            # extract the face ROI and then preproces it in the exact
            # same manner as our training data
            face = frame[startY:endY, startX:endX]
            face = cv2.resize(face, (32, 32))
            face = face.astype("float") / 255.0
            face = img_to_array(face)
            face = np.expand_dims(face, axis=0)

            # pass the face ROI through the trained liveness detector
            # model to determine if the face is "real" or "fake"
            preds = model.predict(face)[0]
            j = np.argmin(preds) # This was np.argmax originally
            label = le.classes_[j]
            return label



            


def face_rec(frame, known_face_encodings, known_face_names,
                face_locations, face_encodings, face_names,
                process_this_frame, face_encoded, len_threshold):

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video

        face_locations = face_recognition.face_locations(rgb_small_frame) # NOTE: this
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) # NOTE: and this are commands that make the code slower
        face_names = []

    #Exception handling is necessary in case a face is not found (for whatever reason)
        try:
            matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
            name = "Unk"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            try:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
                best_match_index = np.argmin(face_distances)
            except IndexError:
                pass
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                return name
        except IndexError:
            pass
        

    process_this_frame = not process_this_frame

