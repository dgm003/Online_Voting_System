🗳️ Secure Online Voting System

A secure, end-to-end encrypted online voting system that leverages Facial Recognition, OTP verification, and Blockchain technology to ensure a transparent, tamper-proof, and user-friendly voting experience.
🚀 Features

✅ Facial Recognition Login
Ensures one-person-one-vote policy using OpenCV-based face recognition for voter identity verification.

✅ 2-Step Verification (OTP via Twilio)
Sends OTP to the voter’s registered phone number using Twilio API, adding an additional layer of security.

✅ Aadhaar/Voter ID Validation
Ensures only verified citizens can proceed to vote.

✅ Blockchain-Powered Vote Ledger
Votes are stored on a local blockchain, ensuring immutability and transparency.

✅ Admin Panel with Face Unlock
Admins can securely view the votes using facial recognition without compromising voter identity.
🧱 Tech Stack
Layer	Technology
GUI	Python + Tkinter
Face Recognition	OpenCV, Haar Cascades
OTP Service	Twilio API
Blockchain	Python (Custom Blockchain)
Frontend (Landing Page)	HTML/CSS
Backend Logic	Python
🛠️ Installation & Setup

    Clone the Repository

git clone https://github.com/your-repo/secure-voting.git
cd secure-voting

Install Required Libraries

pip install opencv-python twilio tkinter

Configure Twilio

    Go to your Twilio Console

    Copy your Account SID and Auth Token

    Paste them into your script:

    self.client = Client("YOUR_SID", "YOUR_AUTH_TOKEN")

Run the Application

    python voter.py

📂 Project Structure

📦 Secure-Voting
├── voter.py                # Main GUI and backend logic
├── blockchain.py           # Simple blockchain implementation
├── face_dataset/           # Stores registered face images
├── trained_model.yml       # Face recognizer model file
├── templates/
│   └── index.html          # Home landing page
├── static/
│   └── style.css           # Styling for the frontend
└── README.md

📸 Screenshots

(You can add screenshots here for Home Page, Face Detection, OTP Input, Voting Page, Blockchain Display, etc.)
🔐 Security Features

    OTP via SMS (Twilio)

    Face recognition login (no password reuse)

    Blockchain-based ledger prevents vote tampering

    Admin authentication also uses facial recognition

📚 Future Enhancements

    Integrate fingerprint authentication

    Add database for persistent user management

    Deploy on a local/hosted server

    Email-based voter confirmation

👨‍💻 Authors

    Dhanush G M – GitHub

    Team Members – Kushagra, Jayanth, Abhijit
