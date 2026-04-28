# Face-Recognition-Attendance-Management-System
An advanced, highly accurate, and automated student attendance tracking system built using Python. This project replaces traditional manual attendance processes with a state-of-the-art Deep Learning facial recognition approach, ensuring a secure and efficient way to manage academic records.

### Key Features

* **Deep Learning Facial Recognition:** Upgraded from basic LBPH to the robust `face_recognition` (dlib) model for high-accuracy face detection and matching in real-time.
* **Dual-Storage Integration:** Automatically saves attendance records simultaneously into local `.csv` files (Excel) and a **MySQL Database** to prevent data loss.
* **Intelligent Database Handling:** Automatically sanitizes inputs (handling spaces and special characters like `&`) to create error-free dynamic SQL tables based on subject names and timestamps.
* **Interactive GUI:** A user-friendly desktop interface built with `Tkinter` for easy navigation between taking images, training the model, and filling attendance.
* **Manual Entry Fallback:** Includes a secure manual attendance entry module that also syncs with both CSV and MySQL seamlessly.

### Tech Stack & Technologies

* **Language:** Python 3.11
* **Computer Vision & AI:** OpenCV (`cv2`), `dlib`, `face_recognition`
* **Data Handling:** Pandas, NumPy
* **Database:** MySQL (via XAMPP), `pymysql`
* **GUI:** Tkinter

### Prerequisites & Setup

Before running this project, ensure you have the following installed on your system:
1.  **Python 3.11** (Ensure it is added to your PATH).
2.  **XAMPP** (For MySQL database server).
3.  **C++ Build Tools** (Required for compiling `dlib`)
 - MSVC v143 - VS 2022 C++ x64/x86 build tools
 - Windows SDK (10 or 11, depending on your system)
 - C++ CMake tools for Windows

### Installation Steps

### Install required Python packages
- Open your terminal and run:
- `py -m pip install cmake dlib face_recognition opencv-python pandas numpy pymysql`

### Database Configuration (Crucial Step)

- Open XAMPP Control Panel and start Apache and MySQL.
- Open your browser and navigate to http://localhost/phpmyadmin.
- Create two empty databases with the exact following names:
- manually_fill_attendance
- face_reco_fill
(Note: The Python script will automatically generate the required tables inside these databases).

### What steps you have to follow to run the project?
- Ensure your XAMPP MySQL server is running in the background.
- Open your terminal in the project directory.
- Run `AMS_Run.py`.

### Project Structure

- After run you need to give your face data to system so enter your ID and name in box than click on `Take Images` button.
- It will collect 200 images of your faces, it save a images in `TrainingImage` folder
- After that we need to train a model(for train a model click on `Train Image` button.
- It will take 5-10 minutes for training(for 10 person data).
- After training click on `Automatic Attendance` ,it can fill attendance by your face using our trained model (model will save in `TrainingImageLabel` )
- it will create `.csv` file of attendance according to time & subject.
- You can store data in database (install wampserver),change the DB name according to your in `AMS_Run.py`.
- `Manually Fill Attendance` Button in UI is for fill a manually attendance (without facce recognition),it's also create a `.csv` and store in a database.

### Screenshots

### Basic UI
<img src="https://github.com/umerchaudhary04/Face-Recognition-Attendance-System/blob/main/Screenshot%20(31).png">

### Automatic Attendance Filling UI
<img src="https://github.com/umerchaudhary04/Face-Recognition-Attendance-System/blob/main/Screenshot%20(02).JPG">

### Manually Attendance Filling UI
<img src="https://github.com/umerchaudhary04/Face-Recognition-Attendance-System/blob/main/Screenshot%20(35).JPG">

### Notes
- It will require high processing power(I have 8 GB RAM)
- Noisy image can reduce the accuracy, so quality of images should be good.

### Author
Umer Asghar (Umer Chaudhary)
Software Engineering Student | Passionate about AI, Computer Vision, and scalable software architecture.