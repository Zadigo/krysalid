def compare_attributes(tag_attrs, attrs):
    """Helper function that determines whether its
    attributes matches searched conditions"""
    if not isinstance(tag_attrs, list):
        raise ValueError()
    
    if not isinstance(attrs, dict):
        raise ValueError()
    
    if not tag_attrs:
        return False
    
    keys = attrs.keys()
    
    tag_keys = map(lambda x: x[0], tag_attrs)
    missing_keys = keys - tag_keys
    
    if missing_keys:
        return False
    
    truth_array = []
    for key in keys:
        # if key in missing_keys:
        #     truth_array.append(False)
        #     continue
        
        value = (key, attrs[key])
        if value in tag_attrs:
            truth_array.append(True)
        else:
            truth_array.append(False)
    return all(truth_array)
