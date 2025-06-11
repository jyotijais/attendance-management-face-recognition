import csv
import os
import cv2

os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def TakeImage(enrollment, name, haarcascade_path, trainimage_path, message_label, err_screen, text_to_speech):
    if not enrollment and not name:
        text_to_speech("Please enter your Enrollment Number and Name.")
        return
    elif not enrollment:
        text_to_speech("Please enter your Enrollment Number.")
        return
    elif not name:
        text_to_speech("Please enter your Name.")
        return

    try:
        enrollment = enrollment.strip()
        name = name.strip()
        sample_num = 0
        folder_name = f"{enrollment}_{name}"
        save_path = os.path.join(trainimage_path, folder_name)

        if os.path.exists(save_path):
            raise FileExistsError("Student data already exists.")

        os.makedirs(save_path)

        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcascade_path)

        while True:
            ret, img = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                sample_num += 1
                face_img = gray[y:y+h, x:x+w]
                img_name = f"{name}_{enrollment}_{sample_num}.jpg"
                cv2.imwrite(os.path.join(save_path, img_name), face_img)

                # Rectangle around face
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = f"{name} ({sample_num}/50)"
                cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Capture Face", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif sample_num >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        # Append to CSV
        with open("StudentDetails/studentdetails.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([enrollment, name])

        result_msg = f"Images saved for ER No: {enrollment}, Name: {name}"
        message_label.configure(text=result_msg)
        text_to_speech(result_msg)

    except FileExistsError as e:
        text_to_speech(str(e))
    except Exception as e:
        print(f"Error: {e}")
        text_to_speech("An error occurred while capturing images.")
