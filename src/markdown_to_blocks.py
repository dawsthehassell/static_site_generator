

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = [block.strip() for block in blocks if block.strip()]
    return cleaned_blocks
