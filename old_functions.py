def create_stimuli_grid(stimuli, rows=3, cols=4):
    """Create a grid of stimuli and return their positions"""
    positions = []
    stim_width = 0.12  # Adjust as needed
    stim_height = 0.12
    
    # Increase spacing between stimuli
    spacing_factor = 1.8  # More space between stimuli
    
    # Calculate grid dimensions
    grid_width = cols * stim_width * spacing_factor
    grid_height = rows * stim_height * spacing_factor
    
    # Calculate starting position (top-left of grid)
    start_x = -grid_width / 2 + stim_width / 2
    start_y = 0.1 #grid_height / 2 - stim_height / 2
    
    # Position each stimulus
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * stim_width * spacing_factor
            y = start_y - row * stim_height * spacing_factor
            positions.append((x, y))
    
    return positions


###------------------------###
def run_training_trials(win, exp_handler):
    """Run the training trials"""
    from stimuli import create_training_stimulus, create_image_from_array, create_training_target_j
    
    training_target_stim = create_image_from_array(win, create_training_target_j())
    
    for trial_number in range(1, 13):  # Changed to 12 trials
        # Create stimuli for this trial
        stimuli = []
        target_index = random.randint(0, 11)  # Changed to 0-11 range
        
        for i in range(12):  # Changed to 12 stimuli
            if i == target_index:
                stim_array = create_training_stimulus(True, trial_number)
            else:
                stim_array = generate_noise_pattern()
            
            stim = create_image_from_array(win, stim_array)
            stimuli.append(stim)
        
        # Show target
        target_label = create_text_screen(win, "Target Letter", pos=(0, 0.7), height=0.05)
        target_label.draw()
        
        training_target_stim.pos = (0, 0.55)
        training_target_stim.draw()
        
        # Position stimuli in a grid
        positions = create_stimuli_grid(stimuli, rows=3, cols=4)  # Changed to 3×4 grid
        for i, stim in enumerate(stimuli):
            stim.pos = positions[i]
            stim.draw()
        
        win.flip()
###------------------------###

def create_image_from_array(win, array):
    """Convert numpy array to PsychoPy stimulus with pixelated rendering"""
    # Convert to PIL Image
    img = Image.fromarray(array)
    img = img.resize((192, 192), Image.NEAREST)  # Resize with nearest neighbor for pixelated look
    
    # Convert to numpy array for PsychoPy and normalize to [-1, 1] range
    img_array = np.array(img).astype(float)
    normalized_array = 2 * (img_array / 255.0) - 1
    
    # Create stimulus with fixed size in height units to prevent stretching
    stim = visual.ImageStim(
        win=win,
        image=normalized_array,
        size=(0.2, 0.2),  # Fixed size relative to window height
        units='height',   # Use height units to maintain aspect ratio
        interpolate=False # Disable interpolation for pixelated look
    )
    
    return stim

###------------------------###

# Create rating scale
    rating_scale = visual.Slider(
        win=win,
        ticks=(1, 2, 3, 4, 5, 6, 7),
        labels=["Not an S at all", "", "", "Neutral", "", "", "Very clearly an S"],
        granularity=0.1,
        pos=(0, -0.3),
        size=(0.8, 0.05),
        style=['rating'],
        color='black',
        fillColor='darkgrey',
        borderColor='white',
        labelHeight=0.05
    )
    
    # Create submit button
    submit_button = visual.Rect(
        win=win,
        width=0.2,
        height=0.1,
        fillColor='green',
        pos=(0, -0.5),
        units='height'
    )
    submit_label = create_text_screen(win, "Submit", pos=(0, -0.5), height=0.05, color='white')
    
    # Create progress text
    progress_text = create_text_screen(win, "", pos=(0, -0.6), height=0.04)

###------------------------###

for i, (img_array, img_metadata) in enumerate(image_data):
        # Create image stimulus
        img_stim = create_image_from_array(win, img_array)
        img_stim.pos = (0, 0.2)

###------------------------###

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

###------------------------###

