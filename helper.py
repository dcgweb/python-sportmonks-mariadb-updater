import constants, datetime, time, random, os, sys, json, string, unicodedata, re
from termcolor import colored

def search_list_of_dicts(_list, search_col, value):
    try:
        for item in _list:
            if(item[search_col] == value):
                return True
    except Exception as e:
        print(colored(e, 'red'))
        return False
    return False


def find_repeated(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(x[i])
    return repeated

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

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

def write_log(log_message):
    import logging
    logging.basicConfig(
        filename="latest.log",
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s"
    )
    logging.debug(log_message)
    if(constants.DEBUG):
        print(colored(log_message, 'red'))