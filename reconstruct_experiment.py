# reconstruct_experiment.py

from psychopy import core
from reconstruction_utils import reconstruct_experiment

def main():
    """Run the experiment reconstruction"""
    # Get participant ID from user
    import tkinter as tk
    from tkinter import simpledialog
    
    root = tk.Tk()
    root.withdraw()
    
    participant_id = simpledialog.askstring("Input", "Enter participant ID:")
    if not participant_id:
        core.quit()
    
    # Run reconstruction
    reconstruct_experiment(participant_id)

if __name__ == "__main__":
    main()