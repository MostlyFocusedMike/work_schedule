import json
from collections import OrderedDict

def read_list(file):
    '''
    Reads file and stores it as a list.
    If the file is empty, it returns an empty list
    '''
    try:
        with open(file) as f_obj:
            contents = json.load(f_obj)
    except FileNotFoundError:
        contents = []
    return contents 

def read_ordered_dict(file):
    '''
    Reads file and stores it as a list.
    If the file is empty, it returns an empty list
    '''
    try:
        with open(file) as f_obj:
            contents = json.load(f_obj)
    except FileNotFoundError:
        contents = OrderedDict()
    return contents 

def read_dict(file):
    '''
    Reads file and stores it as a list.
    If the file is empty, it returns an empty list
    '''
    try:
        with open(file) as f_obj:
            contents = json.load(f_obj)
    except FileNotFoundError:
        contents = {}
    return contents 

    
def read_data(file):
    '''
    Reads file and stores it as a list.
    If the file is empty, it returns an empty list
    '''
    try:
        with open(file) as f_obj:
            contents = json.load(f_obj)
    except FileNotFoundError:
        contents = None
    return contents    
       
def write_data(data, file):
    '''write data to a file'''
    with open(file, 'w') as f_obj:
        json.dump(data, f_obj)
