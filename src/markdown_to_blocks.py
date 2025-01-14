

def markdown_to_blocks(markdown):
    print("Raw input:", repr(markdown))
    blocks = markdown.split("\n\n")
    print("After split:", blocks)
    cleaned_blocks = [block.strip() for block in blocks if block.strip()]
    return cleaned_blocks
