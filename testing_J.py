import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def test_font_sizes(canvas_size=64, font_size_ratios=[0.3, 0.4, 0.5, 0.6]):
    """Test different font sizes for the letter 'J'."""
    fig, axes = plt.subplots(1, len(font_size_ratios), figsize=(15, 5))

    for i, ratio in enumerate(font_size_ratios):
        img = Image.new('L', (canvas_size, canvas_size), color=255)
        draw = ImageDraw.Draw(img)

        try:
            font_size = int(canvas_size * ratio)
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        try:
            draw.text((canvas_size / 2, canvas_size / 2), "J", fill=0, font=font, anchor="mm")
        except TypeError:
            text_width, text_height = font.getsize("J")
            x = canvas_size / 2 - text_width // 2
            y = canvas_size / 2 - text_height // 2
            draw.text((x, y), "J", fill=0, font=font)

        axes[i].imshow(np.array(img), cmap='gray')
        axes[i].set_title(f"Font Ratio: {ratio}")
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

# Test different font sizes
test_font_sizes(canvas_size=16)  # Try with a 32x32 canvas

def analyze_contrast(canvas_size=64, font_size_ratio=0.5):
    """Analyze contrast levels of the letter 'J' against noise."""
    # Generate noise
    noise = np.random.randint(0, 256, (canvas_size, canvas_size), dtype=np.uint8)

    # Create a PIL image from the noise
    img = Image.fromarray(noise)
    draw = ImageDraw.Draw(img)

    try:
        font_size = int(canvas_size * font_size_ratio)
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    try:
        draw.text((canvas_size / 2, canvas_size / 2), "J", fill=0, font=font, anchor="mm")
    except TypeError:
        text_width, text_height = font.getsize("J")
        x = canvas_size / 2 - text_width // 2
        y = canvas_size / 2 - text_height // 2
        draw.text((x, y), "J", fill=0, font=font)

    blended_image = np.array(img)

    # Calculate contrast: difference between 'J' pixels and noise pixels
    j_mask = blended_image < 128  # Assume 'J' pixels are darker
    noise_pixels = blended_image[~j_mask]
    j_pixels = blended_image[j_mask]

    avg_noise = np.mean(noise_pixels)
    avg_j = np.mean(j_pixels)
    contrast = avg_noise - avg_j

    return contrast, blended_image

# Analyze contrast
contrast, contrast_image = analyze_contrast(canvas_size=16)
plt.imshow(contrast_image, cmap='gray')
plt.title(f"Contrast Analysis (Contrast: {contrast:.2f})")
plt.axis('off')
plt.show()

def test_noise_levels(canvas_size=64, noise_intensities=[50, 100, 150]):
    """Test different noise intensities."""
    fig, axes = plt.subplots(1, len(noise_intensities), figsize=(15, 5))

    for i, intensity in enumerate(noise_intensities):
        # Generate noise with specified intensity
        noise = np.random.randint(0, intensity + 1, (canvas_size, canvas_size), dtype=np.uint8)

        # Create a PIL image from the noise
        img = Image.fromarray(noise)
        draw = ImageDraw.Draw(img)

        try:
            font_size = int(canvas_size * 0.5)  # Fixed ratio for testing
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        try:
            draw.text((canvas_size / 2, canvas_size / 2), "J", fill=0, font=font, anchor="mm")
        except TypeError:
            text_width, text_height = font.getsize("J")
            x = canvas_size / 2 - text_width // 2
            y = canvas_size / 2 - text_height // 2
            draw.text((x, y), "J", fill=0, font=font)

        axes[i].imshow(np.array(img), cmap='gray')
        axes[i].set_title(f"Noise Intensity: {intensity}")
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()

# Test different noise levels
test_noise_levels(canvas_size=16)

def create_optimized_training_stimulus(has_target=True, trial_number=1, stim_size=32):
    """Create an optimized training stimulus with clear 'J'."""
    # Generate standard noise pattern with reduced intensity
    max_noise_intensity = max(100 - trial_number * 5, 50)  # Reduce noise over trials
    noise = np.random.randint(0, max_noise_intensity + 1, (stim_size, stim_size), dtype=np.uint8)

    if has_target:
        # Create a PIL image from the noise
        img = Image.fromarray(noise)
        draw = ImageDraw.Draw(img)

        try:
            # Adjust font size based on trial number for better visibility
            base_font_ratio = 0.4 + (trial_number * 0.01)  
            font_size = int(stim_size * base_font_ratio)
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Draw the letter 'J'
        try:
            draw.text((stim_size / 2, stim_size / 2), "J", fill=max(255 - trial_number * 20, 50), 
                      font=font, anchor="mm")
        except TypeError:
            text_width, text_height = font.getsize("J")
            x = stim_size / 2 - text_width // 2
            y = stim_size / 2 - text_height // 2
            draw.text((x, y), "J", fill=max(255 - trial_number * 20, 50), 
                      font=font)

        return np.array(img)

    return noise

# Visualize optimized stimulus across trials
fig, axes = plt.subplots(3, 4, figsize=(12, 9))
for trial in range(1, 13):
    ax = axes[(trial - 1) // 4][(trial - 1) % 4]
    stimulus_with_target = create_optimized_training_stimulus(trial_number=trial)
    ax.imshow(stimulus_with_target, cmap='gray')
    ax.set_title(f"Trial {trial}")
    ax.axis('off')

plt.tight_layout()
plt.show()

