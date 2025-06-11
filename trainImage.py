import os
import cv2
import numpy as np
from PIL import Image

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    
    if len(faces) == 0:
        msg = "⚠️ No training data found!"
        message.configure(text=msg)
        text_to_speech(msg)
        return

    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)
    
    res = "✅ Model trained successfully!"
    message.configure(text=res)
    text_to_speech(res)

def getImagesAndLables(path):
    imagePaths = []
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        for image_file in os.listdir(folder_path):
            imagePaths.append(os.path.join(folder_path, image_file))

    faces = []
    Ids = []
    for imagePath in imagePaths:
        try:
            pilImage = Image.open(imagePath).convert("L")
            imageNp = np.array(pilImage, "uint8")
            Id = int(os.path.split(imagePath)[-1].split("_")[1])
            faces.append(imageNp)
            Ids.append(Id)
        except Exception as e:
            print(f"Skipping {imagePath} due to error: {e}")
    return faces, Ids
