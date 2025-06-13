
# Face Recognition Attendance Management System

A Python-based attendance management system using face recognition technology with OpenCV and Tkinter GUI.

## Features

- **Face Registration**: Register new students/employees with their photos
- **Real-time Face Recognition**: Automatic attendance marking using webcam
- **Training Module**: Train the face recognition model with collected images
- **Attendance Tracking**: View and manage attendance records
- **User-friendly GUI**: Simple Tkinter-based interface
- **Data Export**: Export attendance data to CSV/Excel

## Technologies Used

- **Python 3.9+**
- **OpenCV**: Computer vision and face recognition
- **Tkinter**: GUI framework
- **NumPy**: Numerical operations
- **Pandas**: Data manipulation (if used)
- **PIL (Pillow)**: Image processing

## Prerequisites

Before running this project, make sure you have:

- Python 3.7 or higher installed
- Webcam connected to your computer
- Required Python packages (see Installation)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/attendance-management-face-recognition.git
   cd attendance-management-face-recognition
   ```

2. **Install required packages**
   ```bash
   pip install opencv-contrib-python
   pip install numpy
   pip install pillow
   pip install pandas
   ```

3. **Download Haar Cascade file** (if not included)
   - Download `haarcascade_frontalface_default.xml` from OpenCV GitHub repository
   - Place it in the project root directory

## Usage

1. **Run the main application**
   ```bash
   python attendance.py
   ```

2. **Register New Person**
   - Click "Take Images" button
   - Enter ID and Name
   - Look at the camera and press 's' to capture images
   - Press 'q' to quit after capturing enough images

3. **Train the Model**
   - Click "Train Images" after registering people
   - Wait for training to complete

4. **Take Attendance**
   - Click "Take Attendance"
   - Face the camera for automatic recognition
   - Attendance will be marked automatically

## Project Structure

```
attendance-management-face-recognition/
│
├── attendance.py              # Main application file
├── trainImage.py             # Training module
├── takeImage.py              # Image capture module
├── recognizer.py             # Face recognition module
├── TrainingImage/            # Directory for training images
├── TrainingImageLabel/       # Directory for trained models
├── haarcascade_frontalface_default.xml  # Haar cascade file
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Troubleshooting

### Common Issues:

1. **Camera not working**
   - Check if camera is connected and not used by other applications
   - Try changing camera index in code (0, 1, 2, etc.)

2. **cv2.face module error**
   ```bash
   pip uninstall opencv-python
   pip install opencv-contrib-python
   ```

3. **Permission errors**
   - Run as administrator (Windows) or use sudo (Linux/Mac)
   - Check camera privacy settings

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV community for computer vision libraries
- Python community for excellent documentation
- Contributors and testers

## Author
Jyoti Jais
GitHub: @jyotijais

Project Link: [https://github.com/YOUR_USERNAME/attendance-management-face-recognition](https://github.com/YOUR_USERNAME/attendance-management-face-recognition)

---

⭐ Star this repository if you found it helpful!
