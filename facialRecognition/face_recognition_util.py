import os
import face_recognition

KNOWN_FACES_DIR = 'known_faces'
TOLERANCE = 0.6
MODEL = 'cnn'

def load_known_faces():
    faces = []
    names = []
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
            image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
            encoding = face_recognition.face_encodings(image)[0]
            faces.append(encoding)
            names.append(name)
    return faces, names

def compare_faces(known_faces, unknown_face_encoding):
    return face_recognition.compare_faces(known_faces, unknown_face_encoding, TOLERANCE)
