from customtkinter import *
from twilio.rest import Client
from tkinter import messagebox
from PIL import Image
import random
import sys  # To get command line arguments
import time
import subprocess

# OTP Verifier Class
class OTPVerifier(CTk):
    def __init__(self, phone_number):
        super().__init__()

        self.title("OTP Verification")
        self.geometry("1000x580+200+80")
        self.configure(fg_color="white")
        self.resizable(False, False)

        # Twilio Client Setup
        self.phone_number = phone_number
        self.client = Client("ACef3aa4c166a4733e1ab860d89cb8f949", "f0dad893d6e3cc344f161e844ba70542")
        self.otp = self.generate_OTP()
        self.send_OTP()  # Send OTP when the GUI starts

        # Timer Setup
        self.clockTime = 30

        # Layout
        self.create_layout()

    def create_layout(self):
        # Top Background Image (fluid_1)
        fluid1_img = CTkImage(Image.open("fluid_1.png"), size=(1000, 200))
        self.top_image = CTkLabel(self, image=fluid1_img, text="")
        self.top_image.place(x=0, y=0)

        # Cast Vote Image
        otp4_img = CTkImage(Image.open("otp4.png"), size=(300, 300))
        self.otp4_label = CTkLabel(self, image=otp4_img, text="")
        self.otp4_label.place(x=700, y=200)

        # otp Image
        otp3_img = CTkImage(Image.open("otp3.jpg"), size=(300, 200))
        self.otp3_label = CTkLabel(self, image=otp3_img, text="")
        self.otp3_label.place(x=0, y=200)

        # "Verify OTP" Text
        title_font = CTkFont(family="Times New Roman", size=28, weight="bold")
        self.title_label = CTkLabel(self, text="VERIFY OTP", font=title_font, text_color="red")
        self.title_label.place(x=420, y=200)

        # OTP Entry
        self.otp_entry = CTkEntry(self, placeholder_text="Enter your OTP", width=300, height=40, font=("Calibri", 16))
        self.otp_entry.place(x=350, y=250)

        # Timer Label
        self.timer_label = CTkLabel(self, text="00:30", font=("Calibri", 20), text_color="black")
        self.timer_label.place(x=470, y=300)

        # Submit Button
        self.submit_button = CTkButton(self, text="SUBMIT", width=200, height=40, fg_color="black",
                                       text_color="white", command=self.check_OTP)
        self.submit_button.place(x=400, y=350)

        # Resend OTP Button
        self.resend_button = CTkButton(self, text="RESEND OTP", width=200, height=40, fg_color="black",
                                       text_color="white", command=self.resend_OTP)
        self.resend_button.place(x=400, y=400)

        # Bottom Background Image (fluid_2)
        fluid2_img = CTkImage(Image.open("fluid_2.png"), size=(1000, 130))
        self.bottom_image = CTkLabel(self, image=fluid2_img, text="")
        self.bottom_image.place(x=0, y=450)

        # Start Timer
        self.run_timer()

    def generate_OTP(self):
        """Generate a 4-digit random OTP."""
        return random.randint(1000, 9999)

    def send_OTP(self):
        """Send OTP using Twilio SMS."""
        self.client.messages.create(
            to=self.phone_number,
            from_="+12317742092",
            body=f"Your OTP is: {self.otp}"
        )
        print(f"OTP Sent: {self.otp}")  # Debugging only

    def resend_OTP(self):
        """Generate a new OTP and send it."""
        self.otp = self.generate_OTP()
        self.send_OTP()
        self.clockTime = 30  # Reset timer
        self.run_timer()
        messagebox.showinfo("Resent", "A new OTP has been sent to your phone.")

    def check_OTP(self):
        """Verify the entered OTP."""
        user_input = self.otp_entry.get()
        if user_input == str(self.otp):
            messagebox.showinfo("Success", "OTP Verification Successful!")
            self.otp = None  # Invalidate OTP after use
            subprocess.Popen(["python","voting_system.py"],shell=True)
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

    def run_timer(self):
        """Run the countdown timer."""
        self.update_timer()

    def update_timer(self):
        """Update the timer label each second."""
        if self.clockTime <= 0:
            messagebox.showerror("Timeout", "Your OTP has expired. Please resend OTP.")
            return

        minutes, seconds = divmod(self.clockTime, 60)
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.clockTime -= 1
        self.after(1000, self.update_timer)  # Call this method again after 1 second


if __name__ == "__main__":
    # Check if phone number is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <phone_number>")
        sys.exit(1)

    phone_number = sys.argv[1]
    app = OTPVerifier(phone_number)
    app.mainloop()
