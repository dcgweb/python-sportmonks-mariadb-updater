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

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def db_summary(affected_rows = (0, 0), endpoint = None, tbl = None):
    if(isinstance(affected_rows, bool) == False):
        if(affected_rows[0] > 0 or affected_rows[1] > 0):
            print(f"{endpoint} -> {tbl}:INSERT({affected_rows[0]}) - UPDATE({affected_rows[1]})")