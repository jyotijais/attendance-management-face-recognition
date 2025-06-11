import os
import csv
from datetime import datetime

def is_number(string):
    """Check if the input string is a valid number."""
    try:
        float(string)
        return True
    except ValueError:
        return False

def save_profile(Id, Name, notification_label=None, text_to_speech=None):
    """
    Save student profile to CSV file
    
    Parameters:
    -----------
    Id : str
        Student ID/Enrollment number
    Name : str
        Student name
    notification_label : tkinter.Label, optional
        Label widget to display notifications
    text_to_speech : function, optional
        Function to convert text to speech
    """
    try:
        # Input validation
        if not Id or not Name:
            msg = "Please fill all the fields!"
            if notification_label:
                notification_label.config(text=msg)
            if text_to_speech:
                text_to_speech(msg)
            return False

        # Validate ID is a number
        if not is_number(Id):
            msg = "ID must be a number!"
            if notification_label:
                notification_label.config(text=msg)
            if text_to_speech:
                text_to_speech(msg)
            return False

        # Create directory if it doesn't exist
        if not os.path.exists("StudentDetails"):
            os.makedirs("StudentDetails")

        # Check if student details file exists
        csv_file_path = "StudentDetails/studentdetails.csv"
        file_exists = os.path.isfile(csv_file_path)

        # Check if ID already exists in file
        if file_exists:
            with open(csv_file_path, "r", newline="") as csvFile:
                reader = csv.reader(csvFile)
                # Skip header
                header = next(reader, None)
                # Check each row for matching ID
                for row in reader:
                    if len(row) > 0 and row[0] == Id:
                        msg = f"ID {Id} already exists!"
                        if notification_label:
                            notification_label.config(text=msg)
                        if text_to_speech:
                            text_to_speech(msg)
                        return False

        # Open file in append mode or create new with header
        mode = "a" if file_exists else "w"
        with open(csv_file_path, mode, newline="") as csvFile:
            writer = csv.writer(csvFile)
            
            # Write header if new file
            if not file_exists:
                writer.writerow(["Enrollment", "Name", "RegisteredOn"])
                
            # Get current date and time
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write student details
            writer.writerow([Id, Name, current_date])
            
        # Success message
        msg = f"Profile saved for {Name}!"
        if notification_label:
            notification_label.config(text=msg)
        if text_to_speech:
            text_to_speech(msg)
        return True
            
    except Exception as e:
        # Error message
        msg = f"Error saving profile: {str(e)}"
        if notification_label:
            notification_label.config(text=msg)
        if text_to_speech:
            text_to_speech("Error saving profile")
        print(msg)
        return False
