from flask import Flask, request, jsonify
from utils import extract_face_embedding, compare_embeddings
import os
import cv2
import numpy as np

app = Flask(__name__)

# Endpoint to register a new face
@app.route('/register', methods=['POST'])
def register_face():
    image = request.files['image']
    name = request.form['name']
    path = f"known_faces/{name}.jpg"
    image.save(path)
    return jsonify({"message": f"Face saved for {name}"}), 200

# Endpoint to recognize a face
@app.route('/recognize', methods=['POST'])
def recognize_face():
    image = request.files['image']
    img_bytes = image.read()

    # Load known faces
    known_faces_dir = os.path.join(os.path.dirname(__file__), "known_faces")
    known_embeddings = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            known_img = cv2.imread(os.path.join(known_faces_dir, filename))
            embedding = extract_face_embedding(known_img)
            if embedding is not None:
                known_embeddings.append(embedding)
                known_names.append(filename.split('.')[0])

    # Process input image
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    input_embedding = extract_face_embedding(frame)

    # Compare embeddings
    match_name = "Unknown"
    if input_embedding is not None:
        for known_embedding, name in zip(known_embeddings, known_names):
            distance = np.linalg.norm(input_embedding - known_embedding)
            if distance < 0.6:  # Threshold
                match_name = name
                break

    return jsonify({"match": match_name})

if __name__ == '__main__':
    app.run(debug=True)
