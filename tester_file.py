import os
import face_recognition
import cv2

# Directories create karte hai.
event_photos_dir = 'PUT UR EVENT PHOTOS DIR HERE'
known_faces_dir = 'PUT UR KNOWN FACES DIR HERE'
sorted_photos_dir = 'PUT UR SORTED PHOTOS DIR HERE'
os.makedirs(sorted_photos_dir, exist_ok=True)

#ab lets make the lists for enmbeddings and face names. 
known_face_embeddings = []
known_face_names = []

for image_path in os.listdir(known_faces_dir):
    if image_path.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, image_path))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_embeddings.append(encoding[0])
            known_face_names.append(os.path.splitext(image_path)[0])
# print(known_face_embeddings)

# Making a Tolerance Parameter for Adjustments.
tolerance = 0.5 

# Ab Chalo event photos pe aate hai.
for image_path in os.listdir(event_photos_dir):
    if image_path.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(event_photos_dir, image_path))
        face_locations = face_recognition.face_locations(image)
        face_embeddings = face_recognition.face_encodings(image, face_locations)

        for face_embeddings, face_location in zip(face_embeddings, face_locations):
            matches = face_recognition.compare_faces(known_face_embeddings, face_embeddings, tolerance)
            name = "IDK"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                cv2.imwrite(os.path.join(sorted_photos_dir, f"{name}_{image_path}"), face_image)