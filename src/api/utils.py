def add_index_to_array(arr, key):
    """
    A helper function to take 
    """
    indexed_array = []
    for index, val in enumerate(arr, start = 1):
        indexed_array.append((index, {key: val}))
    
    return indexed_array