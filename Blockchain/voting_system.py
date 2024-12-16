import hashlib
import datetime
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for handling images

# Blockchain Implementation
class Block:
    def __init__(self, index, voter_id, vote, previous_hash):
        self.index = index  # Block number in the chain
        self.timestamp = datetime.datetime.now()  # Timestamp of block creation
        self.voter_id = voter_id  # Unique ID of the voter
        self.vote = vote  # Vote cast by the voter
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = self.calculate_hash()  # Calculate the hash for this block

    def calculate_hash(self):
        """Calculate the hash of the block."""
        block_data = f"{self.index}{self.timestamp}{self.voter_id}{self.vote}{self.previous_hash}"
        return hashlib.sha256(block_data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Initialize the blockchain with the genesis block

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        return Block(0, "Genesis", "None", "0")

    def get_latest_block(self):
        """Retrieve the latest block in the blockchain."""
        return self.chain[-1]

    def add_block(self, voter_id, vote):
        """Add a new block to the blockchain."""
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), voter_id, vote, latest_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Validate the blockchain's integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            # Check if the hash of the block is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            # Check if the previous hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


# Initialize Blockchain
blockchain = Blockchain()

# Dictionary to store votes temporarily for the session
votes = {}

# Functions to Save and Load Blockchain Data
def save_blockchain_to_file():
    """Save blockchain data to a file."""
    with open("blockchain_data.txt", "w") as file:
        for block in blockchain.chain:
            file.write(f"Index: {block.index}, Voter ID: {block.voter_id}, Vote: {block.vote}, Hash: {block.hash}\n")
    print("Blockchain data has been saved to blockchain_data.txt.")


def load_blockchain_from_file():
    """Load and print blockchain data from a file."""
    try:
        with open("blockchain_data.txt", "r") as file:
            data = file.read()
            print("\nBlockchain Data from File:\n", data)
    except FileNotFoundError:
        print("No blockchain data file found.")

# Functions to handle the voting process
def cast_vote(voter_id, party):
    """Store the vote in the blockchain and the dictionary."""
    # Check if the voter has already voted
    if voter_id in votes:
        messagebox.showerror("Error", "You have already voted!")
        return

    # Store vote in dictionary
    votes[voter_id] = party
    print(f"Temporary Vote Storage: {votes}")

    # Add the vote to the blockchain
    blockchain.add_block(voter_id, party)
    print_blockchain()

    messagebox.showinfo("Success", f"Your vote for {party} has been recorded!")

    # Save blockchain data to file
    save_blockchain_to_file()

def print_blockchain():
    """Print the blockchain data to the console."""
    print("\nBlockchain Data:")
    for block in blockchain.chain:
        print(f"Index: {block.index}, Voter ID: {block.voter_id}, Vote: {block.vote}, Hash: {block.hash}")

# Voting GUI with customtkinter
def voting_interface(voter_id):
    """Create the voting interface."""
    def submit_vote():
        selected_party = party_var.get()
        if selected_party:
            cast_vote(voter_id, selected_party)  # Pass voter_id here
            root.quit()  # Close the voting interface window after submitting the vote
        else:
            messagebox.showerror("Error", "Please select a party to vote!")

    root = ctk.CTk()
    root.title("Voting Interface")
    root.geometry("700x700")
    root.config(bg="#2e3b4e")

    # Heading Label with modern font and styling
    heading = ctk.CTkLabel(root, text="Select a Party to Vote For", font=("Arial", 24, "bold"), text_color="#fff", anchor="center")
    heading.pack(pady=30)

    party_var = ctk.StringVar(value="")

    # Party Options with Images
    parties = ["Party A", "Party B", "Party C", "Party D", "Party E", "Party F"]
    party_images = ["/Users/kushagrakumar/Desktop/Online_Voting_System-main/blockchain/Party a.png", "/Users/kushagrakumar/Desktop/Online_Voting_System-main/blockchain/Party b.png", "/Users/kushagrakumar/Desktop/Online_Voting_System-main/blockchain/Party c.png", "/Users/kushagrakumar/Desktop/Online_Voting_System-main/blockchain/Party d.png", "/Users/kushagrakumar/Desktop/Online_Voting_System-main/blockchain/Party e.png", "/Users/kushagrakumar/Desktop/Online_Voting_System-main/blockchain/Party f.png"]  # Replace these with your actual image path

    # Display each party's image and name as radio buttons
    for i, party in enumerate(parties):
        frame = ctk.CTkFrame(root, fg_color="#f7f7f7", width=500, height=120, corner_radius=10)
        frame.pack(pady=15, padx=40, anchor="center")

        # Load party image
        try:
            img = Image.open(party_images[i])  # Use Pillow to open the image
            img = img.resize((80, 80), Image.ANTIALIAS)  # Resize the image
            img = ImageTk.PhotoImage(img)  # Convert the image to a format compatible with tkinter
            img_label = ctk.CTkLabel(frame, image=img, fg_color="#f0f0f0")
            img_label.image = img  # Keep a reference to the image to prevent it from being garbage collected
            img_label.pack(side="left", padx=20)

        except Exception as e:
            print(f"Error loading image for {party}: {e}")

        # Add RadioButton for each party
        radio_button = ctk.CTkRadioButton(frame, text=party, variable=party_var, value=party, font=("Arial", 14), fg_color="#f0f0f0", text_color="#333")
        radio_button.pack(side="left", padx=20)

    # Submit Button with a nice design
    submit_button = ctk.CTkButton(root, text="Submit Vote", command=submit_vote, font=("Arial", 16, "bold"), fg_color="#4CAF50", text_color="white", hover_color="#45a049", corner_radius=10)
    submit_button.pack(pady=40)

    root.mainloop()

# Voter ID Login GUI
def voter_login():
    """Create the login window to get the voter ID."""
    def login():
        voter_id = voter_id_entry.get()
        if voter_id:
            # Validate the Voter ID (example: check if it's in a list of valid IDs)
            if voter_id == "valid_voter_id":  # You can replace this with actual validation logic
                voting_interface(voter_id)  # Pass the voter ID to the voting interface
                login_window.quit()  # Close the login window after successful login
            else:
                messagebox.showerror("Error", "Invalid Voter ID!")
        else:
            messagebox.showerror("Error", "Please enter a Voter ID.")

    # Create Login Window
    login_window = ctk.CTk()
    login_window.title("Voter Login")
    login_window.geometry("400x300")
    login_window.config(bg="#2e3b4e")

    # Voter ID Label and Entry
    voter_id_label = ctk.CTkLabel(login_window, text="Enter Voter ID", font=("Arial", 16), text_color="#fff")
    voter_id_label.pack(pady=20)

    voter_id_entry = ctk.CTkEntry(login_window, font=("Arial", 14))
    voter_id_entry.pack(pady=10)

    # Login Button
    login_button = ctk.CTkButton(login_window, text="Login", command=login, font=("Arial", 16, "bold"), fg_color="#4CAF50", text_color="white", hover_color="#45a049", corner_radius=10)
    login_button.pack(pady=20)

    login_window.mainloop()

# Main Program (Start the login window)
def main():
    voter_login()

if __name__ == "__main__":
    main()
