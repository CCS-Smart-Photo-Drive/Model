import os
import face_recognition
import cv2
from concurrent.futures import ThreadPoolExecutor

# Directories create karte hai.
event_photos_dir = 'PUT UR EVENT PHOTOS DIR HERE'
known_faces_dir = 'PUT UR KNOWN FACES DIR HERE'
sorted_photos_dir = 'PUT UR SORTED PHOTOS DIR HERE'
os.makedirs(sorted_photos_dir, exist_ok=True)

# Function to process known faces
def process_known_face(image_path):
    if image_path.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, image_path))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            return encoding[0], os.path.splitext(image_path)[0]
    return None, None

# Process known faces in parallel
known_face_embeddings = []
known_face_names = []
with ThreadPoolExecutor() as executor:
    results = executor.map(process_known_face, os.listdir(known_faces_dir))
    for encoding, name in results:
        if encoding:
            known_face_embeddings.append(encoding)
            known_face_names.append(name)

# Making a Tolerance Parameter for Adjustments.
tolerance = 0.5 

# Function to process event photos
def process_event_photo(image_path):
    if image_path.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(event_photos_dir, image_path))
        face_locations = face_recognition.face_locations(image)
        face_embeddings = face_recognition.face_encodings(image, face_locations)

        for face_embedding, face_location in zip(face_embeddings, face_locations):
            matches = face_recognition.compare_faces(known_face_embeddings, face_embedding, tolerance)
            name = "IDK"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                cv2.imwrite(os.path.join(sorted_photos_dir, f"{name}_{image_path}"), face_image)

# Process event photos in parallel
batch_size = 1000  # Adjust batch size based on your system's memory capacity
event_photos = os.listdir(event_photos_dir)
for i in range(0, len(event_photos), batch_size):
    batch = event_photos[i:i + batch_size]
    with ThreadPoolExecutor() as executor:
        executor.map(process_event_photo, batch)