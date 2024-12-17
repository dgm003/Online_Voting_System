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

# Function to cast a vote
def cast_vote(voter_id, party):
    """Store the vote in the blockchain and the dictionary."""
    # Check if the voter has already voted
    if voter_id in votes:
        messagebox.showerror("Error", "You have already voted!")
        return

    # Store vote in dictionary
    votes[voter_id] = party

    # Add the vote to the blockchain
    blockchain.add_block(voter_id, party)
    messagebox.showinfo("Success", f"Your vote for {party} has been recorded!")
    print_blockchain()


def print_blockchain():
    """Print the blockchain data to the console."""
    print("\nBlockchain Data:")
    for block in blockchain.chain:
        print(f"Index: {block.index}, Voter ID: {block.voter_id}, Vote: {block.vote}, Hash: {block.hash}")


# GUI Implementation
def create_voting_gui():
    """Create the voting interface using CustomTkinter."""
    def on_vote_click(party):
        voter_id = voter_id_entry.get()
        if not voter_id.strip():
            messagebox.showerror("Error", "Please enter your Voter ID.")
            return
        cast_vote(voter_id, party)
        close_window()

    def close_window():        
        """Close the voting window."""
        root.destroy()

    # Create the main window
    root = ctk.CTk()
    root.title("Online Voting System")
    root.geometry("600x600")

    # Voter ID entry
    voter_id_label = ctk.CTkLabel(root, text="Enter Voter ID:")
    voter_id_label.pack(pady=10)
    voter_id_entry = ctk.CTkEntry(root, width=300)
    voter_id_entry.pack(pady=5)

    # Load party images
    party_images = ["party_a.png", "party_b.png", "party_c.png", "party_d.png", "party_e.png"]
    party_names = ["Party A", "Party B", "Party C", "Party D", "Party E"]

    image_objects = []
    for image_path in party_images:
        img = Image.open(image_path).resize((100, 100))  # Resize for uniformity
        image_objects.append(ImageTk.PhotoImage(img))

    # Create buttons for each party
    for i, party in enumerate(party_names):
        button = ctk.CTkButton(
            root,
            image=image_objects[i],
            text=party,
            compound="top",
            command=lambda p=party: on_vote_click(p)
        )
        button.pack(pady=10)

    root.mainloop()
    root.destroy()


if __name__ == "__main__":
    create_voting_gui()
