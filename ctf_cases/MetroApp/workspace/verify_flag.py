from pathlib import Path
import string
import struct

EXE = Path('workspace/appx/MetroApp.exe')
b = EXE.read_bytes()
assert b[:2] == b'MZ', 'not a PE file'
pe = struct.unpack_from('<I', b, 0x3C)[0]
assert b[pe:pe + 4] == b'PE\0\0', 'bad PE signature'
number_sections = struct.unpack_from('<H', b, pe + 6)[0]
opt_size = struct.unpack_from('<H', b, pe + 20)[0]
section_table = pe + 24 + opt_size
sections = {}
for i in range(number_sections):
    off = section_table + i * 40
    name = b[off:off + 8].split(b'\0', 1)[0].decode('ascii', 'replace')
    virtual_size, virtual_address, raw_size, raw_pointer = struct.unpack_from('<IIII', b, off + 8)
    sections[name] = (virtual_address, virtual_size, raw_pointer, raw_size)

image_base = struct.unpack_from('<I', b, pe + 24 + 28)[0]

def file_to_va(file_offset: int) -> int:
    for va, vsize, raw, rsize in sections.values():
        if raw <= file_offset < raw + rsize:
            return image_base + va + file_offset - raw
    raise AssertionError(f'no section for file offset {file_offset:#x}')

def va_to_file(va: int) -> int:
    rva = va - image_base
    for sva, vsize, raw, rsize in sections.values():
        if sva <= rva < sva + max(vsize, rsize):
            return raw + rva - sva
    raise AssertionError(f'no section for VA {va:#x}')

def find_utf16(text: str) -> int:
    needle = text.encode('utf-16le') + b'\0\0'
    pos = b.find(needle)
    assert pos >= 0, f'missing UTF-16 literal: {text}'
    return pos

text_va, text_size, text_raw, text_raw_size = sections['.text']
text = b[text_raw:text_raw + text_raw_size]

# The decisive loop is: next = ROL8(current, current & 7) XOR key[i & 7].
# The eight-byte key is embedded at VA 0x4307a8.  The nearby instructions
# contain ROL and XOR opcodes, which prevents a lone string literal from being
# mistaken for the accepted input.
KEY_VA = 0x4307A8
key_file = va_to_file(KEY_VA)
key = list(b[key_file:key_file + 8])
assert key == [0x77, 0xAD, 0x07, 0x02, 0xA5, 0x00, 0x29, 0x99]

rol_opcode = b'\xD2\xC2'
xor_opcode = b'\x32\x90\xA8\x07\x43\x00'
assert rol_opcode in text and xor_opcode in text

def rol8(value: int, count: int) -> int:
    count &= 7
    return value & 0xFF if count == 0 else ((value << count) | (value >> (8 - count))) & 0xFF


def generate_chain(first: str) -> str | None:
    values = [ord(first)]
    current = values[0]
    for i in range(20):
        next_value = (key[i & 7] ^ rol8(current, current & 7)) & 0xFF
        if next_value == 0:
            return ''.join(chr(value) for value in values)
        values.append(next_value)
        current = next_value
    return None


charset = string.ascii_uppercase + string.digits
raw_candidates = [generate_chain(first) for first in charset]
raw_candidates = [candidate for candidate in raw_candidates if candidate is not None]
assert raw_candidates == ['Cm', 'D34DF4C3']
valid_candidates = [candidate for candidate in raw_candidates if all(char in charset for char in candidate)]
assert valid_candidates == ['D34DF4C3']

find_utf16('MERONG')  # decoy literal; presence is not accepted-input proof.
find_utf16('Correct!')
find_utf16('Wrong')
find_utf16('PasswordInput')

print('PASS: MetroApp.exe is x86 PE')
print(f'embedded key VA={KEY_VA:#x} bytes={bytes(key).hex(" ")}')
print(f'ROL/XOR opcode evidence at .text: {rol_opcode.hex()} / {xor_opcode.hex()}')
print(f'raw NUL-terminated candidates: {raw_candidates}')
print(f'charset-valid artifact-derived flag: {valid_candidates[0]}')
