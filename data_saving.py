import os
import numpy as np
import pandas as pd
from PIL import Image
import csv
from datetime import datetime

class ParticipantDataManager:
    """Class to manage all data saving operations for a participant"""
    
    def __init__(self, participant_id):
        """Initialize the data manager with participant ID and create folder structure"""
        self.participant_id = participant_id
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.participant_dir = self._setup_participant_folders()
        
    def _setup_participant_folders(self):
        """Create folder structure for a participant's data"""
        # Create main participant directory
        base_dir = os.path.join(os.getcwd(), 'participant_images')
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        # Create participant-specific directory
        participant_dir = os.path.join(base_dir, f'participant_{self.participant_id}_{self.timestamp}')
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
            
        # Create stimuli directories
        stimuli_grid_dir = os.path.join(participant_dir, "stimuli_grids")
        if not os.path.exists(stimuli_grid_dir):
            os.makedirs(stimuli_grid_dir)
            
        stimuli_csv_dir = os.path.join(participant_dir, "stimuli_csv")
        if not os.path.exists(stimuli_csv_dir):
            os.makedirs(stimuli_csv_dir)
        
        return participant_dir
    
    def save_selection_image(self, array, generation, trial):
        """Save a single selection image in multiple formats"""
        # Create filename base
        filename_base = f'selection_p{self.participant_id}_g{generation}_t{trial}'
        
        # Save as PNG
        png_path = os.path.join(self.participant_dir, 'png', f'{filename_base}.png')
        img = Image.fromarray(array)
        img.save(png_path)
        
        # Save as TIFF
        tiff_path = os.path.join(self.participant_dir, 'tiff', f'{filename_base}.tiff')
        img.save(tiff_path)
        
        # Save as CSV
        csv_path = os.path.join(self.participant_dir, 'csv', f'{filename_base}.csv')
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in array:
                writer.writerow(row)
        
        return {
            'png': png_path,
            'tiff': tiff_path,
            'csv': csv_path
        }
    
    def create_composite_image(self, arrays):
        """Create a composite (average) image from multiple arrays"""
        if not arrays:
            return np.zeros((16, 16), dtype=np.uint8)
        
        # Stack arrays and calculate mean
        stacked = np.stack(arrays)
        mean_array = np.mean(stacked, axis=0)
        return mean_array.astype(np.uint8)
    
    def save_composite_image(self, composite_array, generation=None):
        """Save a composite image in multiple formats"""
        composites_dir = os.path.join(self.participant_dir, 'composites')
        
        # Create filename base
        if generation is not None:
            filename_base = f'composite_p{self.participant_id}_g{generation}'
        else:
            filename_base = f'composite_p{self.participant_id}_all'
        
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
    
    def save_stimuli_grid(self, win, generation, trial):
        """Save the current window content as an image"""
        # Get the stimuli grid directory
        stimuli_grid_dir = os.path.join(self.participant_dir, "stimuli_grids")
        
        # Create filename with generation and trial info
        filename = f"{self.participant_id}_G{generation}_T{trial}_grid.png"
        filepath = os.path.join(stimuli_grid_dir, filename)
        
        # Capture the window content
        win.getMovieFrame()
        
        # Save the captured frame
        win.saveMovieFrames(filepath)
        
        return filepath
    
    def save_stimuli_as_csv(self, stimuli_arrays, phase, trial):
        """Save all stimuli from a trial as CSV files"""
        # Get the CSV stimuli directory
        csv_dir = os.path.join(self.participant_dir, "stimuli_csv")
        
        # Save each stimulus as a CSV file
        csv_files = []
        for i, stim_array in enumerate(stimuli_arrays):
            filename = f"{self.participant_id}_{phase}_T{trial}_stim{i}.csv"
            filepath = os.path.join(csv_dir, filename)
            
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write the array data
                for row in stim_array:
                    writer.writerow(row)
            
            csv_files.append(filepath)
        
        # Also save a metadata file with information about the trial
        meta_filename = f"{self.participant_id}_{phase}_T{trial}_metadata.csv"
        meta_filepath = os.path.join(csv_dir, meta_filename)
        
        with open(meta_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['participant_id', 'phase', 'trial', 'timestamp', 'num_stimuli'])
            writer.writerow([self.participant_id, phase, trial, self.timestamp, len(stimuli_arrays)])
        
        return csv_files