#rating_task.py

import os
import random
import numpy as np
from psychopy import visual, event, core
from PIL import Image
from experiment_setup import params
from ui_components import create_text_screen, show_message

def create_custom_slider(win):
    """Create a custom slider with specified properties."""
    slider = visual.Slider(
        win=win,
        ticks=(0, 100),  # Continuous scale from 0 to 100
        labels=["I cannot see the S", "I can clearly see the S"],
        granularity=0,  # Continuous scale
        pos=(0, -0.2),
        size=(0.6, 0.05),
        style=['rating'],
        color='black',
        fillColor='lightgrey',
        borderColor='black',
        labelHeight=0.02,
        labelColor='black',
        markerColor='red',
        lineColor='black'
    )
    # Set the initial marker position to the middle (50)
    slider.markerPos = 50
    return slider

def load_tiff_image(filepath):
    """Load a TIFF image and convert to numpy array"""
    try:
        img = Image.open(filepath)
        return np.array(img)
    except Exception as e:
        print(f"Error loading image {filepath}: {e}")
        return None
    
def load_images_from_classes(base_dir="rating_task_images"):
    """Load classification images from High/Mid/Low imagery participant folders"""
    participant_classes = ['High_imagery', 'Mid_imagery', 'Low_imagery']
    all_image_data = []
    
    for participant_class in participant_classes:
        class_dir = os.path.join(base_dir, participant_class)
        if not os.path.exists(class_dir):
            print(f"Warning: Directory {class_dir} does not exist")
            continue
            
        participant_folders = [f for f in os.listdir(class_dir) if f.startswith('P')]
        
        for participant in participant_folders:
            participant_dir = os.path.join(class_dir, participant)
            
            for session in ['S1', 'S2']:
                session_dir = os.path.join(participant_dir, session)
                if not os.path.exists(session_dir):
                    continue
                    
                for generation in ['G2', 'G6']:
                    gen_dir = os.path.join(session_dir, generation)
                    if not os.path.exists(gen_dir):
                        continue
                        
                    # Look for composite.tiff file
                    image_path = os.path.join(
                        gen_dir, 
                        f"{participant}_{session}_{generation}_composite.tiff"
                    )
                    
                    if os.path.exists(image_path):
                        img = load_tiff_image(image_path)
                        if img is not None:
                            all_image_data.append({
                                'image': img,
                                'metadata': {
                                    'participant_class': participant_class,
                                    'participant_id': participant,
                                    'generation': generation,
                                    'session': session,
                                    'image_path': image_path
                                }
                            })
    
    # Shuffle the images
    random.shuffle(all_image_data)
    
    print(f"Found {len(all_image_data)} images total")
    return all_image_data

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

def run_rating_task(win, exp_handler, debug_mode=False):
    """Run the rating task for classification images"""
    # Show introduction to rating task
    intro_text = """
    Rating Task
    
    In this final part of the experiment, you will be presented with classification images 
    derived from previous participants' responses.
    
    Each image contains the letter 'S', though the visibility may vary considerably.
    
    Your task is to rate the perceptual clarity of the letter 'S' in each image.
    
    Use the slider to indicate your rating from 
    "I cannot see the S" to "I can clearly see the S".
    
    Click the "Submit" button after making your assessment for each image.
    """
    show_message(win, intro_text)
    
    # Load all images
    try:
        image_data = load_images_from_classes()
        if not image_data:
            show_message(win, "No images found for rating task. The experiment will now end.")
            return
    except Exception as e:
        show_message(win, f"Error loading images: {e}\nThe experiment will now end.")
        return
    
    # Create custom rating scale
    rating_scale = create_custom_slider(win)
    
    # Create submit button with adjusted position
    submit_button = visual.Rect(
        win=win,
        width=0.2,
        height=0.08,
        fillColor='green',
        pos=(0, -0.4),
        units='height'
    )
    submit_label = create_text_screen(win, "Submit", pos=(0, -0.4), height=0.04, color='white')
    
    # Create progress text
    progress_text = create_text_screen(win, "", pos=(0, -0.45), height=0.03)
    
    # Process each image
    mouse = event.Mouse(visible=True, win=win)
    total_images = len(image_data)
    
    for i, data_item in enumerate(image_data):
        img_array = data_item['image']
        img_metadata = data_item['metadata']
        
        # Create image stimulus
        img_stim = create_image_from_array(win, img_array)
        img_stim.pos = (0, 0.12)
        img_stim.setSize((0.3, 0.3))
        
        # Reset rating scale for new image
        rating_scale.rating = None
        # Set to middle (50)
        rating_scale.markerPos = 50
        
        # Update progress text
        progress_text.text = f"Image {i+1} of {total_images}"
        
        # Create instruction text
        instruction = create_text_screen(
            win, 
            "Rate how clearly you can spot the 'S' in this image:", 
            pos=(0, 0.4), 
            height=0.05
        )
        
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
                exp_handler.addData('participant_class', img_metadata['participant_class'])
                exp_handler.addData('participant_id', img_metadata['participant_id'])
                exp_handler.addData('generation', img_metadata['generation'])
                exp_handler.addData('image_session', img_metadata['session'])
                exp_handler.addData('image_path', img_metadata['image_path'])
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