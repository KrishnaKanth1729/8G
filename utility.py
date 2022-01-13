def reverse_dict(dictionary: dict) -> dict:
    reversed_dict = {}
    for key, value in dictionary.items():
        reversed_dict[value] = key
    return reversed_dict