import os
import numpy as np
import pandas as pd
from PIL import Image
import csv
from datetime import datetime

def setup_participant_folders(participant_id, timestamp=None):
    """Create folder structure for a participant's data"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create main participant directory
    base_dir = os.path.join(os.getcwd(), 'participant_images')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Create participant-specific directory
    participant_dir = os.path.join(base_dir, f'participant_{participant_id}_{timestamp}')
    if not os.path.exists(participant_dir):
        os.makedirs(participant_dir)
    
    # Create format-specific subdirectories
    for format_dir in ['png', 'tiff', 'csv']:
        format_path = os.path.join(participant_dir, format_dir)
        if not os.path.exists(format_path):
            os.makedirs(format_path)
    
    # Create composites directory
    composites_dir = os.path.join(participant_dir, 'composites')
    if not os.path.exists(composites_dir):
        os.makedirs(composites_dir)
    
    return participant_dir

def save_selection_image(array, participant_id, generation, trial, timestamp, participant_dir=None):
    """Save a single selection image in multiple formats"""
    if participant_dir is None:
        participant_dir = os.path.join(os.getcwd(), 'participant_images', f'participant_{participant_id}_{timestamp}')
    
    # Create filename base
    filename_base = f'selection_p{participant_id}_g{generation}_t{trial}'
    
    # Save as PNG
    png_path = os.path.join(participant_dir, 'png', f'{filename_base}.png')
    img = Image.fromarray(array)
    img.save(png_path)
    
    # Save as TIFF
    tiff_path = os.path.join(participant_dir, 'tiff', f'{filename_base}.tiff')
    img.save(tiff_path)
    
    # Save as CSV
    csv_path = os.path.join(participant_dir, 'csv', f'{filename_base}.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in array:
            writer.writerow(row)
    
    return {
        'png': png_path,
        'tiff': tiff_path,
        'csv': csv_path
    }

def create_composite_image(arrays):
    """Create a composite (average) image from multiple arrays"""
    if not arrays:
        return np.zeros((16, 16), dtype=np.uint8)
    
    # Stack arrays and calculate mean
    stacked = np.stack(arrays)
    mean_array = np.mean(stacked, axis=0)
    return mean_array.astype(np.uint8)

def save_composite_image(composite_array, participant_id, generation=None, timestamp=None, participant_dir=None):
    """Save a composite image in multiple formats"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if participant_dir is None:
        participant_dir = os.path.join(os.getcwd(), 'participant_images', f'participant_{participant_id}_{timestamp}')
    
    composites_dir = os.path.join(participant_dir, 'composites')
    
    # Create filename base
    if generation is not None:
        filename_base = f'composite_p{participant_id}_g{generation}'
    else:
        filename_base = f'composite_p{participant_id}_all'
    
    # Save as PNG
    png_path = os.path.join(composites_dir, f'{filename_base}.png')
    img = Image.fromarray(composite_array)
    img.save(png_path)
    
    # Save as TIFF
    tiff_path = os.path.join(composites_dir, f'{filename_base}.tiff')
    img.save(tiff_path)
    
    # Save as CSV
    csv_path = os.path.join(composites_dir, f'{filename_base}.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in composite_array:
            writer.writerow(row)
    
    return {
        'png': png_path,
        'tiff': tiff_path,
        'csv': csv_path
    }