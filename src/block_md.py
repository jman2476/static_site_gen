from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH='paragraph'
    HEADING='heading'
    CODE='code'
    QUOTE='quote'
    UNORDERED_LIST='unordered list'
    ORDERED_LIST='ordered list'

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    clean_blocks = []

    for block in blocks:
        stripped = block.strip()
        if stripped != '':
            clean_blocks.append(stripped)

    return clean_blocks

def block_to_lines(block):
    return block.split('\n')

def check_valid_first_char(lines, expected, ordered=False):
    valid = True
    if not ordered:
        for line in lines:
            if line[0:1] != expected:
                valid = False
                break
    else:
        for line in lines:
            if line[0:2] != f'{expected}.':
                valid = False
                break
            expected += 1
    return valid

def block_to_block_type(block):
    if len(re.findall(r'^(#{1,6} .+)', block)):
        return BlockType.HEADING
    if len(re.findall(r'^(`{3})\n(.*\n)*(`{3}$)', block)):
        return BlockType.CODE
    lines = block_to_lines(block)
    first_char = lines[0][0:1]
    if first_char == '>':
        valid = check_valid_first_char(lines, '>')
        if valid:
            return BlockType.QUOTE
    if first_char == '-' or first_char == '+':
        minus, plus = (
            check_valid_first_char(lines, '-'),
            check_valid_first_char(lines, '+')
        )
        if minus or plus:
            return BlockType.UNORDERED_LIST
    if first_char == '1':
        valid = check_valid_first_char(
            lines, 1, True
        )
        if valid:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH