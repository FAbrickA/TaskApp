import secrets


def generate_random_token():
    """ Generate crypto strong random token """
    number_of_bytes = 16
    return secrets.token_hex(number_of_bytes)  # length = number_of_bytes * 2
