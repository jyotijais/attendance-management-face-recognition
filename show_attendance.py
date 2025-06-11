import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import messagebox
from automaticAttendance import subjectChoose

def subjectchoose(text_to_speech):
    def calculate_attendance():
        subject_name = subject_entry.get().strip()
        if not subject_name:
            text_to_speech("Please enter the subject name.")
            return

        folder_path = os.path.join("Attendance", subject_name)
        filenames = glob(os.path.join(folder_path, f"{subject_name}*.csv"))

        if not filenames:
            text_to_speech("No attendance records found for this subject.")
            return

        df_list = [pd.read_csv(f) for f in filenames]
        final_df = df_list[0]
        for df in df_list[1:]:
            final_df = final_df.merge(df, how="outer")

        final_df.fillna(0, inplace=True)
        final_df["Attendance"] = [
            f"{int(round(row[2:-1].mean() * 100))}%" for _, row in final_df.iterrows()
        ]

        final_csv_path = os.path.join(folder_path, "attendance.csv")
        final_df.to_csv(final_csv_path, index=False)
        os.startfile(final_csv_path)

    def open_folder():
        subject_name = subject_entry.get().strip()
        path = os.path.join("Attendance", subject_name)
        if subject_name and os.path.exists(path):
            os.startfile(path)
        elif not subject_name:
            text_to_speech("Enter a subject name first.")
        else:
            text_to_speech("Folder does not exist.")
          
    #GUI setup
    window = tk.Tk()
    window.title("📘 View Attendance Sheet")
    window.geometry("500x300")
    window.configure(bg="#f0f4f8")
    window.resizable(False, False)

    tk.Label(window, text="📚 Choose Subject", font=("Segoe UI", 20, "bold"), bg="#f0f4f8", fg="#333").pack(pady=20)
    tk.Label(window, text="Subject Name:", font=("Segoe UI", 12), bg="#f0f4f8", fg="#333").pack()

    subject_entry = tk.Entry(window, font=("Segoe UI", 14), width=25, justify="center", bd=2, relief="groove")
    subject_entry.pack(pady=10)

    tk.Button(window, text="🧾 Generate Attendance Report", command=calculate_attendance,
              font=("Segoe UI", 12), bg="#007acc", fg="white", padx=10, pady=5).pack(pady=10)

    tk.Button(window, text="📁 Open Subject Folder", command=open_folder,
              font=("Segoe UI", 12), bg="#444", fg="white", padx=10, pady=5).pack()

    window.mainloop()

