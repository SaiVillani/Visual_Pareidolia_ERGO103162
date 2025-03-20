# reconstruction_utils.py

import os
import json
import numpy as np
from PIL import Image
from psychopy import visual, core, event

def load_experiment_data(participant_id, timestamp=None):
    """Load experiment data for reconstruction"""
    # Find the participant's data directory
    data_dir = os.path.join(os.getcwd(), 'data')
    
    if timestamp:
        # Use specific timestamp
        participant_dir = os.path.join(data_dir, f"participant_{participant_id}_{timestamp}")
    else:
        # Find the most recent directory for this participant
        participant_dirs = [d for d in os.listdir(data_dir) if d.startswith(f"participant_{participant_id}_")]
        if not participant_dirs:
            raise ValueError(f"No data found for participant {participant_id}")
        
        # Sort by timestamp (newest first)
        participant_dirs.sort(reverse=True)
        participant_dir = os.path.join(data_dir, participant_dirs[0])
    
    # Check for stimuli grids directory
    stimuli_grid_dir = os.path.join(participant_dir, "stimuli_grids")
    if not os.path.exists(stimuli_grid_dir):
        raise ValueError(f"No stimuli grids found for participant {participant_id}")
    
    return {
        "participant_dir": participant_dir,
        "stimuli_grid_dir": stimuli_grid_dir
    }

def reconstruct_trial(win, participant_id, generation, trial, timestamp=None):
    """Reconstruct a specific trial from saved data"""
    # Load experiment data
    data = load_experiment_data(participant_id, timestamp)
    
    # Find the grid image for this trial
    grid_pattern = f"{participant_id}_G{generation}_T{trial}_grid.png"
    grid_path = os.path.join(data["stimuli_grid_dir"], grid_pattern)
    
    if not os.path.exists(grid_path):
        print(f"No grid found for Generation {generation}, Trial {trial}")
        return False
    
    # Display the grid
    grid_img = visual.ImageStim(win, image=grid_path, units='norm', size=(2, 2))
    grid_img.draw()
    win.flip()
    
    # Wait for key press to continue
    event.waitKeys()
    return True

def reconstruct_experiment(participant_id, timestamp=None):
    """Reconstruct the entire experiment sequence"""
    # Create a window for reconstruction
    win = visual.Window(
        size=(1024, 768),
        fullscr=False,
        screen=0,
        allowGUI=True,
        allowStencil=False,
        monitor='testMonitor',
        color='white',
        colorSpace='rgb',
        units='height'
    )
    
    try:
        # Load experiment data
        data = load_experiment_data(participant_id, timestamp)
        
        # Get all grid files and sort them
        grid_files = [f for f in os.listdir(data["stimuli_grid_dir"]) if f.endswith("_grid.png")]
        grid_files.sort()
        
        # Display instructions
        instructions = visual.TextStim(
            win=win,
            text="Experiment Reconstruction\n\nPress any key to advance through trials\nESC to exit",
            pos=(0, 0),
            height=0.05,
            color='black'
        )
        instructions.draw()
        win.flip()
        
        # Wait for key press
        if 'escape' in event.waitKeys():
            return
        
        # Display each grid in sequence
        for grid_file in grid_files:
            grid_path = os.path.join(data["stimuli_grid_dir"], grid_file)
            grid_img = visual.ImageStim(win, image=grid_path, units='norm', size=(2, 2))
            
            # Extract generation and trial from filename
            parts = grid_file.split('_')
            gen_info = [p for p in parts if p.startswith('G')][0]
            trial_info = [p for p in parts if p.startswith('T')][0]
            
            # Display info
            info_text = visual.TextStim(
                win=win,
                text=f"Generation: {gen_info[1:]} | Trial: {trial_info[1:]}",
                pos=(0, -0.45),
                height=0.03,
                color='black'
            )
            
            grid_img.draw()
            info_text.draw()
            win.flip()
            
            # Wait for key press
            keys = event.waitKeys()
            if 'escape' in keys:
                break
    
    finally:
        win.close()