import tkinter as tk
from tkinter import filedialog, ttk
from face_recognition_util import load_known_faces, compare_faces
from image_util import resize_image, cv2_to_pil
from gui_util import create_popup_window, create_canvas

KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        self.canvas = create_canvas(root, 800, 600)

        self.btn_browse = ttk.Button(root, text="Browse Image", command=self.browse_image)
        self.btn_browse.pack(pady=10)

        self.image_path = None
        self.known_faces, self.known_names = load_known_faces()

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=("Helvetica", 14))
        self.listbox.pack(pady=10)

        self.label_result = tk.Label(root, text="Result: ", font=("Helvetica", 12, "bold"))
        self.label_result.pack(pady=5)

        self.listbox.bind("<ButtonRelease-1>", self.show_large_face_from_listbox)

        self.popup_window = None

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                      filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.process_image()

    def show_large_face_from_listbox(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            if selected_index < len(self.known_faces):
                selected_face = self.known_faces[selected_index]
                self.show_large_face(selected_face)

    def show_large_face(self, face_encoding):
        if self.popup_window:
            self.popup_window.destroy()

        self.popup_window = create_popup_window(self.root, "Large Face", 400, 400)
        face_image = extract_face_from_encoding(face_encoding)
        face_image = cv2_to_pil(face_image)
        face_image = face_image.resize((400, 400))
        face_photo = ImageTk.PhotoImage(face_image)
        canvas = create_canvas(self.popup_window, 400, 400)
        canvas.create_image(0, 0, anchor=tk.NW, image=face_photo)
        canvas.image = face_photo

    def extract_face_from_encoding(self, face_encoding):
        face_encoding = np.asarray(face_encoding).reshape(2, -2)
        face_image = face_recognition.load_image_file(self.image_path)
        face_locations = face_recognition.face_locations(face_image, model=MODEL)

        if not face_locations:
            return None

        face_location = face_locations[0]
        top, right, bottom, left = face_location
        face_image = face_image[top:bottom, left:right]

        if not face_image.any():
            return None

        face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
        return face_image

    def process_image(self):
        if self.image_path:
            image = face_recognition.load_image_file(self.image_path)
            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)

            self.listbox.delete(0, tk.END)

            for face_encoding, face_location in zip(encodings, locations):
                results = compare_faces(self.known_faces, face_encoding)
                match = "Unknown"

                if True in results:
                    match = self.known_names[results.index(True)]
                    self.listbox.insert(tk.END, match)

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                color = name_to_color(match)

                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), FONT_THICKNESS)

            image = resize_image(image, (800, 600))
            image = cv2_to_pil(image)
            image = ImageTk.PhotoImage(image)

            self.canvas.delete("all")
            self.canvas.config(width=800, height=600)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image

            if self.listbox.size() > 0:
                selected_name = self.listbox.get(tk.ACTIVE)
                self.label_result.config(text=f"Result: {selected_name}", fg="green")
            else:
                self.label_result.config(text="Result: Unknown", fg="red")

    def name_to_color(self, name):
        color = hash(name) % 0xFFFFFF
        color = tuple(int(format(color, '06x')[i:i+2], 16) for i in (0, 2, 4))
        return color

if __name__ == "__main__":
    root = tk.Tk
