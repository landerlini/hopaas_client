from typing import Union


# FIXME: add uniqueness check for property keys
def valid_properties(properties: Union[dict, None],
                     allow_none: bool = True) -> Union[dict, None]:
    if properties is None:
        if allow_none:
            valid_props = None
        else:
            raise ValueError("None value not supported, please pass the "
                             "study properties through a dictionary.")
    elif isinstance(properties, dict):
        valid_props = dict()
        for k, v in properties.items():
            if k[0] == "_":
                k = k[1:]
            valid_props[k] = v
    else:
        raise ValueError("Properties should be passed as dictionary, "
                         f"instead {type(properties)} passed.")
    return valid_props
