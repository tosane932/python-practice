def count_elements(data_list):
    """
    Counts the frequency of each element in a list 
    and returns the result as a dictionary.
    """
    count_dict = {}
    for item in data_list:
        if item in count_dict:
            # If the item already exists, increment its value
            count_dict[item] += 1
        else:
            # If the item is new, initialize it with 1
            count_dict[item] = 1
    return count_dict
