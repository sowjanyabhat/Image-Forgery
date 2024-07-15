import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import os
import hashlib
from hashlib import sha3_256
import exifread
import socket
import pickle
import threading

# Function to calculate SHA-3 hash of an image


def calculate_sha3(image):
    hash_sha3 = sha3_256()
    block_size = 1024  # Define block size for processing image data

    # Absorb phase
    for block_start in range(0, len(image), block_size):
        block_end = min(block_start + block_size, len(image))
        block = image[block_start:block_end]
        hash_sha3.update(block)

    # Squeeze phase
    return hash_sha3.hexdigest()

# Function to detect forgery using SHA-3 and metadata analysis


def detect_forgery(original_image_path, test_image_path):
    if not os.path.exists(original_image_path) or not os.path.exists(test_image_path):
        return "Error: Please select both original and test images."

    # Read images using OpenCV.
    original_image = cv2.imread(original_image_path)
    test_image = cv2.imread(test_image_path)

    if original_image is None or test_image is None:
        return "Error: Error loading images. Please make sure the selected files are valid images."

    # Calculate SHA-3 hashes of the images before and after modifications.
    original_sha3 = calculate_sha3(original_image)
    test_sha3 = calculate_sha3(test_image)

    # Compare SHA-3 hashes to detect forgery.
    if original_sha3 == test_sha3:
        return f"No forgery detected.\n\nOriginal image SHA-3 hash: {original_sha3}\nTest image SHA-3 hash: {test_sha3}"
    else:
        # Check if dimensions are different
        if original_image.shape != test_image.shape:
            return f"Forgery detected: Dimensional change.\n\nOriginal image SHA-3 hash: {original_sha3}\nTest image SHA-3 hash: {test_sha3}"
        else:
            # Compute absolute difference between images
            diff = cv2.absdiff(original_image, test_image)
            if cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)) > 0:
                return f"Forgery detected: Image content modification.\n\nOriginal image SHA-3 hash: {original_sha3}\nTest image SHA-3 hash: {test_sha3}"
            else:
                # Perform metadata analysis
                original_metadata = get_image_metadata(original_image_path)
                test_metadata = get_image_metadata(test_image_path)

                if original_metadata != test_metadata:
                    return f"Forgery detected: Metadata mismatch.\n\nOriginal image SHA-3 hash: {original_sha3}\nTest image SHA-3 hash: {test_sha3}"
                else:
                    return f"Forgery detected: Unidentified modification.\n\nOriginal image SHA-3 hash: {original_sha3}\nTest image SHA-3 hash: {test_sha3}"

# Function to extract metadata from an image


def get_image_metadata(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        metadata = {}
        for tag in tags:
            metadata[tag] = tags[tag]
        return metadata

# Function to select the original image file


def select_original_image():
    original_image_path = filedialog.askopenfilename(
        title="Select Original Image", filetypes=[("Image files", ".jpg;.jpeg;*.png")])
    if original_image_path:
        original_image_entry.delete(0, tk.END)
        original_image_entry.insert(0, original_image_path)

# Function to select the test image file


def select_test_image():
    test_image_path = filedialog.askopenfilename(
        title="Select Test Image", filetypes=[("Image files", ".jpg;.jpeg;*.png")])
    if test_image_path:
        test_image_entry.delete(0, tk.END)
        test_image_entry.insert(0, test_image_path)

# Function to handle forgery detection


def handle_forgery_detection():
    original_image_path = original_image_entry.get()
    test_image_path = test_image_entry.get()

    result = detect_forgery(original_image_path, test_image_path)
    result_label.config(text=result)

    # Sending result to the server
    threading.Thread(target=send_result_to_server, args=(result,)).start()

# Function to send the result to the server


# Function to send the result to the server
def send_result_to_server(result, server_ip):
    HOST = server_ip  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(result))
    except ConnectionRefusedError:
        print("Connection refused by the server. Please ensure the server is running.")

# Function to handle forgery detection


def handle_forgery_detection():
    original_image_path = original_image_entry.get()
    test_image_path = test_image_entry.get()

    result = detect_forgery(original_image_path, test_image_path)
    result_label.config(text=result)

    # Sending result to the server
    threading.Thread(target=send_result_to_server,
                     args=(result, server_ip)).start()


# Server IP address
server_ip = input("Enter server IP address: ")

# Create Tkinter window
root = tk.Tk()
root.title('Image Forgery Detector')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize the background image to fit the screen
background_image = Image.open("background.png")
background_image = background_image.resize((screen_width, screen_height))
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for other widgets with a light blue background
frame = tk.Frame(root, bg="#e0f2f1", bd=5)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Heading label
heading_label = tk.Label(
    frame, text="Image Forgery Detector", bg="#e0f2f1", font=("Rockwell", 24))
heading_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create buttons and labels for file selection
original_image_label = tk.Label(
    frame, text="Original Image:", bg="#e0f2f1", font=("Rockwell", 16))
original_image_label.grid(row=1, column=0, padx=10)

original_image_entry = tk.Entry(frame, font=("Rockwell", 16))
original_image_entry.grid(row=1, column=1, padx=10)

original_image_button = tk.Button(
    frame, text="Select", command=select_original_image, font=("Rockwell", 14))
original_image_button.grid(row=1, column=2, padx=10)

test_image_label = tk.Label(
    frame, text="Test Image:", bg="#e0f2f1", font=("Rockwell", 16))
test_image_label.grid(row=2, column=0, padx=10)

test_image_entry = tk.Entry(frame, font=("Rockwell", 16))
test_image_entry.grid(row=2, column=1, padx=10)

test_image_button = tk.Button(
    frame, text="Select", command=select_test_image, font=("Rockwell", 14))
test_image_button.grid(row=2, column=2, padx=10)

# Create a button to trigger forgery detection with a green background
detect_button = tk.Button(frame, text='Detect Forgery', command=handle_forgery_detection,
                          bg="#4caf50", fg="white", font=("Rockwell", 18), padx=10, pady=5, borderwidth=0)
detect_button.grid(row=3, column=0, columnspan=3, pady=20)

# Label to display the result
result_label = tk.Label(frame, text="", bg="#e0f2f1", font=("Rockwell", 18))
result_label.grid(row=4, column=0, columnspan=3, pady=10)

# Start the Tkinter event loop
root.mainloop()
