

def extract_title(markdown):
    splitted = markdown.split("\n")
    for line in splitted:
        if line.startswith("# "):
            cleaned = line.lstrip("#").strip()
            return cleaned
    raise Exception("Missing or invalid header")
