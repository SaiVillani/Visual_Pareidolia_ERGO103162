import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

from stimuli import create_training_stimulus, create_training_stimulus_no_blending

import matplotlib.pyplot as plt

# Visualize all training 'J's from trial 1 to 12
fig, axes = plt.subplots(3, 4, figsize=(12, 9))
for trial in range(1, 13):
    ax = axes[(trial - 1) // 4, (trial - 1) % 4]
    stimulus_with_target = create_training_stimulus(True, trial_number=trial)
    ax.imshow(stimulus_with_target, cmap='gray')
    ax.set_title(f'Trial {trial}')
    ax.axis('off')

plt.tight_layout()
plt.show()


# Visualize all training 'J's from trial 1 to 12 without blending
fig, axes = plt.subplots(3, 4, figsize=(12, 9))
for trial in range(1, 13):
    ax = axes[(trial - 1) // 4, (trial - 1) % 4]
    stimulus_with_target = create_training_stimulus_no_blending(True, trial_number=trial)
    ax.imshow(stimulus_with_target, cmap='gray')
    ax.set_title(f'Trial {trial}')
    ax.axis('off')

plt.tight_layout()
plt.show()
