import tkinter as tk
from tkinter import Message ,Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
#root window
window = tk.Tk()
window.title("Face_Recogniser")

window.configure(background='#747575')

window.geometry("1350x720")

#heading label
title = tk.Label(window, text="Face Recognition Based Attendance Management System" ,bg="black"  ,fg="white"  ,width=60  ,height=3,font=('times', 30, 'bold')) 
title.place(x=0,y=10)

lbl_id = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="white"  ,bg="black" ,font=('times', 15, ' bold ') ) 
lbl_id.place(x=300, y=200)

txt_id = tk.Entry(window,width=20  ,bg="#abb0b0" ,fg="black",font=('times', 15, ' bold '))
txt_id.place(x=600, y=215)

lbl_name = tk.Label(window, text="Enter Name",width=20  ,fg="white"  ,bg="black"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl_name.place(x=300, y=300)

txt_name = tk.Entry(window,width=20  ,bg="#abb0b0"  ,fg="black",font=('times', 15, ' bold ')  )
txt_name.place(x=600, y=315)

lbl_notification = tk.Label(window, text="Status : ",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('times', 15, ' bold  ')) 
lbl_notification.place(x=300, y=400)

txt_notification = tk.Label(window, text="" ,bg="#abb0b0"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
txt_notification.place(x=600, y=400)

#lbl_attendance = tk.Label(window, text="Attendance : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline')) 
#lbl_attendance.place(x=300, y=650)

#txt_attendance = tk.Label(window, text="" ,fg="red"   ,bg="yellow",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
#txt_attendance.place(x=600, y=650)
 
def clear():
    txt_id.delete(0, 'end')    
    res = ""
    txt_id.configure(text= res)

def clear2():
    txt_name.delete(0, 'end')    
    res = ""
    txt_name.configure(text= res)       

 #function to crop and save images from video using haar cascade classifier
def TakeImages():        
    Id=(txt_id.get())
    name=(txt_name.get())
    if(name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                cv2.putText(img,"Sample taken:"+ str(sampleNum),(100,50),cv2.FONT_HERSHEY_SIMPLEX ,1,(255, 0, 0) , 2)
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 60
            elif sampleNum>59:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails/StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        txt_notification.configure(text= res)
    else:
        
        if(name.isalpha()):
            res = "Enter Numeric Id"
            txt_notification.configure(text= res)
 

#function to train LPBH recogniser   
def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Image Trained"
    txt_notification.configure(text= res)


#function to to fetch list of images along with their ids
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
       
    #create empty face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids


#function to detect faces
def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)    
    df=pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa                
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    #Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance/Attendance_"+date+".csv"
    if not os.path.exists("Attendance/Attendance_"+date+".csv"):
        attendance.to_csv(fileName,index=False)
    else:
        attendance.to_csv(fileName, mode='a',index=False,header=False)
    data = pd.read_csv(fileName)
    data.drop_duplicates(subset=['Id'],keep='last',inplace=True)  
    data.to_csv(fileName,index=False)     
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    txt_notification.configure(text= res)

def function12():
    
    os.system("py view_attendance.py")
  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="white"  ,bg="black"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=850, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="white"  ,bg="black"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=850, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=100, y=500)
view = tk.Button(window, text="Attendance", command=function12  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
view.place(x=550, y=625)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=400, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=700, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="black"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1000, y=500)

window.mainloop()