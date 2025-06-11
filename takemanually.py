import tkinter as tk
from tkinter import messagebox
import pandas as pd
import datetime
import os
import subprocess

# Global variables
data = {}
index = 0
ts = datetime.datetime.now()
Date = ts.strftime("%Y_%m_%d")
Time = ts.strftime("%H:%M:%S")
Hour, Minute, Second = Time.split(":")
last_csv_path = None


def manually_fill():
    def show_error(msg):
        messagebox.showerror("Input Error", msg)

    def submit_subject():
        subject = subject_entry.get().strip()
        if not subject:
            show_error("Please enter the subject name!")
            return
        subject_window.destroy()
        open_attendance_form(subject)

    def open_attendance_form(subject):
        def clear_enrollment():
            enrollment_entry.delete(0, tk.END)

        def clear_name():
            name_entry.delete(0, tk.END)

        def enter_data():
            global index
            enrollment = enrollment_entry.get().strip()
            name = name_entry.get().strip()
            if not enrollment or not name:
                show_error("Please enter both Enrollment and Name!")
                return

            data[index] = {"Enrollment": enrollment, "Name": name, Date: 1}
            index += 1
            clear_enrollment()
            clear_name()
            update_notification("Entry added")

        def create_csv():
            global last_csv_path
            if not data:
                update_notification("No data to save")
                return
            df = pd.DataFrame.from_dict(data, orient='index')
            os.makedirs("Attendance(Manually)", exist_ok=True)
            file_name = f"Attendance(Manually)/{subject}_{Date}_{Hour}-{Minute}-{Second}.csv"
            df.to_csv(file_name, index=False)
            last_csv_path = file_name
            update_notification("CSV created successfully")
            open_btn.config(state=tk.NORMAL)  # Enable the button

        def open_csv_file():
            global last_csv_path
            if last_csv_path and os.path.exists(last_csv_path):
                try:
                    subprocess.Popen(["start", "", last_csv_path], shell=True)
                except Exception as e:
                    show_error(f"Could not open file:\n{e}")
            else:
                show_error("CSV file not found")

        def update_notification(msg):
            notify_label.config(text=msg)

        form = tk.Tk()
        form.title(f"Manual Attendance - {subject}")
        form.geometry("750x420")
        form.configure(bg="white")

        tk.Label(form, text="Enrollment No:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=20, pady=20)
        enrollment_entry = tk.Entry(form, font=("Arial", 14), width=20)
        enrollment_entry.grid(row=0, column=1)

        tk.Button(form, text="Clear", command=clear_enrollment, bg="tomato", font=("Arial", 12)).grid(row=0, column=2)

        tk.Label(form, text="Student Name:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=20, pady=20)
        name_entry = tk.Entry(form, font=("Arial", 14), width=20)
        name_entry.grid(row=1, column=1)

        tk.Button(form, text="Clear", command=clear_name, bg="tomato", font=("Arial", 12)).grid(row=1, column=2)

        tk.Button(form, text="Enter Data", command=enter_data, bg="lightgreen", font=("Arial", 14), width=15).grid(row=2, column=0, pady=20)
        tk.Button(form, text="Create CSV", command=create_csv, bg="skyblue", font=("Arial", 14), width=15).grid(row=2, column=1)

        global notify_label
        notify_label = tk.Label(form, text="", bg="white", font=("Arial", 12), fg="green")
        notify_label.grid(row=3, column=0, columnspan=3, pady=10)

        # New Button to Open CSV File
        open_btn = tk.Button(form, text="Open CSV File", command=open_csv_file, bg="purple", fg="white",
                             font=("Arial", 14), width=20, state=tk.DISABLED)
        open_btn.grid(row=4, column=0, columnspan=3, pady=10)

        form.mainloop()

    # Subject Entry Window
    subject_window = tk.Tk()
    subject_window.title("Enter Subject Name")
    subject_window.geometry("400x180")
    subject_window.configure(bg="white")

    tk.Label(subject_window, text="Subject Name:", font=("Arial", 14), bg="white").pack(pady=10)
    subject_entry = tk.Entry(subject_window, font=("Arial", 14), width=25)
    subject_entry.pack(pady=5)

    tk.Button(subject_window, text="Submit", command=submit_subject, bg="dodgerblue", fg="white", font=("Arial", 12), width=20).pack(pady=20)
    subject_window.mainloop()
