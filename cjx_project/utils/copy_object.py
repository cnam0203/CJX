def copy_object(obj, attributes):
    new_obj = {}

    for attr in attributes:
        new_obj[attr] = obj[attr]

    return new_obj