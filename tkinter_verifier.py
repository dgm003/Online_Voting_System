from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess

# Initializing CustomTkinter
ctk.set_appearance_mode("dark")  # Different available Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
    
class VotingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Voting App")
        self.geometry("900x600")

        # Gradient Background (Using Canvas for Effect)
        self.gradient_canvas = ctk.CTkCanvas(self, width=900, height=600, bg="#DAB1C5", highlightthickness=0)#pink bg
        self.gradient_canvas.pack(fill="both", expand=True)
        
        # Left Section
        left_frame = ctk.CTkFrame(self, width=600, height=800, corner_radius=32,bg_color="#DAB1C5")
        left_frame.place(x=60, y=90)

        # Title Text
        title_label = ctk.CTkLabel(
            left_frame, 
            text="Welcome Back 👋",
            font=("Arial Rounded MT Bold", 28, "bold"),
            text_color="darkorchid3"
        )
        title_label.pack(pady=20)

        subtitle_label = ctk.CTkLabel(
            left_frame,
            text="Today is a new day. It's your day.\nYou shape it.",
            font=("Helvetica", 18),
            text_color="cornsilk2"
        )
        subtitle_label.pack()

        # Input Fields
        # Identity Proof
        id_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        id_frame.pack(pady=(20, 5), anchor="w")

        id_icon=Image.open("identity_icon.png").resize((40, 40))
        id_img=ImageTk.PhotoImage(id_icon)
        id_label = ctk.CTkLabel(id_frame, image=id_img, text="")
        id_label.image = id_img  # Keep reference
        id_label.pack(side="left", padx=(0, 10))

        self.id_entry = ctk.CTkEntry(id_frame, placeholder_text="Enter Voter ID/Aadhar Number",text_color="lavender",width=300)
        self.id_entry.pack(side="left")

         # Phone Number frame
        phone_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        phone_frame.pack(pady=(20, 5), anchor="w")
        ph_icon = Image.open("phone_icon.png").resize((40, 40))
        ph_img = ImageTk.PhotoImage(ph_icon)
        phone_label = ctk.CTkLabel(phone_frame, image=ph_img, text="")
        phone_label.image = ph_img  # Keep reference
        phone_label.pack(side="left", padx=(0, 10))
       
        self.phone_entry = ctk.CTkEntry(phone_frame, placeholder_text="Enter Your Phone No. starting with +91",text_color="lavender",width=300)
        self.phone_entry.pack(side="left")

        # Submit Button
        submit_button = ctk.CTkButton(left_frame, text="Submit",corner_radius=32,fg_color="#4158D0", hover_color="green4", border_color="purple3", command=self.submit_action)
        submit_button.pack(pady=40)

        # Right Section (Image)
        image = Image.open("vote_image.png")  # Replace with your image path
        image = image.resize((500, 500))
        vote_image = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(self, image=vote_image, text="")
        image_label.image = vote_image  # Keep reference
        image_label.place(x=450, y=50)

        #creating a Folder to save/store the data:
        self.data_folder = "voter_data"
        if not os.path.exists(self.data_folder):  # Check if folder exists
            os.mkdir(self.data_folder)  # Create the folder 

    def submit_action(self):
        #storing the entered details in the folder
        voter_id=self.id_entry.get().strip()
        ph_no=self.phone_entry.get().strip()

        #validating the inputs now:
        if not voter_id or not ph_no:
            messagebox.showerror("Error","Must enter both the fields!")
            return # Stops the further execution when if condition fails(i.e wont go for the else state)

        else:
            messagebox.showinfo("Info stored in database!","Proceed further->😃")
            #now,defining the file_path:
        file_path=os.path.join(self.data_folder,"Voter_details.txt")

        try:
            # Write the details to the file
            with open(file_path, "a") as file:
                file.write(f"Voter ID: {voter_id}, Phone Number: {ph_no}\n")

           
            # Show success message
            messagebox.showinfo("Confirmed!", "Move to Next Page 👉")
            self.id_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')

            subprocess.Popen(["python", "pr2.py",ph_no])  # opening otp verifier file
            self.destroy()  # Close the current window after opening the next one


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        
        
        

# Run the app
if __name__ == "__main__":
    app = VotingApp()
    app.mainloop()
