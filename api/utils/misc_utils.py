def check_required_fields(json_data, required_fields=None):
    if required_fields is None:
        required_fields = []

    if isinstance(json_data, list):
        for j in json_data:
            for field in required_fields:
                if field not in j:
                    return False

    else:
        for field in required_fields:
            if field not in json_data:
                return False
    return True
