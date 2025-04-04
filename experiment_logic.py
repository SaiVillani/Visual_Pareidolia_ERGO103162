#experiment_logic.py

from psychopy import event, core
from stimuli import generate_noise_pattern, create_image_from_array
from genetic_algorithm import filter_selection, generate_offspring, ideal_observer_select
from ui_components import create_text_screen, create_stimuli_grid, show_message
from data_saving import ParticipantDataManager
from experiment_setup import params
import numpy as np

# Global variables for tracking experiment state
current_session = 1
current_generation = 0
current_parents = []
next_generation_parents = []
current_batches = None
current_batch_index = 0

#data saving bits
participant_selections = {}  # Dictionary to store all selections by generation
participant_dir = None
timestamp = None

def run_trial(win, exp_handler, generation, trial, target_stim, target_array=None, debug_mode=False, data_manager=None):
    """Run a single trial of the main experiment"""
    global current_batch_index, next_generation_parents, participant_selections
    
    # Get stimuli for this trial
    if generation == 0:
        # First generation: random noise patterns
        stimuli_arrays = [generate_noise_pattern() for _ in range(12)]
    else:
        # Later generations: use offspring from previous generation
        stimuli_arrays = current_batches[current_batch_index]
        current_batch_index += 1

    # Create PsychoPy stimuli from arrays
    stim_objects = [create_image_from_array(win, array) for array in stimuli_arrays]
    
    # Show target
    target_label = create_text_screen(win, "Target Letter", pos=(0, 0.7), height=0.05)

    # If in debug mode, allow adjusting the UI elements
    if debug_mode:
        from debug_utils import debug_ui_section
        
        # Create a dictionary of all UI elements
        ui_elements = {
            "target_label": target_label,
            "target_stim": target_stim
        }
        
        # Add stimuli to the UI elements dictionary
        for i, stim in enumerate(stim_objects):
            ui_elements[f"stimulus_{i}"] = stim
        
        # Debug the UI elements
        debug_ui_section(win, ui_elements, "main_task")
    
    # If in ideal observer mode, select the most similar stimulus automatically
    if params["mode"] == "ideal_observer":
        if target_array is None:
            raise ValueError("Target array must be provided for ideal observer mode")
            
        # Show target
        target_label = create_text_screen(win, "Target Letter (Ideal Observer Mode)", pos=(0, 0.8), height=0.05)

        target_stim.pos = (0, 0.35)
        target_stim.draw()
        
        # Position stimuli in a grid
        positions = create_stimuli_grid(stim_objects)
        for i, stim in enumerate(stim_objects):
            stim.pos = positions[i]
            stim.draw()
        
        win.flip()

        # Save the stimuli grid
        participant_id = exp_handler.extraInfo['participant']
        grid_filepath = data_manager.save_stimuli_grid(win, generation, trial)
        csv_filepaths = data_manager.save_stimuli_as_csv(stimuli_arrays, f"G{generation}", trial)

        # Simulate thinking time
        core.wait(0.2)
        
        # Select stimulus using ideal observer
        selected_id = ideal_observer_select(stimuli_arrays, target_array)
        selected_array = stimuli_arrays[selected_id]
        
        # Highlight selected stimulus
        stim_objects[selected_id].setSize((0.22, 0.22))  # Make selected stimulus larger
        
        # Redraw everything with selected stimulus highlighted
        target_label.draw()
        target_stim.draw()
        for i, stim in enumerate(stim_objects):
            stim.draw()
        
        win.flip()
        core.wait(0.2)  # Show selection briefly
        
        # Get non-selected arrays for filtering
        non_selected_arrays = [stimuli_arrays[j] for j in range(12) if j != selected_id]
        
        # Apply filtering to selected image
        filtered_array = filter_selection(selected_array, non_selected_arrays)

        # Save the selection image
        data_manager.save_selection_image(selected_array, generation, trial)

        # Track the selection for composites
        participant_selections[generation].append(selected_array)
        
        # Add to parents for next generation
        if not next_generation_parents:
            next_generation_parents = []
        
        if filtered_array is not None:
            next_generation_parents.append(filtered_array)
        
        # Save data
        exp_handler.addData('session', 1)
        exp_handler.addData('generation', generation)
        exp_handler.addData('trial', trial)
        exp_handler.addData('selected_id', selected_id)
        exp_handler.addData('rt', 0.2)  # Simulated reaction time
        exp_handler.addData('mode', 'ideal_observer')
        exp_handler.addData('stimuli_grid', grid_filepath)
        exp_handler.addData('stimuli_csv', csv_filepaths)
        exp_handler.nextEntry()
        
        # Wait between trials
        core.wait(params["inter_trial_interval"])
        return

    # Manual mode - rest of the function as before
    
    target_stim.pos = (0, 0.35)
    target_stim.draw()
    
    # Position stimuli in a grid
    positions = create_stimuli_grid(stim_objects)
    for i, stim in enumerate(stim_objects):
        stim.pos = positions[i]
        stim.draw()
    
    win.flip()

    # Save the stimuli grid
    participant_id = exp_handler.extraInfo['participant']
    grid_filepath = data_manager.save_stimuli_grid(win, generation, trial)
    csv_filepaths = data_manager.save_stimuli_as_csv(stimuli_arrays, f"G{generation}", trial)

    # Wait for mouse click on a stimulus
    mouse = event.Mouse(visible=True, win=win)
    clicked = False
    start_time = core.getTime()

    # Make sure mouse button is released before starting trial
    while any(mouse.getPressed()):
        core.wait(0.01)
    
    while not clicked:
        # Redraw everything on each frame
        target_label.draw()
        target_stim.draw()
        
        # Check for hover and draw stimuli
        mouse_pos = mouse.getPos()
        for i, stim in enumerate(stim_objects):
            # Store original size for reference
            if not hasattr(stim, 'original_size'):
                stim.original_size = stim.size
    
            # Check if mouse is hovering over stimulus with improved hit detection
            stim_pos = stim.pos
            stim_size = stim.size[0]  # Assuming square stimuli
    
            # Calculate distance from mouse to stimulus center
            distance = np.sqrt((mouse_pos[0] - stim_pos[0])**2 + (mouse_pos[1] - stim_pos[1])**2)
    
            # If mouse is within the stimulus boundary
            if distance < stim_size/2:
                # Highlight stimulus
                stim.setSize((stim.original_size[0] * 1.1, stim.original_size[1] * 1.1))
            else:
                # Reset to normal size
                stim.setSize(stim.original_size)
    
            # Draw the stimulus
            stim.draw()

        win.flip()
        
        # Check for clicks
        if mouse.getPressed()[0]:  # Left mouse button pressed
            for i, stim in enumerate(stim_objects):
                if stim.contains(mouse_pos):
                    selected_id = i
                    selected_array = stimuli_arrays[i]
                    reaction_time = core.getTime() - start_time
                    
                    # Get non-selected arrays for filtering
                    non_selected_arrays = [stimuli_arrays[j] for j in range(12) if j != i]
                    
                    # Apply filtering to selected image
                    filtered_array = filter_selection(selected_array, non_selected_arrays)

                    #save the selection image
                    data_manager.save_selection_image(selected_array, generation, trial)

                    #track the selection for composites
                    participant_selections[generation].append(selected_array)
                    
                    # Add to parents for next generation
                    if not next_generation_parents:
                        next_generation_parents = []
                    
                    if filtered_array is not None:
                        next_generation_parents.append(filtered_array)
                    
                    # Save data
                    exp_handler.addData('session', 1)
                    exp_handler.addData('generation', generation)
                    exp_handler.addData('trial', trial)
                    exp_handler.addData('selected_id', selected_id)
                    exp_handler.addData('rt', reaction_time)
                    exp_handler.addData('stimuli_grid', grid_filepath)
                    exp_handler.nextEntry()
                    
                    clicked = True
                    break
            
        if event.getKeys(['escape']):
            win.close()
            core.quit()

    # Wait for mouse button release before continuing to next trial
    core.wait(params['inter_trial_interval'])
    while any(mouse.getPressed()):
        core.wait(0.01)


def run_session(win, exp_handler, session_num, target_stim, target_array=None, debug_mode=False):
    """Run a complete session of the experiment"""
    global current_session, current_generation, current_parents
    global next_generation_parents, current_batches, current_batch_index
    global participant_selections
    
    # Initialize session variables
    current_session = session_num
    current_parents = []
    next_generation_parents = []
    current_batches = None
    current_batch_index = 0
    
    # Initialize participant selections tracking
    participant_selections = {gen: [] for gen in range(12)}
    
    # Create data manager for this participant
    participant_id = exp_handler.extraInfo['participant']
    data_manager = ParticipantDataManager(participant_id)
    
    # Show session start message
    if params["mode"] == "manual":
        session_text = f"""
        Starting Session {session_num}
        
        You will now complete a series of trials.
        
        In each trial, you will see 12 different patterns.
        Select the pattern that best matches your target.
        """
        show_message(win, session_text)
    
    # Run all generations for this session
    for gen in range(params['generations']):
        current_generation = gen
        
        # If not first generation, prepare offspring
        if gen > 0:
            # Use parents from previous generation
            current_parents = next_generation_parents
            next_generation_parents = []
            
            # Generate offspring
            current_batches = generate_offspring(current_parents)
            current_batch_index = 0
            
            # Create and save composite for the previous generation
            if participant_selections[gen-1]:
                composite = data_manager.create_composite_image(participant_selections[gen-1])
                data_manager.save_composite_image(composite, gen-1)
        
        # Run all trials for this generation
        for trial in range(12):  # 12 trials per generation
            run_trial(win, exp_handler, gen, trial, target_stim, target_array, debug_mode, data_manager)
    
    # Create and save composite for the last generation
    if participant_selections[11]:
        composite = data_manager.create_composite_image(participant_selections[11])
        data_manager.save_composite_image(composite, 11)
    
    # Create and save mega-composite of all selections
    all_selections = []
    for gen in range(12):
        all_selections.extend(participant_selections[gen])
    
    if all_selections:
        mega_composite = data_manager.create_composite_image(all_selections)
        data_manager.save_composite_image(mega_composite)

