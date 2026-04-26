import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import threading
import face_recognition
import pickle
import pymysql

# Window is our Main frame of system
window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")
window.geometry('1280x720')
window.configure(background='grey80')

# ==========================================
# REUSABLE ERROR SCREENS
# ==========================================
def create_error_window(message):
    ec = tk.Toplevel() 
    ec.geometry('330x100')
    ec.title('Warning!!')
    ec.configure(background='snow')
    Label(ec, text=message, fg='red', bg='white', font=('times', 16, ' bold ')).pack()
    Button(ec, text='OK', command=ec.destroy, fg="black", bg="lawn green", width=9, height=1, font=('times', 15, ' bold ')).place(x=90, y=50)

# ==========================================
# MANUALLY FILL ATTENDANCE (Original Logic)
# ==========================================
def manually_fill():
    sb = tk.Toplevel() 
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='grey80')

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        
        subb = SUB_ENTRY.get()
        DB_table_name = str(subb + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second)

        try:
            connection = pymysql.connect(host='localhost', user='root', password='', db='manually_fill_attendance')
            cursor = connection.cursor()
            sql = "CREATE TABLE " + DB_table_name + """
                            (ID INT NOT NULL AUTO_INCREMENT,
                             ENROLLMENT varchar(100) NOT NULL,
                             NAME VARCHAR(50) NOT NULL,
                             DATE VARCHAR(20) NOT NULL,
                             TIME VARCHAR(20) NOT NULL,
                                 PRIMARY KEY (ID));"""
            cursor.execute(sql)
        except Exception as ex:
            print(ex)

        if subb == '':
            create_error_window('Please enter your subject name!!!')
        else:
            sb.destroy()
            MFW = tk.Toplevel()
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='grey80')

            def testVal(inStr, acttyp):
                if acttyp == '1':
                    if not inStr.isdigit(): return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="grey", font=('times', 15))
            ENR.place(x=30, y=100)
            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="black", bg="grey", font=('times', 15))
            STU_NAME.place(x=30, y=200)

            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key', bg="white", fg="black", font=('times', 23))
            ENR_ENTRY['validatecommand'] = (ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="white", fg="black", font=('times', 23))
            STUDENT_ENTRY.place(x=290, y=205)

            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '' or STUDENT == '':
                    create_error_window('Please enter Student & Enrollment!!!')
                else:
                    time_str = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
                    Insert_data = "INSERT INTO " + DB_table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(STUDENT), str(Date), str(time_str))
                    try:
                        cursor.execute(Insert_data, VALUES)
                        connection.commit()
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(0, END)
                    STUDENT_ENTRY.delete(0, END)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="SkyBlue1", width=20, height=2, font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=300)

    SUB = tk.Label(sb, text="Enter Subject : ", width=15, height=2, fg="black", bg="grey80", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)
    SUB_ENTRY = tk.Entry(sb, width=20, bg="white", fg="black", font=('times', 23))
    SUB_ENTRY.place(x=250, y=105)
    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="black", bg="SkyBlue1", width=20, height=2, font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)

# ==========================================
# 1. NEW TAKE IMAGES LOGIC (DEEP LEARNING)
# ==========================================
def take_img_logic():
    enrollment = txt.get()
    name = txt2.get()
    if enrollment == '' or name == '':
        create_error_window("Enrollment & Name required!!!")
        return

    if not os.path.exists("TrainingImage"):
        os.makedirs("TrainingImage")

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        create_error_window("Camera Error! Cannot open webcam.")
        return

    while True:
        ret, frame = cam.read()
        if not ret: break
        
        cv2.putText(frame, "Look at camera and press SPACE to capture", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Capture Image", frame)
        
        # Space bar to capture
        if cv2.waitKey(1) & 0xFF == 32: 
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:
                filename = f"TrainingImage/{enrollment}_{name}.jpg"
                cv2.imwrite(filename, frame)
                
                # Save details to CSV
                ts = time.time()
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                row = [enrollment, name, Date, Time]
                
                if not os.path.exists('StudentDetails'):
                    os.makedirs('StudentDetails')
                with open('StudentDetails/StudentDetails.csv', 'a+', newline='') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(row)
                
                Notification.configure(text=f"Saved: {enrollment} - {name}", bg="SpringGreen3", width=50)
                break
            else:
                print("No face detected! Try again.")
                
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# ==========================================
# 2. NEW TRAIN IMAGES LOGIC (DEEP LEARNING)
# ==========================================
def trainimg_logic():
    known_encodings = []
    known_names = []
    known_ids = []
    
    if not os.path.exists("TrainingImage"):
        Notification.configure(text='Please make "TrainingImage" folder & add images', bg="red", width=50)
        return

    for file in os.listdir("TrainingImage"):
        if file.endswith(".jpg") or file.endswith(".png"):
            parts = file.split('.')[0].split('_')
            if len(parts) >= 2:
                enrollment_id = parts[0]
                name = parts[1]
                
                img_path = os.path.join("TrainingImage", file)
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)
                
                if len(encodings) > 0:
                    known_encodings.append(encodings[0])
                    known_names.append(name)
                    known_ids.append(enrollment_id)
                    
    with open("encodings.pkl", "wb") as f:
        pickle.dump([known_encodings, known_names, known_ids], f)
        
    Notification.configure(text="AI Model Trained Successfully!", bg="olive drab", width=50)

# ==========================================
# 3. NEW AUTOMATIC ATTENDANCE LOGIC
# ==========================================
def subjectchoose():
    windo = tk.Toplevel()
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='grey80')
    Notifica = tk.Label(windo, text="", bg="grey80", fg="white", width=33, height=2, font=('times', 15, 'bold'))
    Notifica.place(x=20, y=250)

    def fill_attendance_logic():
        sub = tx.get()
        if sub == '':
            create_error_window('Please enter your subject name!!!')
            return

        try:
            with open("encodings.pkl", "rb") as f:
                known_encodings, known_names, known_ids = pickle.load(f)
        except FileNotFoundError:
            Notifica.configure(text='Model not trained!', bg="red")
            return

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            Notifica.configure(text="Camera Error!", bg="red")
            return

        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Enrollment', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)
        
        future = time.time() + 20 # 20 seconds window

        while True:
            ret, im = cam.read()
            small_frame = cv2.resize(im, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                top *= 4; right *= 4; bottom *= 4; left *= 4
                
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                name, Id = "Unknown", "Unknown"
                
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                        Id = known_ids[best_match_index]
                        
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
                
                color = (0, 260, 0) if name != "Unknown" else (0, 25, 255)
                cv2.rectangle(im, (left, top), (right, bottom), color, 4)
                cv2.putText(im, f"{Id}-{name}", (left, top - 10), font, 1, color, 2)
                
            cv2.imshow('Filling Attendance (Press ESC to stop)', im)
            
            if time.time() > future or (cv2.waitKey(1) & 0xFF == 27):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Save to DB and CSV
        attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        
        if not os.path.exists("Attendance"): os.makedirs("Attendance")
        fileName = f"Attendance/{sub}_{date}_{Hour}-{Minute}-{Second}.csv"
        attendance.to_csv(fileName, index=False)

        # Database insertion
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        DB_Table_name = str(sub + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
        
        try:
            connection = pymysql.connect(host='localhost', user='root', password='', db='Face_reco_fill')
            cursor = connection.cursor()
            sql = "CREATE TABLE " + DB_Table_name + """
            (ID INT NOT NULL AUTO_INCREMENT, ENROLLMENT varchar(100) NOT NULL, NAME VARCHAR(50) NOT NULL,
             DATE VARCHAR(20) NOT NULL, TIME VARCHAR(20) NOT NULL, PRIMARY KEY (ID));"""
            cursor.execute(sql)
            
            for index, row in attendance.iterrows():
                insert_data = "INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                cursor.execute(insert_data, (str(row['Enrollment']), str(row['Name']), str(row['Date']), str(row['Time'])))
            connection.commit()
        except Exception as e:
            print("DB Error:", e)

        Notifica.configure(text='Attendance Filled Successfully!', bg="Green")

    def thread_fill_attendance():
        t = threading.Thread(target=fill_attendance_logic)
        t.start()

    sub = tk.Label(windo, text="Enter Subject : ", width=15, height=2, fg="black", bg="grey", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)
    tx = tk.Entry(windo, width=20, bg="white", fg="black", font=('times', 23))
    tx.place(x=250, y=105)
    fill_a = tk.Button(windo, text="Fill Attendance", command=thread_fill_attendance, fg="white", bg="SkyBlue1", width=20, height=2, font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)

# ==========================================
# THREAD WRAPPERS FOR MAIN BUTTONS
# ==========================================
def thread_take_img():
    threading.Thread(target=take_img_logic).start()

def thread_trainimg():
    threading.Thread(target=trainimg_logic).start()

# ==========================================
# MAIN GUI LAYOUT
# ==========================================
message = tk.Label(window, text="Face-Recognition-Based-Attendance-System", bg="black", fg="white", width=50, height=3, font=('times', 30, ' bold '))
message.place(x=80, y=20)

Notification = tk.Label(window, text="", bg="grey80", fg="white", width=50, height=3, font=('times', 17))
Notification.place(x=250, y=400)

lbl = tk.Label(window, text="Enter Enrollment : ", width=20, height=2, fg="black", bg="grey", font=('times', 15, 'bold'))
lbl.place(x=200, y=200)
txt = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 25))
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name : ", width=20, fg="black", bg="grey", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)
txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 25))
txt2.place(x=550, y=310)

def clear(): txt.delete(0, END)
def clear1(): txt2.delete(0, END)

clearButton = tk.Button(window, text="Clear", command=clear, fg="white", bg="black", width=10, height=1, font=('times', 15, ' bold '))
clearButton.place(x=950, y=210)
clearButton1 = tk.Button(window, text="Clear", command=clear1, fg="white", bg="black", width=10, height=1, font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)

takeImg = tk.Button(window, text="Take Images", command=thread_take_img, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Images", command=thread_trainimg, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold '))
trainImg.place(x=390, y=500)

FA = tk.Button(window, text="Automatic Attendance", command=subjectchoose, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold '))
FA.place(x=690, y=500)

quitWindow = tk.Button(window, text="Manually Fill Attendance", command=manually_fill, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold '))
quitWindow.place(x=990, y=500)

window.mainloop()