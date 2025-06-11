import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import pandas as pd
import csv
import takeImage
import saveProfile
import trainImage
import automaticAttendance

# Colors and fonts
bg_color = "#121212"
fg_color = "#00FFF5"
accent_color = "#00ADB5"
header_font = ("Segoe UI", 24, "bold")
label_font = ("Segoe UI", 14)
button_font = ("Segoe UI", 12, "bold")
entry_font = ("Segoe UI", 12)

def get_total_registrations():
    try:
        # Check if the file exists first
        if os.path.exists("StudentDetails/studentdetails.csv"):
            df = pd.read_csv("StudentDetails/studentdetails.csv")
            return len(df)
        else:
            return 0
    except Exception as e:
        print(f"Error getting registrations: {e}")
        return 0

def text_to_speech(text):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        pass

def update_treeview(tree, csv_path):
    if not isinstance(csv_path, str) or not os.path.exists(csv_path):
        return

    # Clear existing data
    for row in tree.get_children():
        tree.delete(row)

    try:
        # Read and display CSV data
        with open(csv_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 4:
                    tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))
    except Exception as e:
        print(f"Error updating treeview: {e}")

def subject_choose(tree, notif_label):
    try:
        # Handle camera not available error gracefully
        try:
            import cv2
            # Test if camera is accessible
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                notif_label.config(text="⚠️ Camera not available")
                messagebox.showerror("Error", "Cannot access webcam. Please check your camera connection.")
                return
            cap.release()
        except Exception as e:
            notif_label.config(text="⚠️ Camera error")
            messagebox.showerror("Error", f"Camera initialization error: {str(e)}")
            return
            
        latest_csv = automaticAttendance.subjectChoose(text_to_speech)
        if latest_csv and os.path.exists(latest_csv):
            update_treeview(tree, latest_csv)
            notif_label.config(text="✅ Attendance updated.")
        else:
            notif_label.config(text="⚠️ Attendance file not found.")
    except Exception as e:
        notif_label.config(text=f"⚠️ Error: {str(e)}")
        print(f"Error in subject_choose: {e}")

def main():
    root = tk.Tk()
    root.title("Attendance - Class Vision")
    root.geometry("1280x720")
    root.configure(bg=bg_color)
    root.resizable(False, False)

    # Ensure directories exist
    os.makedirs("StudentDetails", exist_ok=True)
    os.makedirs("TrainingImage", exist_ok=True)
    os.makedirs("TrainingImageLabel", exist_ok=True)
    os.makedirs("Attendance", exist_ok=True)

    # Header
    header = tk.Frame(root, bg="#1e1e1e", height=90)
    header.pack(fill="x")

    try:
        logo_img = Image.open("UI_IMAGE/0001.png").resize((50, 47), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(header, image=logo, bg="#1e1e1e").place(x=470, y=20)
    except Exception as e:
        print(f"Error loading logo: {e}")
        # Create a placeholder if image not found
        tk.Label(header, text="LOGO", bg="#1e1e1e", fg=fg_color, font=("Segoe UI", 12)).place(x=470, y=20)

    tk.Label(header, text="FACE RECOGNITION BASED ATTENDANCE SYSTEM", font=header_font,
             bg="#1e1e1e", fg=fg_color).place(relx=0.5, y=30, anchor="center")

    content = tk.Frame(root, bg=bg_color)
    content.pack(pady=10, padx=30, fill="both", expand=True)

    # Left Frame (Attendance Display)
    left_frame = tk.Frame(content, bg=bg_color)
    left_frame.pack(side="left", fill="y", padx=(0, 50), pady=10)

    tk.Label(left_frame, text="For Already Registered", font=("Segoe UI", 18, "bold"),
             bg=bg_color, fg="#00FFAA").pack(pady=(0, 10))

    notif_label = tk.Label(left_frame, text="", font=("Segoe UI", 12), fg="green", bg=bg_color)
    notif_label.pack()

    tree_frame = tk.Frame(left_frame, bg=bg_color)
    tree_frame.pack(pady=10)
    columns = ("ID", "Name", "Date", "Time")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
    
    # Configure style for treeview
    style = ttk.Style()
    style.configure("Treeview", 
                   background="#333333", 
                   foreground="white", 
                   fieldbackground="#333333",
                   font=("Segoe UI", 10))
    style.configure("Treeview.Heading", 
                   font=("Segoe UI", 11, "bold"),
                   background="#1e1e1e",
                   foreground=fg_color)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left")

    tk.Button(left_frame, text="Take Attendance",
              command=lambda: subject_choose(tree, notif_label),
              font=button_font, bg=accent_color, fg="white", cursor="hand2").pack(pady=10)

    tk.Button(left_frame, text="Quit", command=root.destroy,
              font=button_font, bg="red", fg="white", cursor="hand2").pack(pady=20)

    # Right Frame (Registration)
    right_frame = tk.Frame(content, bg=bg_color)
    right_frame.pack(side="right", fill="y", pady=10)

    tk.Label(right_frame, text="For New Registrations", font=("Segoe UI", 18, "bold"),
             bg=bg_color, fg="#00FFAA").pack(pady=(0, 10))

    form_frame = tk.Frame(right_frame, bg=bg_color)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Enter Enrollment No:", font=label_font,
             bg=bg_color, fg="white").grid(row=0, column=0, sticky="w", pady=5)
    enroll_entry = tk.Entry(form_frame, font=entry_font, bg="#333333", fg="white", relief="flat")
    enroll_entry.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Enter Name:", font=label_font,
             bg=bg_color, fg="white").grid(row=1, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(form_frame, font=entry_font, bg="#333333", fg="white", relief="flat")
    name_entry.grid(row=1, column=1, pady=5, padx=10)

    notif = tk.Label(right_frame, text="", font=("Segoe UI", 12, "bold"), fg="#00FFAA", bg=bg_color)
    notif.pack(pady=10)

    btn_style = {
        "font": button_font,
        "bg": accent_color,
        "fg": "white",
        "activebackground": "#007B8A",
        "relief": "flat",
        "cursor": "hand2",
        "width": 20,
        "height": 2
    }

    # Store ImageTk references to prevent garbage collection
    root.image_refs = []
    if 'logo' in locals():
        root.image_refs.append(logo)

    tk.Button(right_frame, text="Take Images",
              command=lambda: takeImage.TakeImage(enroll_entry.get(), name_entry.get(), "haarcascade_frontalface_default.xml", "TrainingImage", notif, None, text_to_speech),
              **btn_style).pack(pady=5)

    # Fix for saveProfile module issue - call the correct function
    tk.Button(right_frame, text="Save Profile",
              command=lambda: saveProfile.save_profile(enroll_entry.get(), name_entry.get(), notif, text_to_speech),
              **btn_style).pack(pady=5)

    tk.Button(right_frame, text="Train Model",
              command=lambda: trainImage.TrainImage("haarcascade_frontalface_default.xml", "TrainingImage", "TrainingImageLabel/Trainner.yml", notif, text_to_speech),
              **btn_style).pack(pady=5)

    total = get_total_registrations()
    total_label = tk.Label(right_frame, text=f"Total Registrations till now: {total}", font=("Segoe UI", 12, "bold"),
             fg="#FFD369", bg=bg_color)
    total_label.pack(pady=20)
    
    # Update total registrations periodically
    def update_total_registrations():
        current_total = get_total_registrations()
        total_label.config(text=f"Total Registrations till now: {current_total}")
        root.after(30000, update_total_registrations)  # Update every 30 seconds
    
    # Start the periodic update
    root.after(30000, update_total_registrations)

    root.mainloop()

if __name__ == "__main__":
    main()