from typing import Union


# FIXME: add uniqueness check for propertiy keys
def valid_properties(properties: Union[dict, None],
                     allow_none: bool = True) -> Union[dict, None]:
    if properties is None:
        if allow_none:
            valid_props = None
        else:
            raise ValueError("pippo")   # TODO: add error message
    elif isinstance(properties, dict):
        valid_props = dict()
        for k, v in properties.items():
            if k[0] == "_":
                k = k[1:]
            valid_props[k] = v
    else:
        raise ValueError("pippo")   # TODO: add error message
    return valid_props
