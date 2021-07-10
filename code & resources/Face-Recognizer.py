import cv2
import face_recognition as fr
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter.filedialog import askopenfilename
import pickle


#######################################################################
"""This is for the GUI interface to start"""

root = Tk()
root.geometry("600x350+300+100")
root.title("Face Recognition Based Attendance System")

########################################################################
""" This part is for deleting any information previously stored in this file.
        Such as results from previous use of this system"""

file = open("attendence.csv", "r+")
file.truncate(0)
file.close()

#########################################################################
""" Declaration of all the necessary global variables """

namelist = []

###############################################################
"""This function shows the welcome text and guidance in the user interface"""

def WelcomeGuide():
    lab1 = Label(root, text="Welcome to the Attendance System", font=("times",12, "bold")).place(x=180, y=100)
    lab1 = Label(root, text="Go to 'Options' to start camera or select an image.", font=8).place(x=120, y=125)
    lab1 = Label(root, text="Choosing 'Start camera' will open the webcam and analyze frames.", font=8).place(x=75, y=150)
    lab1 = Label(root, text="Press 'Esc' to close camera.", font=8).place(x=190, y=175)
    lab1 = Label(root, text="Choosing 'Select Image' will offer user to select an image and analyze it.", font=8).place(x=55,
                                                                                                              y=200)
    lab1 = Label(root, text="Check the Output in 'attendence.csv' file.", font=8).place(x=160, y=225)

#########################################################################
"""This function creates the menubar"""


def Menubar():
    menulist1 = Menu()
    menulist2 = Menu()

    menulist1.add_command(label="Select Image", command=SelectImage)
    menulist1.add_command(label="Start WebCam", command=faceRecognition)
    menulist2.add_cascade(label="Options", menu=menulist1)
    root.config(menu=menulist2)

def SelectImage():

    # loading the previously encoded face's encoding values

    file = open("knownencoding.txt", "rb")
    knownEncodings = pickle.load(file)
    file.close()

    # Loading the name of the person in the image that has been used for encoding

    file = open("names.txt", "rb")
    imagenames = pickle.load(file)
    file.close()

    # Asking the user to select an image from the storage

    fname = askopenfilename()
    img = cv2.imread(fname)

    # Resizing image to perform operations quickly

    #imgShort = cv2.resize(src=img, dsize=(0, 0), dst=None, fx=0.25, fy=0.25)
    imgN = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Getting face locations and encodings from the frame

    frameFaceLoc = fr.face_locations(img=imgN)
    frameEncode = fr.face_encodings(face_image=imgN, known_face_locations=frameFaceLoc)

    # Checking the faces with the known encoding faces to recognize it

    for encodeFrameFace, frameFaceLocation in zip(frameEncode, frameFaceLoc):
        faceMatch = fr.compare_faces(known_face_encodings=knownEncodings, face_encoding_to_check=encodeFrameFace)
        faceDistance = fr.face_distance(face_encodings=knownEncodings, face_to_compare=encodeFrameFace)
        index = np.argmin(faceDistance)

        if faceMatch[index]:
            personName = imagenames[index]
            # print(personName)
            markAttendence(personName)

            # Putting the recognized details in the frame

            y1, x2, y2, x1 = frameFaceLocation
            #y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 255), thickness=2)
            cv2.rectangle(img=img, pt1=(x1, y2 - 35), pt2=(x2, y2), color=(255, 0, 127), thickness=-1)
            cv2.putText(img=img, text=personName, org=(x1 + 6, y2 - 6), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 127), thickness=1)
    cv2.imshow("Output", img)


#########################################################################
""" Marking the attendence of any detected face. Won't store any frmae previously detected. """

def markAttendence(name):
    with open("attendence.csv", "r+") as file:
        alreadyEnteredData = file.readlines()
        if name not in namelist:
            namelist.append(name)
            time = datetime.now()
            strtime = time.strftime("%I:%M %p")
            file.writelines(f"\n{name}, {strtime}")


############################################################################
""" Main function that detects the faces """

def faceRecognition():
    # encodingsRegenerate()

    # loading the previously encoded face's encoding values

    file = open("knownencoding.txt", "rb")
    knownEncodings = pickle.load(file)
    file.close()

    # Loading the name of the person in the image that has been used for encoding

    file = open("names.txt", "rb")
    imagenames = pickle.load(file)
    file.close()

    # Setting up webcam for taking frames

    cap = cv2.VideoCapture(0)
    count = 0

    while True:

        # taking one frames to use after skipping 10 frames
        # It is done for making the system faster and more accurate.

        _, img = cap.read()
        count += 1
        if count% 10 != 0:
            cv2.imshow("Cam", img)
        else:
            # Resizing image to perform operations quickly

            imgShort = cv2.resize(src=img, dsize=(0, 0), dst=None, fx=0.25, fy=0.25)
            imgShort = cv2.cvtColor(imgShort, cv2.COLOR_BGR2RGB)

            # Getting face locations and encodings from the frame

            frameFaceLoc = fr.face_locations(img=imgShort)
            frameEncode = fr.face_encodings(face_image=imgShort, known_face_locations=frameFaceLoc)

            # Checking the faces with the known encoding faces to recognize it

            for encodeFrameFace, frameFaceLocation in zip(frameEncode, frameFaceLoc):
                faceMatch = fr.compare_faces(known_face_encodings=knownEncodings, face_encoding_to_check=encodeFrameFace)
                faceDistance = fr.face_distance(face_encodings=knownEncodings, face_to_compare=encodeFrameFace)
                index = np.argmin(faceDistance)

                if faceMatch[index]:
                    personName = imagenames[index]
                    # print(personName)
                    markAttendence(personName)

                    # Putting the recognized details in the frame

                    y1, x2, y2, x1 = frameFaceLocation
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 255), thickness=2)
                    cv2.rectangle(img=img, pt1=(x1, y2 - 35), pt2=(x2, y2), color=(255, 0, 127), thickness=-1)
                    cv2.putText(img=img, text=personName, org=(x1 + 6, y2 - 6), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1,
                                color=(255, 255, 127), thickness=1)
            cv2.imshow("Cam", img)
            count = 0

        # If Esc button is pressed then the system will shutdown.

        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

WelcomeGuide()
Menubar()

label1 = Label(root)
label1.pack()
root.mainloop()


#######################################################################
"""This Part of the code for generating encodings, 
    It is used only once to get all the encodings for using in future any time. """

# def encodingsRegenerate():
#     # mylist = os.listdir(path="attimages/train")
#     # file = open("knownencoding.txt", "r")
#     # lines = file.readlines()
#     # for i, line in zip(mylist, lines):
#     #     imagenames.append(os.path.splitext(i)[0])
#     #     dlist = line.strip(" ").split(",")
#     #     dfloat = list(map(float, dlist))
#     #     faceencoding = np.array(dfloat)
#     #     knownEncodings.append(faceencoding)
#     # file.close()
#




