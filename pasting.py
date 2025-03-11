import os

# In your setup_experiment function
def setup_experiment():
    # ... (rest of the function remains the same)
    
    # Create a directory for stimuli if it doesn't exist
    stimuli_dir = f"{exp_handler.filename}.stimuli"
    if not os.path.exists(stimuli_dir):
        os.makedirs(stimuli_dir)
    
    return exp_handler, win, exp_info
