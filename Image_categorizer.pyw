import tkinter as tk
from tkinter import filedialog
import cv2
import pytesseract
import os
import shutil
import numpy as np
import threading

class ImageCategorizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Categorizer")
        self.root.geometry("600x400")  # Set window size
        self.input_dir = ""
        self.processing = True  # Flag to control processing
        
        self.create_widgets()
        
        self.total_files = 0
        self.processed_files = 0
    
    def create_widgets(self):
        self.select_dir_button = tk.Button(self.root, text="Select Input Directory", command=self.select_directory)
        self.select_dir_button.pack(pady=(30,10))
        
        self.input_dir_label = tk.Label(self.root, text="Input Directory:")
        self.input_dir_label.pack(pady=(10, 0))
        
        self.dir_path_text = tk.Entry(self.root, width=80)
        self.dir_path_text.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Start Categorizing", command=self.start_categorizing, state=tk.DISABLED)
        self.start_button.pack(pady=(20, 10))  # Adjusted space between button and status label
        
        self.stop_button = tk.Button(self.root, text="STOP", command=self.stop_categorizing, bg='red', fg='white')
        self.stop_button.pack(pady=(20, 20))  # Add space below the STOP button
        
        self.status_label = tk.Label(self.root, text="Status:")
        self.status_label.pack(pady=(10, 0))
        
        self.status_text = tk.Label(self.root, text="Select a directory to start processing.")
        self.status_text.pack(pady=10)
    
    def select_directory(self):
        # Open a directory selection dialog
        self.input_dir = filedialog.askdirectory()
        if self.input_dir:
            self.total_files = len([f for f in os.listdir(self.input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))])
            self.processed_files = 0
            self.dir_path_text.delete(0, tk.END)
            self.dir_path_text.insert(0, self.input_dir)
            self.status_text.config(text=f"Selected directory: {self.input_dir}")
            self.start_button.config(state=tk.NORMAL)  # Enable the start button
    
    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def detect_text(self, image):
        gray = self.preprocess_image(image)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        text_boxes = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 50:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                text_boxes.append((x, y, w, h))
        return data, text_boxes

    def detect_faces(self, image):
        face_cascades = [
            cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"),
            cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"),
            cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"),
            cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
        ]
        
        faces_detected = []
        
        for face_cascade in face_cascades:
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > 0:
                faces_detected.extend(faces)
        
        faces_detected = np.array(faces_detected)
        faces_detected = np.unique(faces_detected, axis=0)
        
        return faces_detected

    def categorize_image(self, image_path):
        image = cv2.imread(image_path)
        faces = self.detect_faces(image)
        data, _ = self.detect_text(image)
        
        confidence_threshold = 50  # Confidence level threshold
        
        # Initialize a variable to count characters
        filtered_text = ""
        specific_words = {"Shot", "On"}

        # Iterate through detected words and filter by confidence level
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            conf = int(data['conf'][i])
            text = data['text'][i]
            
            # Check if confidence is above the threshold and text is not empty
            if conf >= confidence_threshold and text.strip() != "":
                filtered_text += text + " "  # Add the text to the filtered text string

        text_length = len(filtered_text.strip())
        
        text_length_threshold = 20
        
        if len(faces) > 0 and text_length > 0:
        # Check if any specific words are in the detected text
            if any(word in filtered_text for word in specific_words):
                category = "People"
            else:
                if text_length < text_length_threshold:
                    category = "People"
                else:
                    category = "Meme"
        elif len(faces) > 0:
            category = "People"
        elif text_length > 0:
            category = "Meme"
        else:
            category = "Others"
        
        return category

    def copy_image(self, image_path, category_folder):
        filename = os.path.basename(image_path)
        shutil.copy(image_path, os.path.join(category_folder, filename))

    def process_images(self):
        if not self.input_dir:
            return

        memes_folder = "memes"
        people_folder = "people"
        others_folder = "others"

        os.makedirs(memes_folder, exist_ok=True)
        os.makedirs(people_folder, exist_ok=True)
        os.makedirs(others_folder, exist_ok=True)

        for filename in os.listdir(self.input_dir):
            if not self.processing:
                break
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image_path = os.path.join(self.input_dir, filename)
                
                if os.path.exists(image_path):
                    category = self.categorize_image(image_path)
                    
                    if category == "Meme":
                        self.copy_image(image_path, memes_folder)
                    elif category == "People":
                        self.copy_image(image_path, people_folder)
                    else:
                        self.copy_image(image_path, others_folder)
                    
                    self.processed_files += 1
                    # Schedule status update after processing a file
                    self.root.after(100, self.update_status)
                    print(f"Categorized {filename} as {category}")
                else:
                   print(f"{image_path} does not exist.")
        
        # Final update to status text
        self.processed_files = self.total_files
        self.root.after(100, self.update_status)

    def update_status(self):
        self.status_text.config(text=f"Processed {self.processed_files} out of {self.total_files} files.")
        if self.processed_files < self.total_files:
            self.root.after(1000, self.update_status)

    def start_categorizing(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.processing = True
        threading.Thread(target=self.process_images).start()
    
    def stop_categorizing(self):
        # Set processing flag to False to stop processing
        self.processing = False
        # Disable the stop button and enable the start button
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        # Update status to reflect stopping
        self.status_text.config(text="Processing stopped.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCategorizerApp(root)
    root.mainloop()
