import os
import random
import numpy as np
from psychopy import visual, event, core
from PIL import Image
from experiment_setup import params
from debug_utils import debug_element
from ui_components import create_text_screen, show_message

def load_tiff_image(filepath):
    """Load a TIFF image and convert to numpy array"""
    try:
        img = Image.open(filepath)
        return np.array(img)
    except Exception as e:
        print(f"Error loading image {filepath}: {e}")
        return None

def load_composite_images(base_dir="study_data_export_20250225_125147/classification_images"):
    """Load all G6 composite images from previous participants"""
    s1_images = []
    s2_images = []
    image_paths = []  # Store paths to track which image is which
    
    # Find all participant folders
    participant_folders = [f for f in os.listdir(base_dir) if f.startswith('P')]
    
    for participant in participant_folders:
        participant_dir = os.path.join(base_dir, participant)
        
        # Look for S1 G6 composite
        s1_path = os.path.join(participant_dir, "S1", "G6", f"{participant}_S1_G6_composite.tiff")
        if os.path.exists(s1_path):
            img = load_tiff_image(s1_path)
            if img is not None:
                s1_images.append(img)
                image_paths.append({"path": s1_path, "participant": participant, "session": "S1"})
        
        # Look for S2 G6 composite
        s2_path = os.path.join(participant_dir, "S2", "G6", f"{participant}_S2_G6_composite.tiff")
        if os.path.exists(s2_path):
            img = load_tiff_image(s2_path)
            if img is not None:
                s2_images.append(img)
                image_paths.append({"path": s2_path, "participant": participant, "session": "S2"})
    
    print(f"Found {len(s1_images)} S1 images")
    print(f"Found {len(s2_images)} S2 images")
    
    # Combine all images and their metadata
    all_images = s1_images + s2_images
    
    # Create a list of tuples (image, metadata)
    image_data = list(zip(all_images, image_paths))
    
    # Shuffle the images while keeping track of their metadata
    random.shuffle(image_data)
    
    return image_data

def create_image_from_array(win, array):
    """Convert numpy array to PsychoPy stimulus"""
    # Resize for display if needed
    from PIL import Image
    img = Image.fromarray(array)
    img = img.resize((192, 192), Image.NEAREST)
    
    # Convert to numpy array for PsychoPy and normalize to [-1, 1] range
    img_array = np.array(img).astype(float)
    normalized_array = 2 * (img_array / 255.0) - 1
    
    # Create stimulus
    stim = visual.ImageStim(
        win=win,
        image=normalized_array,
        size=(0.3, 0.3),  # Larger size for rating task
        units='height',
        interpolate=False
    )
    
    return stim

def run_rating_task(win, exp_handler):
    """Run the rating task for composite images"""
    # Show introduction to rating task
    intro_text = """
    Rating Task
    
    In this final part of the experiment, you will see composite images 
    created from previous participants' responses.
    
    Your task is to rate how much each image resembles the letter 'S'.
    
    Use the slider to indicate your rating from 
    "Not an S at all" to "Very clearly an S".
    
    Click the "Submit" button when you've made your decision for each image.
    """
    show_message(win, intro_text)
    
    # Load all composite images
    try:
        image_data = load_composite_images()
        if not image_data:
            show_message(win, "No images found for rating task. The experiment will now end.")
            return
    except Exception as e:
        show_message(win, f"Error loading images: {e}\nThe experiment will now end.")
        return
    
    # Create rating scale with adjusted position and size
    rating_scale = visual.Slider(
        win=win,
        ticks=(1, 2, 3, 4, 5, 6, 7),
        labels=["Not an S at all", "", "", "Neutral", "", "", "Very clearly an S"],
        granularity=0.1,
        pos=(0, -0.2),  # Moved up slightly
        size=(0.7, 0.05),  # Slightly smaller width
        style=['rating'],
        color='black',
        fillColor='darkgrey',
        borderColor='white',
        labelHeight=0.04  # Smaller labels
    )
    
    # Create submit button with adjusted position
    submit_button = visual.Rect(
        win=win,
        width=0.2,
        height=0.08,  # Slightly smaller
        fillColor='green',
        pos=(0, -0.4),  # Moved up
        units='height'
    )
    submit_label = create_text_screen(win, "Submit", pos=(0, -0.4), height=0.04, color='white')
    
    # Create progress text with adjusted position
    progress_text = create_text_screen(win, "", pos=(0, -0.55), height=0.03)
    
    # Process each image
    mouse = event.Mouse(visible=True, win=win)
    total_images = len(image_data)
    
    for i, (img_array, img_metadata) in enumerate(image_data):
        # Create image stimulus with adjusted position
        img_stim = create_image_from_array(win, img_array)
        img_stim.pos = (0, 0.25)  # Moved up slightly
        img_stim.setSize((0.25, 0.25))  # Larger for rating task
        
        # Reset rating scale for new image
        rating_scale.rating = None
        rating_scale.markerPos = None
        
        # Update progress text
        progress_text.text = f"Image {i+1} of {total_images}"
        
        # Create instruction text
        instruction = create_text_screen(
            win, 
            "Rate how much this image resembles the letter 'S':", 
            pos=(0, 0.5), 
            height=0.05
        )

        # Debug mode - add after creating UI elements but before the main loop
        if params["debug"]:
            debug_element(win, img_stim, "image_stimulus")
            debug_element(win, instruction, "instruction_text")
            debug_element(win, rating_scale, "rating_scale")
            debug_element(win, submit_button, "submit_button")
            debug_element(win, submit_label, "submit_label")
            debug_element(win, progress_text, "progress_text")
        
        # Wait for rating and submission
        submitted = False
        while not submitted:
            # Draw everything
            instruction.draw()
            img_stim.draw()
            rating_scale.draw()
            submit_button.draw()
            submit_label.draw()
            progress_text.draw()
            win.flip()
            
            # Check for submit button click
            if mouse.isPressedIn(submit_button) and rating_scale.rating is not None:
                # Save data
                exp_handler.addData('task', 'rating')
                exp_handler.addData('image_index', i)
                exp_handler.addData('image_participant', img_metadata['participant'])
                exp_handler.addData('image_session', img_metadata['session'])
                exp_handler.addData('image_path', img_metadata['path'])
                exp_handler.addData('rating', rating_scale.rating)
                exp_handler.nextEntry()
                
                submitted = True
                core.wait(0.2)  # Prevent accidental double-clicks
            
            # Check for escape key
            if event.getKeys(['escape']):
                win.close()
                core.quit()
        
    # Show completion message
    completion_text = """
    Rating Task Complete
    
    Thank you for rating all the images.
    
    You have now completed all parts of the experiment.
    """
    show_message(win, completion_text)