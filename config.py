import json
class config:
    def __init__(self, conf, filename):
        '''A class for easier work with JSON config files'''
        self.conf = conf
        self.filename = filename

    def get(self, item, value_if_fails = None, index = None):
        '''Returns the value of the item or if it fails, sets it to a select value'''
        try:
            return self.conf[item]
        except:
            if not value_if_fails is None:
                self.set(item, value_if_fails, index, True)
            else:
                return None
    
    def set(self, item, value, index = None, overwrite = False):
        '''Sets an item (or one of its items) in the config to the chosen value'''
        if overwrite:
            self.conf[item] = value
        elif type(self.conf[item]) == list or type(self.conf[item]) == dict:
            self.conf[item][index] = value
        else:
            self.conf[item] = value

    def save(self):
        '''Writes the config to the disk'''
        with open(self.filename, 'w', -1, 'utf-8') as file:
            file.write(json.dumps(self.conf, indent=4, ensure_ascii=False))

    def load(self, filename):
        '''Adds the contents of a file to the config or replaces them'''
        with open(filename, 'r', -1, 'utf-8') as file:
            try:
                data = json.load(file)
            except:
                print("File error: error while decoding config file - it may have been corrupted")
                raise SyntaxError(f"couldn't load file {filename} - something went wrong")
        for i in data.keys():
            self.conf[i] = data[i]

    def reload(self, filename):
        '''Overwrites whatever there is in the config with data in the file'''
        self.conf = {}
        self.load(filename)

def get_file(filename):
    '''Loads a file like a config'''
    with open(filename, 'r+', -1, 'utf-8') as file:
        try:
            return json.load(file)
        except:
            return {}
