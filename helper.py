import copy
#from inspect import stack

def get_keys_from_dict(_list = None, key = 'id', as_string = False):
    result = []
    if(isinstance(_list, list) == False):
        return False
    for elem in _list:
        if(isinstance(elem, dict)):
            if(key not in elem):
                continue
            result.append(elem[key])
    if(len(result) == 0):
        return False

    if(as_string):
        return ",".join(str(v) for v in result)
    else:
        return result

def get_keys_from_db_dataset(dataset = None, key = 'id', as_string = False):
    result = []
    if(dataset == None or isinstance(dataset, list) == False or len(dataset) == 0):
        return result

    for elem in dataset:
        if(isinstance(elem, object)):
            result.append(getattr(elem, str(key)))

    if(len(result) == 0):
        return result

    if(as_string):
        return ",".join(str(v) for v in result)
    else:
        return result

def remove_key(data = None, key = 'id'):
    if(isinstance(data, dict)):
        omitted_data = copy.deepcopy(data)
        del omitted_data[key]
    return omitted_data

def db_summary(affected_rows = (0, 0)):
    if(affected_rows[0] > 0):
        print(f"Inserted {affected_rows[0]} rows")
    if(affected_rows[1] > 0):
        print(f"Updated {affected_rows[1]} rows")