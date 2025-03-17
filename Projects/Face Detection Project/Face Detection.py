import cv2

class FaceDetector:
    def __init__(self, camera_index=0, width=640, height=480):
        """
        Initialize the FaceDetector with the specified camera index and resolution.
        """
        # Load the pre-trained Haar Cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize the webcam
        self.camera = cv2.VideoCapture(camera_index)
        
        # Set camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        if not self.camera.isOpened():
            raise Exception("Error: Could not open the camera.")
        
        print("FaceDetector initialized. Press 'q' to exit.")
    
    def detect_faces(self, frame):
        """
        Detect faces in the given frame.
        :param frame: The frame to process.
        :return: List of bounding boxes for detected faces.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces

    def run(self):
        """
        Start the face detection loop.
        """
        while True:
            # Capture frame-by-frame
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            # Detect faces
            faces = self.detect_faces(frame)
            
            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Display the resulting frame
            cv2.imshow('Face Detection', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cleanup()
    
    def cleanup(self):
        """
        Release the camera and close all windows.
        """
        self.camera.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed.")

# Instantiate and run the FaceDetector
if __name__ == "__main__":
    face_detector = FaceDetector()
    face_detector.run()