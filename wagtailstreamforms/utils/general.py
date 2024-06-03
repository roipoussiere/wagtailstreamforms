from slugify import slugify



def get_slug_from_string(label) -> str:
    return slugify(label)
