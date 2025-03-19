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
        
        # Check if in debug mode
        debug_mode = params.get("debug", False)
        debug_section = 0
        
        # If in debug mode, ask which section to debug
        if debug_mode:
            from psychopy import event, visual
            from debug_utils import debug_ui_section
            
            debug_text = visual.TextStim(
                win=win,
                text="DEBUG MODE\n\nSelect section to debug:\n\n1 - Introduction\n2 - Training\n3 - Main Task\n4 - Rating Task\n\nPress the corresponding number key",
                pos=(0, 0),
                height=0.05,
                color='black'
            )
            debug_text.draw()
            win.flip()
            
            # Wait for key press
            keys = event.waitKeys(keyList=['1', '2', '3', '4', 'escape'])
            if 'escape' in keys:
                win.close()
                core.quit()
            
            debug_section = int(keys[0])
        
        # Create target images
        target_array, target_display = create_target_s()
        target_stim = create_target_s_stim(win, target_display)
        training_target_stim = create_training_target_j_stim(win)
        
        # Run introduction (skip in ideal observer mode)
        if params["mode"] == "manual" and (not debug_mode or debug_section == 1):
            run_introduction(win, training_target_stim, debug_mode)
            
        # Run training trials
        if params["mode"] == "manual" and (not debug_mode or debug_section == 2):
            run_training_trials(win, exp_handler, debug_mode)
        
        # Run main session
        if not debug_mode or debug_section == 3:
            run_session(win, exp_handler, 1, target_stim, target_array, debug_mode)

        # Run rating task
        if params["mode"] == "manual" and (not debug_mode or debug_section == 4):
            from rating_task import run_rating_task
            run_rating_task(win, exp_handler, debug_mode)
        
        # Show debrief (skip in ideal observer mode)
        if params["mode"] == "manual" and not debug_mode:
            show_debrief(win)
        
    except Exception as e:
        print(f"Error in experiment: {e}")
    finally:
        # Clean up
        win.close()
        core.quit()


if __name__ == "__main__":
    main()