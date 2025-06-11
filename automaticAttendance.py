import os
import cv2
import pandas as pd
import datetime
import time

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def subjectChoose(text_to_speech=None):
    try:
        import tkinter as tk
        from tkinter import simpledialog, messagebox

        root = tk.Tk()
        root.withdraw()
        subject_name = simpledialog.askstring("Subject", "Enter Subject Name:")
        if not subject_name:
            return None

        # Check for required files
        if not os.path.exists(trainimagelabel_path):
            messagebox.showerror("Error", "Model not found, please train the model.")
            if text_to_speech:
                text_to_speech("Model not found, please train the model.")
            return None
        
        if not os.path.exists(studentdetail_path):
            messagebox.showerror("Error", "Student details not found.")
            if text_to_speech:
                text_to_speech("Student details not found.")
            return None

        # Initialize face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainimagelabel_path)
        face_cascade = cv2.CascadeClassifier(haarcasecade_path)
        
        # Load student data
        try:
            df = pd.read_csv(studentdetail_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading student details: {str(e)}")
            if text_to_speech:
                text_to_speech("Error reading student details file.")
            return None

        # Initialize camera
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            if text_to_speech:
                text_to_speech("Could not open camera.")
            return None

        # Set up attendance dataframe
        attendance = pd.DataFrame(columns=["ID", "Name", "Date", "Time"])
        recognized_ids = set()  # To track which students have been recognized
        
        # Create a window with a countdown timer
        start_time = datetime.datetime.now()
        duration = 20  # seconds
        
        if text_to_speech:
            text_to_speech(f"Starting attendance for {subject_name}. Please look at the camera.")

        while (datetime.datetime.now() - start_time).seconds < duration:
            ret, img = cam.read()
            if not ret:
                if text_to_speech:
                    text_to_speech("Camera error. Please restart.")
                break
                
            # Calculate remaining time
            elapsed = (datetime.datetime.now() - start_time).seconds
            remaining = duration - elapsed
                
            # Process frame
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                id_, conf = recognizer.predict(gray[y:y + h, x:x + w])
                
                if conf < 70:  # Good recognition confidence
                    # Check if we have this student ID in our data
                    matching_rows = df.loc[df["Enrollment"] == id_]
                    if not matching_rows.empty:
                        name = matching_rows["Name"].values[0]
                        
                        # Visual indication: Green box for new attendance, Blue for already marked
                        if id_ not in recognized_ids:
                            # New attendance - mark in green
                            current_time = datetime.datetime.now().strftime("%H:%M:%S")
                            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                            attendance.loc[len(attendance)] = [id_, name, current_date, current_time]
                            recognized_ids.add(id_)
                            box_color = (0, 255, 0)  # Green for new attendance
                            cv2.putText(img, f"{name} - Marked!", (x, y - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                        else:
                            # Already marked - show in blue
                            box_color = (255, 0, 0)  # Blue for already marked
                            cv2.putText(img, f"{name} - Already Marked", (x, y - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                        
                        cv2.rectangle(img, (x, y), (x + w, y + h), box_color, 2)
                    else:
                        # ID found but not in student database
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 165, 255), 2)  # Orange
                        cv2.putText(img, "Not Registered", (x, y - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                else:
                    # Low confidence recognition
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red
                    cv2.putText(img, "Unknown", (x, y - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Show countdown and attendance count
            count_text = f"Students: {len(recognized_ids)}/{len(df)}"
            timer_text = f"Time: {remaining}s"
            cv2.putText(img, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(img, timer_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("Attendance", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Handle no attendance case
        if len(attendance) == 0:
            messagebox.showinfo("Information", "No students were recognized.")
            if text_to_speech:
                text_to_speech("No students were recognized.")
            return None

        # Ensure attendance directory exists
        if not os.path.exists(attendance_path):
            os.makedirs(attendance_path)

        # Save attendance file
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.now().strftime("%H-%M-%S")
        filename = f"{attendance_path}/{subject_name}_{date}_{timeStamp}.csv"
        attendance.to_csv(filename, index=False)

        # Show summary
        summary_message = f"Attendance completed. Marked {len(attendance)} students present."
        messagebox.showinfo("Attendance", summary_message)
        if text_to_speech:
            text_to_speech(summary_message)
            
        return filename

    except Exception as e:
        error_message = f"Error: {str(e)}"
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", error_message)
        if text_to_speech:
            text_to_speech("Error during attendance.")
        print(f"Exception in attendance: {str(e)}")
        return None