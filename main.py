"""
MAIN GUI FILE

RESPONSIBLE FOR USER INTERFACE AND ALLOWING USER INTERACTION WITH THE MODEL
BUILT OFF TKINTER
BHAVYA PATEL 2024

"""

# API IMPORT
import mnistPrediction as mp

# OS IMPORT
import os
import time  # For checking new files

# TKINTER IMPORTS
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Label

# PIL
from PIL import ImageTk, Image, ImageFilter

"""
FUNCTIONS

- for each button and stuff
"""

def exit_program():
    root.quit()  # Closes the application

def delete_files_in_directory():
    try:
        files = os.listdir("./normalizedImgStorage")
        for file in files:
            file_path = os.path.join("./normalizedImgStorage", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")
    
def select_file():
    file_paths = filedialog.askopenfilenames(title="Select Image File")
    if file_paths:
        for paths in file_paths:
            #messagebox.showinfo("Files Selected", "\n".join(paths)) // testing
            messagebox.showinfo("File succesfully found!", "File Predicted as: " + str(mp.predict(mp.noramlize(str(paths)), str(paths))))

def select_folder():
    folder_path = filedialog.askdirectory(title="Select Folder of Images")
    if folder_path:
        for paths in os.listdir(folder_path):
            #messagebox.showinfo("Files Selected", "\n".join(paths)) // testing
            tk.Text(root, height=50,width=50)
            messagebox.showinfo("File succesfully found!", "File Predicted as: " + str(
                mp.predict(
                    mp.noramlize(folder_path + "/"+ str(paths)),folder_path + "/"+  str(paths)
                )
            ))

# Global variables for cycling through images
current_index = 0
pathsNorm = []
last_checked_time = 0

def displayImg():
    """Populate the list of image paths from './normalizedImgStorage'."""
    global pathsNorm, current_index
    pathsNorm = []  # Reset image paths
    img_folder = "./normalizedImgStorage"  # Specify the folder for normalized images

    # Populate pathsNorm with image file paths
    for filename in os.listdir(img_folder):
        imgPath = os.path.join(img_folder, filename)
        if os.path.isfile(imgPath) and filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            pathsNorm.append(imgPath)

    if pathsNorm:
        current_index = 0  # Start from the first image
        show_image(pathsNorm[current_index])

def show_image(imgPath):
    """Display the image located at imgPath."""
    img = Image.open(imgPath)
    img = img.resize((250, 250))  # Removed Image.ANTIALIAS, not needed for modern versions of PIL

    # Convert image to format tkinter can use
    img_display = ImageTk.PhotoImage(img)

    # Update the image label
    image_label.config(image=img_display)
    image_label.image = img_display

    # Update the caption label
    caption_label.config(text=f"Displaying: {os.path.basename(imgPath)}")

def next_image():
    """Show the next image in the pathsNorm list."""
    global current_index
    if pathsNorm:
        current_index = (current_index + 1) % len(pathsNorm)  # Cycle to the next image
        show_image(pathsNorm[current_index])

def prev_image():
    """Show the previous image in the pathsNorm list."""
    global current_index
    if pathsNorm:
        current_index = (current_index - 1) % len(pathsNorm)  # Cycle to the previous image
        show_image(pathsNorm[current_index])

def refresh_directory():
    """Check for new images in the folder and refresh the list of images."""
    global last_checked_time, pathsNorm

    # Get the current time
    current_time = time.time()

    # Check for any new files in the directory since the last time it was checked
    img_folder = "./normalizedImgStorage"
    new_files_found = False

    for filename in os.listdir(img_folder):
        imgPath = os.path.join(img_folder, filename)
        # Check if it's a new file (modified after last check)
        if os.path.isfile(imgPath) and filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if os.path.getmtime(imgPath) > last_checked_time:
                pathsNorm.append(imgPath)
                new_files_found = True

    if new_files_found:
        messagebox.showinfo("New Files", "New images found! Displaying the first one now.")
        show_image(pathsNorm[-1])  # Display the most recently added image
        last_checked_time = current_time  # Update last checked time

"""
ROOT CODE

- bulk of the root application
- definition of buttons and main features currently available
"""

root = tk.Tk()
root.title("MNIST Classification")
root.geometry("800x600")  # Adjusted to be more manageable

# Create a file select button and place it on the window
file_button = tk.Button(root, text="Select Files", command=select_file)
file_button.pack(pady=10)

# Create a folder directory select button and place it on the window
folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.pack(pady=10)

# Create an exit button and place it on the window
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack(pady=10)

# Create a delete files button and place it on the window
# Deletes ./normalizedImgStorage files, clears them
exit_button = tk.Button(root, text="Clear Normalized Images", command=delete_files_in_directory)
exit_button.pack(pady=10)


# Create a button for displaying Normalized Images
normalized_images_button = tk.Button(root, text="Show Normalized Images", command=displayImg)
normalized_images_button.pack(pady=10)

# Create "Next" and "Previous" buttons for cycling through images
prev_button = tk.Button(root, text="Previous", command=prev_image)
prev_button.pack(side="left", padx=10, pady=10)

next_button = tk.Button(root, text="Next", command=next_image)
next_button.pack(side="right", padx=10, pady=10)

# Create a button for refreshing the directory to look for new images
refresh_button = tk.Button(root, text="Refresh Directory", command=refresh_directory)
refresh_button.pack(pady=10)

# Create a label for displaying images and captions
image_label = Label(root)
image_label.pack(pady=20, expand=True)

# Label for all the captions
caption_label = Label(root, text="", font=("Helvetica", 12))
caption_label.pack(pady=10)

# Run the application
root.mainloop()
