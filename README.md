# Face-Recogniton-based-Attendance-System

I have build this system called "Face Recognition based Attendance System". This system can take an image from the storage or webcam to identify a person who's information been previousy encoded to the system. The recognition person's name & time of recognitiotn is sotred in a CSV file named **output.csv**. I have build The GUI with "Tkinter" package. 
Similar tutorial can be founnd in [Murtaza's Workshop - Robotics and AI](https://www.youtube.com/user/Mhproductionhouse) YouTube channel. The main repository of the "face-recognition" package can be found [here](https://github.com/ageitgey/face_recognition).

There are several pre-requisite for building/running this system. The steps to meet them are:
1. Install Visual Studio Community 2019.
   - Install "Desktop developmet C/C++".
2. Install these in the virtual environment.
   - Install "dlib" package.
   - Install "Cmake" package.
   - Install "face-recognition" package.

Now Donwload this Github repository and unzip it in you desired location. After that follow these steps.
1. Keep the virtual environment active in the terminal
2. Traverse to the file localiton where "Face-Recognizer.py" file exists.
3. Run that python file. 
   - Command : ```python Face-Recognizer.py```
5. Use the system with the given images in this repository.
6. See the result in the **output.csv** file.

If everything is properly done then the output will be in the a separate window as well as in the CSV file.
