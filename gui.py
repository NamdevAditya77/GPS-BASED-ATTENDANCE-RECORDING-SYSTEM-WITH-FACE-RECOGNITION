import tkinter as tk
from tkinter import messagebox
import geopy.distance
import requests
import subprocess
import threading

# Function to calculate distance between two GPS coordinates
def calculate_distance(coord1, coord2):
    return geopy.distance.distance(coord1, coord2).meters

# Function to get the current coordinates of the device
def get_current_coordinates():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        lat, lon = map(float, data['loc'].split(','))
        return (lat, lon)
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None

# Function to fetch and display teacher's coordinates
def fetch_teacher_coordinates():
    teacher_coords = get_current_coordinates()

    if teacher_coords is None:
        messagebox.showerror("Error", "Could not fetch coordinates.")
        return

    formatted_teacher_coords = f"({teacher_coords[0]:.8f}, {teacher_coords[1]:.8f})"
    label_teacher_coords.config(text=f"Teacher Coordinates: {formatted_teacher_coords}")

    button_fetch_student_coords.config(state=tk.NORMAL)

# Function to fetch and display student's coordinates
def fetch_student_coordinates():
    student_coords = get_current_coordinates()

    if student_coords is None:
        messagebox.showerror("Error", "Could not fetch coordinates.")
        return

    formatted_student_coords = f"({student_coords[0]:.8f}, {student_coords[1]:.8f})"
    label_student_coords.config(text=f"Student Coordinates: {formatted_student_coords}")

    button_mark_attendance.config(state=tk.NORMAL)

# Function to run facial recognition script
def run_facial_recognition():
    subprocess.run(["python", "main.py"])

# Function to show loading animation
def show_loading_animation(frames):
    def animate(frame_index=0):
        if facial_recognition_thread and not facial_recognition_thread.is_alive():
            loading_label.config(image='')
            return

        frame = frames[frame_index]
        loading_label.config(image=frame)
        frame_index = (frame_index + 1) % len(frames)
        root.after(100, animate, frame_index)  # Update every 100ms
    animate()

# Function to mark attendance
def mark_attendance():
    try:
        teacher_coords = label_teacher_coords.cget("text")
        student_coords = label_student_coords.cget("text")

        if teacher_coords == "Teacher Coordinates: Not fetched":
            messagebox.showerror("Error", "Teacher coordinates not set.")
            return

        if student_coords == "Student Coordinates: Not fetched":
            messagebox.showerror("Error", "Student coordinates not fetched.")
            return

        teacher_coords = eval(teacher_coords.split(":")[1])
        student_coords = eval(student_coords.split(":")[1])

        # Calculate the distance
        distance = calculate_distance(teacher_coords, student_coords)

        # Check if the student is within 25 meters
        if distance <= 25:
            # Start loading animation
            show_loading_animation(loading_frames)

            # Run facial recognition script in a separate thread
            global facial_recognition_thread
            facial_recognition_thread = threading.Thread(target=run_facial_recognition)
            facial_recognition_thread.start()
        else:
            messagebox.showinfo("Attendance Status", "Student is not within the required range.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the GUI window
root = tk.Tk()
root.title("Attendance System")

# Calculate window size and position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height
geometry_string = f"{window_width}x{window_height}"
root.geometry(geometry_string)

# Set background image
bg_image = tk.PhotoImage(file="Resources/window.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create labels for teacher and student coordinates
label_teacher_coords = tk.Label(root, text="Teacher Coordinates: Not fetched", font=('Times New Roman', 30, 'bold'))
label_teacher_coords.place(y=200, relx=0.5, rely=0.2, anchor="center")

label_student_coords = tk.Label(root, text="Student Coordinates: Not fetched", font=('Times New Roman', 30, 'bold'))
label_student_coords.place(y=175, relx=0.5, rely=0.3, anchor="center")

# Create buttons to fetch coordinates and mark attendance
button_fetch_teacher_coords = tk.Button(root, text="Fetch Teacher Coordinates", command=fetch_teacher_coordinates, font=('Times New Roman', 30, 'bold'), activebackground="red")
button_fetch_teacher_coords.place(y=160, relx=0.5, rely=0.4, anchor="center")

button_fetch_student_coords = tk.Button(root, text="Fetch Student Coordinates", command=fetch_student_coordinates, state=tk.DISABLED, font=('Times New Roman', 30, 'bold'), activebackground="red")
button_fetch_student_coords.place(y=160, relx=0.5, rely=0.5, anchor="center")

button_mark_attendance = tk.Button(root, text="Mark Attendance", command=mark_attendance, state=tk.DISABLED, font=('Times New Roman', 30, 'bold'), activebackground="black", activeforeground="white")
button_mark_attendance.place(y=160, relx=0.5, rely=0.6, anchor="center")

# Create a loading label
loading_label = tk.Label(root, text="")
loading_label.place(y=220, relx=0.5, rely=0.7, anchor="center")

# Load the animation frames
loading_frames = [tk.PhotoImage(file=f"frames/{i}.png") for i in range(1, 31)]

# Initialize the facial recognition thread variable
facial_recognition_thread = None

root.mainloop()
