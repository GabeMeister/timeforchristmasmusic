""" random helpers """

# pylint: disable=C0103,C0111,E1101,W0401,C0301

def get_name_from_url(url):
    name = url.replace('-', ' ').title()
    return name
