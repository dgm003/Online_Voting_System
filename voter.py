import tkinter as tk
import util
import cv2
import os
import subprocess#is used to run external commands and interact with the OS.
from PIL import Image,ImageTk# converting any formats(as in arrays,etc) into Image format;ImageTk=> used to convert PIL images into a format that Tkinter can display.

class App:
    def __init__(self): #constructor
        self.main_window=tk.Tk() #creating out our main window using/in tkinter!
        self.main_window.geometry("1200x520+350+100") #Defining size of the window(1200x520) with x nd y values

        #creating a set/database to track the users who have already voted
        self.voted_users = set()

        self.login_button_main_window=util.get_button(self.main_window,'LOGIN',"blue",self.login)#creating login button inside the window with text LOGIN in Blue color which fncts login
        self.login_button_main_window.place(x=750,y=300)#Place of the Login button in Window

        self.register_button_main_window=util.get_button(self.main_window,'REGISTER NEW USER',"grey",self.register,fg="black")#fg=>Foreground
        self.register_button_main_window.place(x=750,y=400)#Place of the Register button in Window

        self.webcam_label=util.get_img_label(self.main_window)# Create a label to display webcam footage
        self.webcam_label.place(x=10,y=0,width=700,height=400)

        self.add_cam(self.webcam_label) #adding our cam inside the label

        #creating a db directory to store images.
        self.db_dir='./votersdb'

        if not os.path.exists(self.db_dir): #If the directory doesnt exists then we r creating it
            os.mkdir(self.db_dir)


    def start(self):
        self.main_window.mainloop()#inner loop to run our app each time we open the window.

    def login(self):
        unkown_img_path='./.tmp.jpg' #to exectute the next command,we'll be needing a temp image,but on later stage, we'll not req, so we delete it
        
         # Capture the current frame as an image file for face recognition processing
        cv2.imwrite(unkown_img_path,self.recent_capture_arr)
        
        # Run face recognition to match the temporary image with the database,
        output=str(subprocess.check_output(['face_recognition',self.db_dir, unkown_img_path]))
        name=output.split(',')[1][:-5]# Extract the user's name from the recognition output

        if name in ['unknown_person','no_persons_found']:
            util.msg_box('OOPS!','Unknown User. Please register or try again')

        elif name in self.voted_users:
             util.msg_box('ALREADY VOTED!', f'Hi {name}, your vote has already been cast. Thank you!')
            
        else:
            util.msg_box('WELCOME BACK!!','Welcome,{}'.format(name))
            self.voted_users.add(name)  # Mark the user as having voted

            subprocess.Popen(["python", "tkinter_verifier.py"])
            self.main_window.destroy()


        os.remove(unkown_img_path)

    def register(self):
        self.register_window=tk.Toplevel(self.main_window)#creating the register window on clicking register button frm the main window
        self.register_window.geometry("1200x520+370+120")#here we kept x=370 y=120 so that it doesnt overlap with main window

        self.accept_button_register_window=util.get_button(self.register_window,'ACCEPT',"green",self.accept)#creating accept button inside the register window with text ACCEPT in green color which fncts login
        self.accept_button_register_window.place(x=750,y=300)#Place of the ACCEPT button in Window

        self.try_button_register_window=util.get_button(self.register_window,'TRY AGAIN',"red",self.try_again)#creating try again button inside the register window with text TRY in red color which fncts login
        self.try_button_register_window.place(x=750,y=400)#Place of the TRY AGAIN button in Window

        self.capture_label=util.get_img_label(self.register_window)#here we use capture_label, cz unlike in main window, here we dont need streaming video, but capturing a pic
        self.capture_label.place(x=10,y=0,width=700,height=400)

        self.add_img_to_label(self.capture_label)#adding a single captured image,not the stream/video

        self.entering_text_for_new_user=util.get_entry_text(self.register_window)
        self.entering_text_for_new_user.place(x=750, y=150)

        self.text_label_for_registration=util.get_text_label(self.register_window,'ENTER YOUR USERNAME:')
        self.text_label_for_registration.place(x=750, y=70)

    def add_img_to_label(self,label):#similar to the  process_cam() fnct, wr here it only takes the pic, instead of video
        imgtk=ImageTk.PhotoImage(image=self.recent_capture_pil)
        label.imgtk=imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture=self.recent_capture_arr.copy()#fnct used to capture the img of new user



    def accept(self):
        name=self.entering_text_for_new_user.get(1.0,"end-1c")#retrieves the text Entered by user in TEXT widget in Tkinter
    # where 1.0: This specifies the starting position from which to read the text. In Tkinter, text widgets are indexed by line and character position, where 1.0 refers to the first line, first character. 
    # "end-1c": This specifies the end position, but "end-1c" means "up to the end, minus one character." In Tkinter, end includes a trailing newline, so "end-1c" removes this extra newline and gives you just the actual text entered by the user.

        cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)),self.register_new_user_capture)
        #os.path.join constructs a file path by joining self.db_dir(dir where we have saved the Image) with filename.
        #'{}.jpg'.format(name) creates a string for the filename, where {} is replaced by the value of 'name'.eg=>Dhanush.jpg

        util.msg_box('SUCCESSFUL!','User Was Registered Successfully!')

        self.register_window.destroy()

    def try_again(self):
        self.register_window.destroy()#this fnct destroys the register window nd takes back to the main window.



#we'll be calling the foll fnct more than once, and everytime we can't create new object so created the loop
    def add_cam(self,label): #label as well cz we'll be putting the webcam into this 
        if 'cap' not in self.__dict__: #asks Dictionary if variable created, if not then it creates
            self.cap=cv2.VideoCapture(0) #Accessing the system's webcam(i.e the full webcam is accessed by putting 0 in it)

        self._label=label
        self.process_cam()#fnct used to put the webcam into the label

    def process_cam(self): #used to read frames frm cam nd put the frames into the label
        ret, frame=self.cap.read()
        self.recent_capture_arr=frame
        img=cv2.cvtColor(self.recent_capture_arr, cv2.COLOR_BGR2RGB) 
        self.recent_capture_pil=Image.fromarray(img)#converting the img to PILLOW
        imgtk=ImageTk.PhotoImage(image=self.recent_capture_pil)#putting the frames into the label(i.e converting to ImageTK)

        self._label.imgtk=imgtk#storing reference to avoid garbage collection
        self._label.configure(image=imgtk)#till here v r putting only 1 single frame into the webcam, so=>
        self._label.after(20,self.process_cam)#after 20 milli sec, we call this fnct agn nd agn, to make the single frames as streaming a video(converting frames to video) 




if __name__ == "__main__":
    app = App()
    app.start()#calling the start method to display the window
    