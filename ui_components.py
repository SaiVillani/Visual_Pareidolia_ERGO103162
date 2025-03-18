#ui_components.py

from psychopy import visual, event, core
from stimuli import generate_noise_pattern, create_image_from_array, create_training_stimulus, create_training_target_j_stim
import random
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

def show_message(win, message, button_text="Continue", height=0.05):
    """Display a message with a continue button"""
    text_stim = create_text_screen(win, message, pos=(0, 0.1), height=height)
    button = visual.Rect(
        win=win,
        width=0.3,
        height=0.08,
        fillColor='green',
        pos=(0, -0.4),
        units = 'height'
    )
    button_label = create_text_screen(win, button_text, pos=(0, -0.4), height=0.05, color='white')
    
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
    start_y = 0.3  # Position grid below the target
    
    # Position each stimulus
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * x_spacing
            y = start_y - row * y_spacing
            positions.append((x, y))
    
    return positions



def run_introduction(win, training_target_stim):
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
    show_message(win, intro_text)
    
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
    
    # Show training target
    training_target_stim.pos = (0, 0.3)
    training_target_stim.draw()
    
    training_instructions = create_text_screen(win, training_text, pos=(0, -0.1), height=0.04)
    training_instructions.draw()
    
    button = visual.Rect(win=win, width=0.4, height=0.1, fillColor='green', pos=(0, -0.4), units='height')
    button_label = create_text_screen(win, "Begin Training", pos=(0, -0.4), height=0.05, color='white')
    
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

def run_training_trials(win, exp_handler):
    """Run the training trials"""
    from stimuli import create_training_stimulus, create_image_from_array, create_training_target_j
    
    training_target_stim = create_image_from_array(win, create_training_target_j())
    
    for trial_number in range(1, 13):
        # Create stimuli for this trial 
        stimuli = []
        target_index = random.randint(0, 11)
        
        for i in range(12):
            if i == target_index:
                stim_array = create_training_stimulus(True, trial_number)
            else:
                stim_array = generate_noise_pattern()
            
            stim = create_image_from_array(win, stim_array)
            stimuli.append(stim)
        
        # Show target - adjusted position
        target_label = create_text_screen(win, "Target Letter", pos=(0, 0.8), height=0.05)
        target_label.draw()
        
        training_target_stim.pos = (0, 0.65)
        training_target_stim.draw()
        
        # Position stimuli in a grid - using improved grid function
        positions = create_stimuli_grid(stimuli, rows=3, cols=4)
        for i, stim in enumerate(stimuli):
            stim.pos = positions[i]
            stim.setSize((0.14, 0.14))  # Consistent size
            stim.draw()
        
        win.flip()
        
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
    show_message(win, training_complete_text)

def show_break(win):
    """Show break screen between sessions"""
    break_text = """
    Break Time
    
    Well done! You've completed the first session.
    
    Please take a moment to rest your eyes and stretch if needed.
    
    The second session will be identical to the first one. 
    Remember to keep looking for patterns that resemble the letter 'S'.
    """
    show_message(win, break_text)

def show_debrief(win):
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
    show_message(win, debrief_text, "Exit")