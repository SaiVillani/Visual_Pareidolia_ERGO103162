#main.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Genetic Reverse Correlation Task - Main Runner
"""

from psychopy import core
from experiment_setup import setup_experiment, params
from stimuli import create_target_s, create_training_target_j, create_target_s_stim, create_training_target_j_stim
from ui_components import run_introduction, run_training_trials, show_debrief, show_break
from experiment_logic import run_session

def main():
    """Run the complete experiment"""
    try:
        # Setup experiment
        exp_handler, win, exp_info = setup_experiment()
        
        # Create target images
        target_array, target_display = create_target_s()
        target_stim = create_target_s_stim(win, target_display)
        
        # Run introduction (skip in ideal observer mode)
        if params["mode"] == "manual":
            training_target_stim = create_training_target_j_stim(win)
            run_introduction(win, training_target_stim)
            run_training_trials(win, exp_handler)
        
        # Run main session
        run_session(win, exp_handler, 1, target_stim, target_array)

        # Run rating task
        if params["mode"] == "manual":
            from rating_task import run_rating_task
            run_rating_task(win, exp_handler)
        
        # Show debrief (skip in ideal observer mode)
        if params["mode"] == "manual":
            show_debrief(win)
        
    except Exception as e:
        print(f"Error in experiment: {e}")
    finally:
        # Clean up
        win.close()
        core.quit()


if __name__ == "__main__":
    main()