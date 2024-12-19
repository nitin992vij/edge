import cv2
from flask import Flask, Response
import torch
 
# Initialize Flask app
app = Flask(__name__)
 
# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use yolov5s model, can replace with others
cap = cv2.VideoCapture(0)  # Open the default camera (change index for other cameras)
 
def generate_frames():
    while True:
        # Capture frame-by-frame
        success, frame = cap.read()
        if not success:
            break
 
        # Perform object detection
        results = model(frame)
 
        # Draw boxes and labels on the frame
        frame = results.render()[0]  # Render the results on the frame
 
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
 
        # Yield the frame to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
# Define the Flask route for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
# Main route to view the video stream
@app.route('/')
def index():
    return "<h1>YOLOv5 Camera Stream</h1><img src='/video_feed'>"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)