import pandas as pd

# Getting Started
#1 Load the data to a single DataFrame
def load_file(input_file): # signature (2: we rename the string for use within the function)
    # the function internally doesn't care what the variable is called outside of itself
    # it uses an internal name
    # this internal name refers to a single object - string, dict, integer, etc
    # so you can't use config['input'] here
    # so we can call it 'input_file' or anything else
    try:
        df = pd.read_excel(input_file) # (3: now the function doesn't know what config is)
        # so again, we use the name input_file
    except KeyError as e:
        e.add_note(f'Your config does not have an "input" entry.')
        raise e
    return df # (4: if we just use return, we leave the function without returning a value)
    # returning nothing is the default
    # if we want to return something, we have to tell python