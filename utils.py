from deepface import DeepFace
import numpy as np
import cv2

# Improved embedding extraction with preprocessing
def extract_face_embedding(image_path, target_size=(160, 160)):
    try:
        # Preprocess image (convert to RGB if needed)
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Image not loaded properly")
            
        # Convert to RGB if needed
        if len(img.shape) == 2:  # Grayscale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:  # RGBA
            img = img[:, :, :3]
            
        # Get embeddings
        embedding_objs = DeepFace.represent(
            img_path=img,
            model_name='Facenet512',
            detector_backend='retinaface',  # More accurate than default
            enforce_detection=True,
            align=True  # Crucial for good recognition
        )
        
        if embedding_objs and isinstance(embedding_objs, list):
            return np.array(embedding_objs[0]['embedding'])
            
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
    return None

# Better comparison with adjustable threshold
def compare_embeddings(embedding1, embedding2, threshold=0.5):
    if embedding1 is None or embedding2 is None:
        return False, 0.0
        
    # Cosine similarity calculation
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    similarity = (similarity + 1) / 2  # Convert from [-1,1] to [0,1] range
    return similarity > threshold, similarity

# Example with multiple test cases
if __name__ == "__main__":
    test_cases = [
        ("image_1.jpg", "image_2.jpg", True),  # Same person different photo
        ("image_1.jpg", "Taylor Swift.jpg", False),       # Different people
        ("images (3).jfif", "images (3).jpg", True) # Same person cropped
    ]
    
    for img1, img2, should_match in test_cases:
        emb1 = extract_face_embedding(img1)
        emb2 = extract_face_embedding(img2)
        
        if emb1 is None:
            print(f"Could not detect face in {img1}")
            continue
        if emb2 is None:
            print(f"Could not detect face in {img2}")
            continue
            
        is_match, confidence = compare_embeddings(emb1, emb2)
        
        result = "✅" if is_match == should_match else "❌"
        print(f"{img1} vs {img2}: Match={is_match} (Confidence: {confidence:.2f}) {result}")