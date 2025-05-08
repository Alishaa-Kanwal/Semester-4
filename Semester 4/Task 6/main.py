from flask import Flask, render_template, request
import os, cv2, torch, numpy as np
import mediapipe as mp
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

model = YOLO("yolov8x.pt")
herd_classes = {"dog", "cat", "goat", "cow", "sheep", "giraffe"}

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

def detect_animals(image_path):
    img = preprocess_image(image_path)
    results = model(img)
    detected_animals = {}

    for box in results[0].boxes.data:
        x1, y1, x2, y2, score, class_id = box.tolist()
        class_name = model.names[int(class_id)]
        if class_name in herd_classes:
            detected_animals[class_name] = detected_animals.get(class_name, 0) + 1
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, f"{class_name}", (int(x1), int(y1)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    result_path = os.path.join(app.config['RESULT_FOLDER'], os.path.basename(image_path))
    cv2.imwrite(result_path, img)
    return result_path, detected_animals

def extract_facial_features(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            for landmark in landmarks.landmark:
                h, w, _ = img.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(img, (x, y), 1, (0, 0, 255), -1)

    face_result_path = os.path.join(app.config['RESULT_FOLDER'], 'face_' + os.path.basename(image_path))
    cv2.imwrite(face_result_path, img)
    return face_result_path if results.multi_face_landmarks else None

def generate_coordinates():
    base_lat, base_lon = 31.5204, 74.3587
    return {
        "lat": base_lat + np.random.uniform(-0.05, 0.05),
        "lon": base_lon + np.random.uniform(-0.05, 0.05)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return 'No file selected', 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        result_path, detected_herds = detect_animals(file_path)
        extract_facial_features(file_path)

        herd_found = any(count >= 2 for count in detected_herds.values())
        coords = generate_coordinates() if herd_found else None

        return render_template('index.html',
                               result_image=result_path,
                               herds=detected_herds,
                               found=herd_found,
                               coords=coords,
                               no_herd_message=None if herd_found else "No animal herd detected.")

    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)
