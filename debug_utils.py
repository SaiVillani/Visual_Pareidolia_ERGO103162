#debug_utils.py

"""
How the Debug Mode Works
The debug_element function I provided lets you interactively adjust UI elements using keyboard controls:

Arrow keys: Move the element up/down/left/right

+/- keys: Increase/decrease the element's size

Enter key: Save changes and move to the next element

Escape key: Cancel debugging

When you call debug_element(win, some_element, "element_name"), it will:

Show the element with a red outline

Display its current position and size

Let you adjust it with keyboard controls

Return when you press Enter or Escape

"""
from psychopy import event, visual, core
import numpy as np
import json
import os

def debug_element(win, element, name="element", element_index=0, total_elements=1):
    """Show debug info for an element and allow position/size adjustments with navigation"""
    # Create debug overlay
    outline = visual.Rect(
        win=win,
        width=element.size[0] if hasattr(element, 'size') else 0.2,
        height=element.size[1] if hasattr(element, 'size') else 0.1,
        pos=element.pos,
        lineColor='red',
        fillColor=None,
        units='height'
    )
    
    info_text = visual.TextStim(
        win=win,
        text=f"{name}: pos={element.pos}, size={element.size if hasattr(element, 'size') else 'N/A'}",
        pos=[0, -0.4],
        height=0.03,
        color='black'
    )
    
    help_text = visual.TextStim(
        win=win,
        text="Arrow keys: move | +/- keys: resize | Enter: next | Backspace: previous | S: save | Escape: cancel",
        pos=[0, -0.45],
        height=0.02,
        color='black'
    )
    
    navigation_text = visual.TextStim(
        win=win,
        text=f"Element {element_index+1} of {total_elements}",
        pos=[0, -0.5],
        height=0.02,
        color='black'
    )
    
    # Allow adjustment with arrow keys
    step_size = 0.01
    size_step = 0.01
    
    print(f"Debugging {name}. Use arrow keys to adjust position, +/- to adjust size, Enter to continue, Backspace to go back")
    
    while True:
        # Draw the element and debug info
        if hasattr(element, 'draw'):
            element.draw()
        outline.pos = element.pos
        outline.draw()
        info_text.text = f"{name}: pos=({element.pos[0]:.2f}, {element.pos[1]:.2f})"
        if hasattr(element, 'size'):
            info_text.text += f", size=({element.size[0]:.2f}, {element.size[1]:.2f})"
        info_text.draw()
        help_text.draw()
        navigation_text.draw()
        win.flip()
        
        # Check for key presses
        keys = event.waitKeys()
        
        if 'escape' in keys:
            return "cancel"  # Cancel debugging
        elif 'return' in keys:
            return "next"    # Move to next element
        elif 'backspace' in keys:
            return "previous"  # Go back to previous element
        elif 's' in keys:
            return "save"    # Save and exit
        elif 'up' in keys:
            element.pos = (element.pos[0], element.pos[1] + step_size)
        elif 'down' in keys:
            element.pos = (element.pos[0], element.pos[1] - step_size)
        elif 'left' in keys:
            element.pos = (element.pos[0] - step_size, element.pos[1])
        elif 'right' in keys:
            element.pos = (element.pos[0] + step_step, element.pos[1])
        elif 'equal' in keys or 'plus' in keys:
            if hasattr(element, 'size'):
                element.setSize((element.size[0] + size_step, element.size[1] + size_step))
        elif 'minus' in keys:
            if hasattr(element, 'size'):
                element.setSize((max(0.01, element.size[0] - size_step), 
                                max(0.01, element.size[1] - size_step)))
                
        # Update outline size if element has size
        if hasattr(element, 'size'):
            outline.width = element.size[0]
            outline.height = element.size[1]

def save_layout(elements_dict, filename="layout.json"):
    """Save element positions and sizes to a JSON file"""
    layout = {}
    for name, element in elements_dict.items():
        # Convert positions and sizes to serializable format
        pos = [float(element.pos[0]), float(element.pos[1])] if hasattr(element, 'pos') else None
        size = [float(element.size[0]), float(element.size[1])] if hasattr(element, 'size') else None
        
        layout[name] = {
            "pos": pos,
            "size": size
        }
    
    with open(filename, 'w') as f:
        json.dump(layout, f, indent=2)
    
    print(f"Layout saved to {filename}")

def load_layout(elements_dict, filename="layout.json"):
    """Load element positions and sizes from a JSON file"""
    if not os.path.exists(filename):
        print(f"Layout file {filename} not found")
        return False
    
    try:
        with open(filename, 'r') as f:
            layout = json.load(f)
        
        for name, element in elements_dict.items():
            if name in layout:
                if layout[name]["pos"] and hasattr(element, 'pos'):
                    element.pos = tuple(layout[name]["pos"])
                if layout[name]["size"] and hasattr(element, 'size'):
                    element.setSize(tuple(layout[name]["size"]))
        
        print(f"Layout loaded from {filename}")
        return True
    except Exception as e:
        print(f"Error loading layout: {e}")
        return False

def debug_ui_section(win, elements_dict, section_name):
    """Debug all elements in a section with navigation and save their layout"""
    print(f"Debugging {section_name} UI elements")
    
    # Try to load existing layout first
    layout_file = f"{section_name}_layout.json"
    loaded = load_layout(elements_dict, layout_file)
    
    # Convert dictionary to list for ordered navigation
    element_names = list(elements_dict.keys())
    element_objects = [elements_dict[name] for name in element_names]
    total_elements = len(element_names)
    
    # Start with the first element
    current_index = 0
    
    while 0 <= current_index < total_elements:
        name = element_names[current_index]
        element = element_objects[current_index]
        
        print(f"Debugging {name} ({current_index+1}/{total_elements})...")
        result = debug_element(win, element, name, current_index, total_elements)
        
        if result == "next":
            current_index += 1
        elif result == "previous":
            current_index -= 1
        elif result == "save":
            # Save the layout and exit
            save_layout(elements_dict, layout_file)
            return True
        elif result == "cancel":
            print("Debugging canceled")
            return False
    
    # If we've gone through all elements
    save_layout(elements_dict, layout_file)
    return True