#genetic_algorithm.py

from tkinter import Image
import numpy as np
import random

def crossbreed(parent1, parent2, stim_size=16):
    """Crossbreed two parent images to create a child"""
    child = np.zeros((stim_size, stim_size), dtype=np.uint8)
    
    # Uniform crossover with normalization
    for i in range(stim_size):
        for j in range(stim_size):
            # Choose from either parent with 50% probability
            if random.random() < 0.5:
                gray_value = parent1[i, j]
            else:
                gray_value = parent2[i, j]
            
            # Mutation (1% chance)
            if random.random() < 0.01:
                gray_value = random.randint(0, 255)
            
            child[i, j] = gray_value
    
    return child

def generate_offspring(parents, stim_size=16):
    """Generate offspring from parents"""
    if len(parents) < 2:
        raise ValueError('Insufficient parents for breeding')
    
    child_array = []
    
    # Create all possible parent combinations
    for i in range(len(parents)):
        for j in range(len(parents)):
            child_array.append(crossbreed(parents[i], parents[j], stim_size))
    
    # Shuffle all children
    random.shuffle(child_array)
    
    # Split into batches of 12 stimuli each
    batches = []
    for i in range(0, len(child_array), 12):
        batch = child_array[i:i+12]
        # Ensure each batch has exactly 12 stimuli
        if len(batch) == 12:
            batches.append(batch)
    
    return batches

def filter_selection(selected_data, non_selected_data_list, threshold=30, 
                    preservation_factor=0.95, noise_reduction_factor=0.1):
    """Filter the selected image using implementation three"""
    # Calculate average of non-selected images
    avg_non_selected = np.zeros_like(selected_data, dtype=float)
    for non_selected in non_selected_data_list:
        avg_non_selected += non_selected
    avg_non_selected /= len(non_selected_data_list)
    
    # Apply filtering algorithm (implementation three)
    filtered_data = np.zeros_like(selected_data, dtype=np.uint8)
    
    for i in range(selected_data.shape[0]):
        for j in range(selected_data.shape[1]):
            selected_value = selected_data[i, j]
            avg_value = avg_non_selected[i, j]
            difference = selected_value - avg_value
            
            if abs(difference) > threshold:
                # For significant differences (potential signal features)
                new_value = round(selected_value * preservation_factor)
            else:
                # For smaller differences (likely noise)
                new_value = round(selected_value - (noise_reduction_factor * difference))
            
            # Ensure values stay within valid range [0,255]
            filtered_data[i, j] = max(0, min(255, new_value))
    
    return filtered_data

def calculate_similarity(image_array, target_array):
    """Calculate similarity between an image and the target (lower is more similar)"""
    # Resize target if needed to match image dimensions
    if image_array.shape != target_array.shape:
        img = Image.fromarray(target_array)
        img = img.resize((image_array.shape[1], image_array.shape[0]), Image.NEAREST)
        target_array = np.array(img)
    
    # Calculate mean squared error
    diff = image_array.astype(float) - target_array.astype(float)
    return np.sum(diff * diff)

def ideal_observer_select(stimuli_arrays, target_array):
    """Simulate an ideal observer by selecting the stimulus most similar to target"""
    similarities = []
    
    # Resize target if needed to match stimuli dimensions
    if stimuli_arrays[0].shape != target_array.shape:
        from PIL import Image
        img = Image.fromarray(target_array)
        img = img.resize((stimuli_arrays[0].shape[1], stimuli_arrays[0].shape[0]), Image.NEAREST)
        target_array = np.array(img)
    
    for stim_array in stimuli_arrays:
        # Calculate mean squared error
        diff = stim_array.astype(float) - target_array.astype(float)
        similarity = np.sum(diff * diff)
        similarities.append(similarity)
    
    # Return index of most similar stimulus (lowest difference)
    return np.argmin(similarities)