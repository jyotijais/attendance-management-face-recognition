import requests
import cv2
import numpy as np

url = "http://192.168.29.109:8080/shot.jpg"

print("Press 'q' to exit.")

while True:
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()  # Raises HTTPError for bad responses
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("IP Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break
    except requests.exceptions.RequestException as e:
        print("Failed to get frame:", e)
        break

cv2.destroyAllWindows()
