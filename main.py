import tkinter as tk
import util
import cv2
import os
import subprocess  # is used to run external commands and interact with the OS.
from PIL import Image, ImageTk  # converting any formats(as in arrays, etc) into Image format; ImageTk=> used to convert PIL images into a format that Tkinter can display.

class App:
    def __init__(self):  # constructor
        self.main_window = tk.Tk()  # creating out our main window using/in tkinter!
        self.main_window.geometry("1200x520+350+100")  # Defining size of the window (1200x520) with x and y values

        self.login_button_main_window = util.get_button(self.main_window, 'LOGIN', "blue", self.login)  # creating login button inside the window with text LOGIN in Blue color which functions login
        self.login_button_main_window.place(x=750, y=300)  # Place of the Login button in Window

        self.webcam_label = util.get_img_label(self.main_window)  # Create a label to display webcam footage
        self.webcam_label.place(x=10, y=0, width=700, height=400)

        self.add_cam(self.webcam_label)  # adding our cam inside the label

        # creating a db directory to store images.
        self.db_dir = './db'

        if not os.path.exists(self.db_dir):  # If the directory doesn't exist then we are creating it
            os.mkdir(self.db_dir)

    def start(self):
        self.main_window.mainloop()  # inner loop to run our app each time we open the window.

    def login(self):
        unknown_img_path = './.tmp.jpg'  # Temporary image file for face recognition processing

        # Capture the current frame as an image file for face recognition processing
        cv2.imwrite(unknown_img_path, self.recent_capture_arr)

        # Run face recognition to match the temporary image with the database
        try:
            output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]).decode('utf-8').strip()
            print(f"Face recognition output: {output}")  # Debugging
            if ',' in output:
                name = output.split(',')[1].strip()  # Extract the user's name from the recognition output
            else:
                name = "unknown_person"
        except Exception as e:
            print(f"Error during face recognition: {e}")
            name = "unknown_person"  # Default to unknown if there's an error

        print(f"Extracted name: {name}")  # Debugging

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('OOPS!', 'Unknown Admin. This page is only for Admins')
        else:
            util.msg_box('WELCOME BACK!!', 'Welcome, {}'.format(name))

            # Open the voter data file
            os.system('open voting_data.txt')  # macOS

            # Close the current window
            self.main_window.destroy()

        # Clean up the temporary image
        os.remove(unknown_img_path)

    def add_cam(self, label):  # label as well because we'll be putting the webcam into this
        if 'cap' not in self.__dict__:  # asks Dictionary if variable created, if not then it creates
            self.cap = cv2.VideoCapture(0)  # Accessing the system's webcam (i.e., the full webcam is accessed by putting 0 in it)

        self._label = label
        self.process_cam()  # function used to put the webcam into the label

    def process_cam(self):  # used to read frames from cam and put the frames into the label
        ret, frame = self.cap.read()
        self.recent_capture_arr = frame
        img = cv2.cvtColor(self.recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.recent_capture_pil = Image.fromarray(img)  # converting the img to PILLOW
        imgtk = ImageTk.PhotoImage(image=self.recent_capture_pil)  # putting the frames into the label (i.e., converting to ImageTK)

        self._label.imgtk = imgtk  # storing reference to avoid garbage collection
        self._label.configure(image=imgtk)  # till here we are putting only 1 single frame into the webcam, so =>
        self._label.after(20, self.process_cam)  # after 20 milliseconds, we call this function again and again, to make the single frames as streaming a video (converting frames to video)

if __name__ == "__main__":
    app = App()
    app.start()  # calling the start method to display the window
