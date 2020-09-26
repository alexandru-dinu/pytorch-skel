import json


class Config:
    """
    Fully manages a configuration
    """

    def __init__(self, data: dict = None):
        if data is not None:
            self.__dict__.update(data)

    def __str__(self):
        return json.dumps(self.__get_nested(), indent=4)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.__dict__)

    def __get_nested(self) -> dict:
        out = {}

        for k, v in self.__dict__.items():
            # nested config
            if isinstance(v, Config):
                out[k] = Config.__get_nested(v)

            # non-primitive type
            elif hasattr(v, '__dict__'):
                out[k] = str(v)

            # primitives
            else:
                out[k] = v

        return out

    def is_empty(self):
        return len(self) == 0

    def to_dict(self) -> dict:
        return self.__get_nested()

    def to_file(self, fname) -> None:
        with open(fname, 'wt') as fp:
            fp.write(str(self))
