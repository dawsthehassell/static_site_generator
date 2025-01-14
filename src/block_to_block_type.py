

def block_to_block_type(block: str) -> str:
    # check for code
    if block.startswith('```') and block.endswith('```'):
        return "code"
    # check for heading
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            break
    if 1 <= count <= 6 and len(block) > count and block[count] == ' ':
            return 'heading'
    # check for quote
    lines = block.split('\n')
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return "quote"
    # check for unordered list
    is_unordered = True
    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            is_unordered = False
            break
    if is_unordered:
        return "unordered_list"
    #check for ordered list
    expected_number = 1
    is_ordered = True
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            is_ordered = False
            break
        expected_number += 1
    if is_ordered:
        return "ordered_list"
    # default case
    return "paragraph"

