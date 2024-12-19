from re import sub

def sanitize_filename(filename):
    return sub(r'[\\/:"*?<>|]', '', filename)
