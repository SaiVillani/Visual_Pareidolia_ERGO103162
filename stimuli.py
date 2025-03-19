#stimuli.py


import numpy as np
from PIL import Image, ImageDraw, ImageFont
from psychopy import visual

def generate_noise_pattern(stim_size=16):
    """Generate a random noise pattern"""
    noise = np.random.randint(0, 256, (stim_size, stim_size), dtype=np.uint8)
    return noise

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
        size=(0.14, 0.14),  # Reduced size to prevent clipping
        units='height',   # Use height units to maintain aspect ratio
        interpolate=False # Disable interpolation for pixelated look
    )
    
    return stim



def create_target_s():
    # Create a canvas
    img = Image.new('L', (32, 32), color=255)
    draw = ImageDraw.Draw(img)
    
    # Draw the letter 'S'
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw text centered
    try:
        draw.text((16, 16), "S", fill=0, font=font, anchor="mm")
    except TypeError:
        text_width, text_height = font.getsize("S")
        draw.text((16 - text_width//2, 16 - text_height//2), "S", fill=0, font=font)
    
    # Convert to numpy array and flip vertically to correct orientation
    target_array = np.array(img)
    target_array = np.flipud(target_array)  # Flip vertically
    
    # Create larger display version (also flipped)
    display_img = Image.new('L', (96, 96), color=255)
    display_draw = ImageDraw.Draw(display_img)
    
    try:
        display_font = ImageFont.truetype("arial.ttf", 72)
    except IOError:
        display_font = ImageFont.load_default()
    
    try:
        display_draw.text((48, 48), "S", fill=0, font=display_font, anchor="mm")
    except TypeError:
        text_width, text_height = display_font.getsize("S")
        display_draw.text((48 - text_width//2, 48 - text_height//2), "S", fill=0, font=display_font)
    
    display_array = np.array(display_img)
    display_array = np.flipud(display_array)  # Flip vertically
    
    return target_array, display_array

def create_target_s_stim(win, target_display):
    """Create PsychoPy stimulus from target image"""
    return create_image_from_array(win, target_display)

def create_training_target_j():
    """Create the training target 'J' image"""
    img = Image.new('L', (64, 64), color=255)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the letter 'J' (compatible with older PIL versions)
    try:
        draw.text((32, 32), "J", fill=0, font=font, anchor="mm")
    except TypeError:
        text_width, text_height = font.getsize("J")
        draw.text((32 - text_width//2, 32 - text_height//2), "J", fill=0, font=font)
    
    # Flip vertically to correct orientation
    return np.flipud(np.array(img))


def create_training_target_j_stim(win):
    """Create PsychoPy stimulus from training target image"""
    return create_image_from_array(win, create_training_target_j())

from scipy import ndimage

def create_training_stimulus(has_target, trial_number, stim_size=16):
    """Create a training stimulus using pixel-wise subtraction for visibility control."""
    # Generate standard noise pattern
    noise = generate_noise_pattern(stim_size)

    if has_target:
        # Create the 'J' canvas as a binary mask
        img = Image.new('L', (stim_size, stim_size), color=255)
        draw = ImageDraw.Draw(img)

        
        font_size = int(stim_size * 1)  # Font size ratio fixed at 0.8
        font = ImageFont.truetype(r"C:/Windows/Fonts/ARIALN.TTF", font_size)

        # Draw the letter 'J' centered in the canvas
        try:
            draw.text((stim_size / 2, stim_size / 2), "J", fill=0, font=font, anchor="mm")
        except TypeError:
            text_width, text_height = font.getsize("J")
            x = stim_size / 2 - text_width // 2
            y = stim_size / 2 - text_height // 2
            draw.text((x, y), "J", fill=0, font=font)

        # Convert the image to a numpy array (binary mask where 'J' pixels are <255)
        j_canvas = np.array(img) < 255

        # Calculate visibility scaling factor for this trial
        max_visibility = 1.0  # Maximum visibility (darkest J)
        min_visibility = 0.65  # Minimum visibility (faintest J)
        visibility = max(min_visibility, max_visibility - (trial_number - 1) * ((max_visibility - min_visibility) / 11))

        # Perform pixel-wise operation: noise + scaled 'J'
        stimulus = noise.copy()
        stimulus[j_canvas] = np.clip(noise[j_canvas] * (1 - visibility), 0, 255)

        return stimulus

    return noise