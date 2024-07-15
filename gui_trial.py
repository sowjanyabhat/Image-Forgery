import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from trial import detect_forgery

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
