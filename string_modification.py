def string_to_bits(s):
    # Convert each character to its ASCII value, then to its binary representation.
    return ''.join(format(ord(char), '08b') for char in s)

def bits_to_string(bits):
    # Split the bit string into chunks of 8 bits (since each character is 8 bits long)
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    # Convert each 8-bit chunk to a character using chr(int(bit_string, 2))
    return ''.join(chr(int(char, 2)) for char in chars)