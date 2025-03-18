#layout_utils.py


def save_layout(elements_dict, filename="layout.json"):
    """Save element positions and sizes to a JSON file"""
    import json
    
    layout = {}
    for name, element in elements_dict.items():
        layout[name] = {
            "pos": element.pos,
            "size": element.size if hasattr(element, 'size') else None
        }
    
    with open(filename, 'w') as f:
        json.dump(layout, f)
    
    print(f"Layout saved to {filename}")

def load_layout(elements_dict, filename="layout.json"):
    """Load element positions and sizes from a JSON file"""
    import json
    import os
    
    if not os.path.exists(filename):
        print(f"Layout file {filename} not found")
        return
    
    with open(filename, 'r') as f:
        layout = json.load(f)
    
    for name, element in elements_dict.items():
        if name in layout:
            element.pos = layout[name]["pos"]
            if hasattr(element, 'size') and layout[name]["size"]:
                element.setSize(layout[name]["size"])
    
    print(f"Layout loaded from {filename}")
