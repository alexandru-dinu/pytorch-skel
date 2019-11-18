import json


class Config:
    """
    Fully manages a configuration 
    """
    
    def __init__(self, data=None):
        if isinstance(data, str):
            self.from_json(data)
        if isinstance(data, dict):
            self.from_dict(data)
    
    def __str__(self):
        return '\n'.join(self.__get_sorted())
    
    def __repr__(self):
        return str(self)
    
    def __get_sorted(self):
        return [f'{k:>16}: {v}' for k, v in sorted(self.__dict__.items())]
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__)
    
    def to_file(self, fname) -> None:
        with open(fname, 'wt') as fp:
            for line in self.__get_sorted():
                fp.write(f'{line}\n')
    
    def from_dict(self, d, clear=True):
        if clear:
            self.__dict__ = {}
            
        for k, v in d.items():
            self.__dict__[k] = v
    
    def from_json(self, json_file, clear=True):
        self.from_dict(json.loads(json_file), clear)