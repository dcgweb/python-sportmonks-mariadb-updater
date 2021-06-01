import copy, string, unicodedata, re
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

def clean_string(string, whitelist="-_.() %s%s" % (string.ascii_letters, string.digits), replace='-'):
    # replace spaces
    for r in replace:
        string = string.replace(r,'-')

    # keep only valid ascii chars
    cleaned_string = unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_string = ''.join(c for c in cleaned_string if c in whitelist)
    return cleaned_string[:255]

def media_key(d, key):
    if(key in d):
        try:
            result = d[key][0]['media_url']
        except:
            return '/assets/images/twitter-banner.jpg'
        else:
            return result
    return '/assets/images/twitter-banner.jpg'

def de_emojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def de_url(string):
    return re.sub(r'http\S+', '', string)

def extract_hashtags(s):
    return re.findall(r"#(\w+)", s)
