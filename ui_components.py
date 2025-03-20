#ui_components.py

from psychopy import visual, event, core
from stimuli import generate_noise_pattern, create_image_from_array, create_training_stimulus, create_training_target_j_stim, create_training_target_j
from data_saving import save_stimuli_grid, save_stimuli_as_csv, setup_participant_folders
import random
from datetime import datetime
from experiment_setup import params

def create_text_screen(win, text, pos=(0, 0), height=0.05, color='black'):
    """Create a text stimulus"""
    return visual.TextStim(
        win=win,
        text=text,
        font='Arial',
        pos=pos,
        height=height,
        wrapWidth=1.8,
        color=color,
        colorSpace='rgb',
        opacity=1,
        depth=0.0
    )

def show_message(win, message, button_text="Continue", height=0.05, debug_mode=False):
    """Display a message with a continue button"""
    text_stim = create_text_screen(win, message, pos=(0, 0.1), height=height)
    button = visual.Rect(
        win=win,
        width=0.3,
        height=0.08,
        fillColor='green',
        pos=(0, -0.4),
        units='height'
    )
    button_label = create_text_screen(win, button_text, pos=(0, -0.4), height=0.05, color='white')
    
    # If in debug mode, allow adjusting the UI elements
    if debug_mode:
        from debug_utils import debug_ui_section
        
        # Create a dictionary of all UI elements
        ui_elements = {
            "text_stim": text_stim,
            "button": button,
            "button_label": button_label
        }
        
        # Debug the UI elements
        debug_ui_section(win, ui_elements, "message_screen")
    
    mouse = event.Mouse(visible=True, win=win)
    
    while True:
        text_stim.draw()
        button.draw()
        button_label.draw()
        win.flip()
        
        if mouse.isPressedIn(button):
            core.wait(0.2)  # Prevent accidental double-clicks
            break
        
        if event.getKeys(['escape']):
            win.close()
            core.quit()

def create_stimuli_grid(stimuli, rows=3, cols=4):
    """Create a grid of stimuli and return their positions"""
    positions = []
    
    # Calculate grid dimensions based on window height
    grid_width = 0.8  # 80% of window width
    grid_height = 0.6  # 60% of window height
    
    # Calculate spacing between stimuli
    x_spacing = grid_width / cols
    y_spacing = grid_height / rows
    
    # Calculate starting position (top-left of grid)
    start_x = -grid_width / 2 + x_spacing / 2
    start_y = 0.15  # Position grid below the target
    
    # Position each stimulus
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * x_spacing
            y = start_y - row * y_spacing
            positions.append((x, y))
    
    return positions

def run_introduction(win, training_target_stim, debug_mode=False):
    """Show introduction screens"""
    # Welcome screen
    intro_text = """
    Welcome to the Genetic Reverse Correlation Task
    
    In this experiment, you'll be searching for hidden patterns within visual noise.
    
    On each trial, you'll see a grid of 10 patterns. Your task is to find the pattern 
    that most resembles the target symbol.
    
    First, you'll complete a brief training session to familiarize yourself with the task. 
    Then, you'll proceed to two main sessions with a break in between.
    
    To make your selection, simply click on your chosen pattern with your mouse.
    """
    show_message(win, intro_text, debug_mode=debug_mode)
    
    # Training instructions
    training_text = """
    Training Phase
    
    Let's start with 10 practice trials to help you understand the task.
    
    During training, the patterns will start very clear and become gradually more subtle. 
    This helps you learn what to look for in visual noise.
    




    Important Note: The training patterns are designed to be easier to see than those 
    in the main experiment.
    
    Take your time with each selection - there's no time limit.
    """
    
    # Create UI elements
    training_instructions = create_text_screen(win, training_text, pos=(0, 0.12), height=0.04)
    button = visual.Rect(win=win, width=0.4, height=0.1, fillColor='green', pos=(0, -0.4), units='height')
    button_label = create_text_screen(win, "Begin Training", pos=(0, -0.4), height=0.05, color='white')
    
    # Set target position
    training_target_stim.pos = (0, 0.10)
    
    # If in debug mode, allow adjusting the UI elements
    if debug_mode:
        from debug_utils import debug_ui_section
        
        # Create a dictionary of all UI elements
        ui_elements = {
            "training_instructions": training_instructions,
            "training_target_stim": training_target_stim,
            "button": button,
            "button_label": button_label
        }
        
        # Debug the UI elements
        debug_ui_section(win, ui_elements, "introduction")
    
    # Draw elements
    training_target_stim.draw()
    training_instructions.draw()
    button.draw()
    button_label.draw()
    win.flip()
    
    # Wait for button click
    mouse = event.Mouse(visible=True, win=win)
    while True:
        if mouse.isPressedIn(button):
            core.wait(0.2)
            break
        if event.getKeys(['escape']):
            win.close()
            core.quit()

def run_training_trials(win, exp_handler, debug_mode=False):
    """Run the training trials"""
    
    # Create timestamp for this session if not already created
    if 'timestamp' not in globals():
        global timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Setup participant directory if not already done
    participant_id = exp_handler.extraInfo['participant']
    if 'participant_dir' not in globals():
        global participant_dir
        participant_dir = setup_participant_folders(participant_id, timestamp)

    training_target_stim = create_image_from_array(win, create_training_target_j())

    print("crash after training_target_stim")
    for trial_number in range(1, 13):
        # Create stimuli for this trial 
        stimuli = []
        stimuli_arrays = []
        target_index = random.randint(0, 11)

        for i in range(12):
            if i == target_index:
                stim_array = create_training_stimulus(True, trial_number)
            else:
                stim_array = generate_noise_pattern()
            stimuli_arrays.append(stim_array)
            
            stim = create_image_from_array(win, stim_array)
            stimuli.append(stim)

        csv_filepaths = save_stimuli_as_csv(stimuli_arrays, participant_id, "training", trial_number, timestamp, participant_dir)

        # Create UI elements
        target_label = create_text_screen(win, "Target Letter", pos=(0, 0.8), height=0.05)
        training_target_stim.pos = (0, 0.35)
        
        # Position stimuli in a grid
        positions = create_stimuli_grid(stimuli, rows=3, cols=4)
        for i, stim in enumerate(stimuli):
            stim.pos = positions[i]
            stim.setSize((0.14, 0.14))  # Consistent size
        
        # If in debug mode and this is the first trial, allow adjusting the UI elements
        if debug_mode and trial_number == 1:
            from debug_utils import debug_ui_section
            
            # Create a dictionary of all UI elements
            ui_elements = {
                "target_label": target_label,
                "training_target_stim": training_target_stim
            }
            
            # Add stimuli to the UI elements dictionary
            for i, stim in enumerate(stimuli):
                ui_elements[f"stimulus_{i}"] = stim
            
            # Debug the UI elements
            debug_ui_section(win, ui_elements, "training_trial")
        
        # Draw elements
        #target_label.draw()
        training_target_stim.draw()
        for i, stim in enumerate(stimuli):
            stim.draw()
        win.flip()

        # Save the stimuli grid
        grid_filepath = save_stimuli_grid(win, participant_id, "training", trial_number, timestamp, participant_dir)
        
        # Wait for mouse click on a stimulus
        mouse = event.Mouse(visible=True, win=win)
        clicked = False
        start_time = core.getTime()
        
        # Make sure mouse button is released before starting trial
        while any(mouse.getPressed()):
            core.wait(0.01)
        
        while not clicked:
            # Check for hover and draw stimuli
            mouse_pos = mouse.getPos()
            
            # Redraw everything
            target_label.draw()
            training_target_stim.draw()
            
            for i, stim in enumerate(stimuli):
                # Check if mouse is hovering over stimulus
                if stim.contains(mouse_pos):
                    # Highlight stimulus
                    stim.setSize((0.22, 0.22))  # Make slightly larger when hovered
                else:
                    # Reset to normal size
                    stim.setSize((0.14, 0.14))
                
                # Draw the stimulus
                stim.draw()
            
            win.flip()
            
            # Check for clicks
            if mouse.getPressed()[0]:  # Left mouse button pressed
                for i, stim in enumerate(stimuli):
                    if stim.contains(mouse_pos):
                        selected_id = i
                        is_correct = (selected_id == target_index)
                        reaction_time = core.getTime() - start_time
                        
                        # Save data
                        exp_handler.addData('trial_type', 'training')
                        exp_handler.addData('trial_number', trial_number)
                        exp_handler.addData('target_index', target_index)
                        exp_handler.addData('selected_id', selected_id)
                        exp_handler.addData('correct', is_correct)
                        exp_handler.addData('rt', reaction_time)
                        exp_handler.addData('stimuli_grid', grid_filepath)
                        exp_handler.addData('stimuli_csv', csv_filepaths)
                        exp_handler.nextEntry()
                        
                        clicked = True
                        break
            
            if event.getKeys(['escape']):
                win.close()
                core.quit()
        
        # Wait for mouse button release before continuing to next trial
        core.wait(params['inter_trial_interval'])  # Add a brief pause
        while any(mouse.getPressed()):
            core.wait(0.01)
    
    # Show training completion message
    training_complete_text = """
    Training Complete!
    
    You have completed the training phase.
    
    Now you will begin the main experiment. Your task is to find patterns 
    that resemble the letter 'S'.

    The patterns will be more subtle than in training - this is normal.
    
    If you can't clearly see an 'S', choose the pattern that feels most 'S-like'.
    """
    show_message(win, training_complete_text, debug_mode=debug_mode)

def show_break(win, debug_mode=False):
    """Show break screen between sessions"""
    break_text = """
    Break Time
    
    Well done! You've completed the first session.
    
    Please take a moment to rest your eyes and stretch if needed.
    
    The second session will be identical to the first one. 
    Remember to keep looking for patterns that resemble the letter 'S'.
    """
    show_message(win, break_text, debug_mode=debug_mode)

def show_debrief(win, debug_mode=False):
    """Show the debrief screen"""
    debrief_text = """
    Thank You for Participating!
    
    You have completed the experiment. Your data has been saved.
    
    The aim of this research was to understand the relationship between visual mental 
    imagery and pareidolia. Pareidolia is the tendency to perceive meaningful patterns 
    or images in random or ambiguous stimuli, such as seeing faces in clouds or objects 
    in random shapes.
    
    Your participation will contribute to our understanding of the relationship between 
    pareidolia, visual imagery, and perception. This knowledge is valuable for developing 
    more accurate and objective assessments of visual imagery abilities.
    
    If you have any questions about this study, please contact the researcher.
    
    Thank you again for your participation!
    """
    show_message(win, debrief_text, "Exit", debug_mode=debug_mode)
