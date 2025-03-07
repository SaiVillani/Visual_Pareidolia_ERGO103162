#Experiment_setup.py

from psychopy import visual, core, data, event, gui, logging
import os
from datetime import datetime

# Experimental parameters
params = {
    "generations": 12,
    "trials_per_gen": 12,
    "sessions": 1,
    "stim_size": 16,
    "inter_trial_interval": 0.3,
    "mode" : "manual" # "manual" or "ideal_observer"
}

# Constants for filtering
SINGLE_TRIAL_INSTANCE = True
IMPLEMENTATION = 3
THRESHOLD = 30
PRESERVATION_FACTOR = 0.95
NOISE_REDUCTION_FACTOR = 0.1

def setup_experiment():
    """Set up the experiment environment and return handlers"""
    # Create experiment info dialog
    exp_info = {
        'participant': '',
        'session': '001',
        'fullscreen': True
    }
    
    dlg = gui.DlgFromDict(dictionary=exp_info, sortKeys=False, title='Genetic Reverse Correlation Task')
    if not dlg.OK:
        core.quit()  # User pressed cancel
    
    # Create data file name and path
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Create a unique filename for this participant
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_dir}/participant_{exp_info['participant']}_{timestamp}"
    
    # Set up experiment handler to save data
    exp_handler = data.ExperimentHandler(
        name='GeneticReverseCorrelation',
        version='1.0',
        extraInfo=exp_info,
        dataFileName=filename
    )
    
    # Setup the window
    win = visual.Window(
        size=(1000, 800),
        fullscr=exp_info['fullscreen'],
        screen=0,
        allowGUI=False,
        allowStencil=False,
        monitor='testMonitor',
        color='white',
        colorSpace='rgb',
        blendMode='avg',
        useFBO=True
    )
    
    # Set up logging
    logging.console.setLevel(logging.WARNING)
    log_file = logging.LogFile(f"{filename}.log", level=logging.INFO)
    
    return exp_handler, win, exp_info
