import binascii
import sys
import os

cipher_hex = [
    b"c2b8fd15d46e6008a97cc3644390b24a2cc784a7a4144dd504f431ec4a0456dfccdfb06d428d8016fc583526b73287deea40",
    b"ccabe40695025d15ec61d164729ae6563e8b9cb6e15378d31ffb3af8190558c3c993f358559c811df7143838ee53afc8e21a",
    b"ddb1e845c43b5d03a728c0367c8efc03398888efab4170d718b23be95c1f19c5c5d6b05546949158f75b3d",
]

cipher_bin = [binascii.unhexlify(c) for c in cipher_hex]


def byte_xor(a, b):
    """
    XOR two byte arrays and returns the result as a byte array
    length of result is the length of the shorter input array
    """
    if len(a) > len(b):
        a = a[: len(b)]
    else:
        b = b[: len(a)]
    return [(ch_a ^ ch_b) for ch_a, ch_b in zip(a, b)]


def byte_array_to_string(byte_arr):
    """
    Converts a byte array to a string
    """
    return "".join([chr(c) for c in byte_arr])


def valid_punctuation(char):
    return char in ".,?!:;'\"-"


def run_crib_drag(xor_ed, crib):
    """
    Performs crib dragging on a byte array that has been XORed with another
    byte array. Prints out possible substrings that could have been included in
    the message. Also writes these results to an outfile.
    """
    found_messages = []
    indices = []
    with open("cribs.txt", "w") as f:
        f.write(f"crib: [{crib}]")
        for i in range(len(xor_ed)):
            out_b = byte_xor(xor_ed[i:], bytearray(crib.encode()))
            string = "".join([chr(c) for c in out_b])
            if all(c.isalnum() or c.isspace() or valid_punctuation(c) for c in string):
                msg = f"\n[{i}]\n{string}"
                # print(msg)
                f.write(msg + "\n")
                found_messages.append(string)
                indices.append(i)
    # print out all found messages and their indices in a table
    print("Found messages:")
    print("Index\tMessage")
    for i, msg in zip(indices, found_messages):
        print(f"{i}\t{msg}")

    return found_messages


def get_key(msg, encrypted_bytes):
    """
    Given a string message and its corresponding encrypted byte array,
    returns the key used to encrypt the message
    """
    msg_byte_arr = bytearray(msg.encode())
    return byte_xor(msg_byte_arr, encrypted_bytes)


def bytes_to_hexstring(byte_arr):
    """
    Given a byte array, returns a string of hex characters representing
    the byte array.
    """
    hex_string = "".join(format(num, "02x") for num in byte_arr)
    return hex_string


def encrypt_to_byte_array(msg, key):
    """
    Encrypts a message using a key and returns the encrypted message
    as a byte array.
    """
    msg_byte_arr = bytearray(msg.encode())
    return byte_xor(msg_byte_arr, key)


def encrypt_to_hexstring(msg, key):
    """
    Encrypts a string message to a hex string using a provided key.
    """
    msg_byte_arr = bytearray(msg.encode())
    assert len(msg_byte_arr) <= len(key)
    encrypted_bytes = byte_xor(msg_byte_arr, key)
    return bytes_to_hexstring(encrypted_bytes)


def gen_key(length):
    """
    Generates a random key of the specified length.
    """
    return os.urandom(length)


if __name__ == "__main__":
    # a = bytearray.fromhex(cipher_hex[0].decode())
    # b = bytearray.fromhex(cipher_hex[1].decode())
    msg1 = "Kappa Theta Pi is the Professional Technology Fraternity"
    msg2 = "Eric Liu is actually getting hard carried by Andi"

    key = gen_key(max(len(msg1), len(msg2)))
    key_hex = bytes_to_hexstring(key)
    print(f"key as a hex string: {key_hex}\n")

    encrypted_1 = encrypt_to_byte_array(msg1, key)
    encrypted_2 = encrypt_to_byte_array(msg2, key)

    encrypted_hexstring1 = encrypt_to_hexstring(msg1, key)
    encrypted_hexstring2 = encrypt_to_hexstring(msg2, key)
    print(f"encrypted_hexstring 1: {encrypted_hexstring1}")
    print(f"encrypted_hexstring 2: {encrypted_hexstring2}\n")

    print(f"decrypted message 1: {byte_array_to_string(byte_xor(encrypted_1, key))}")
    print(f"decrypted message 2: {byte_array_to_string(byte_xor(encrypted_2, key))}\n")

    print(
        f"extracting the key from msg1: {bytes_to_hexstring(get_key(msg1, encrypted_1))}"
    )
    print(
        f"extracting the key from the msg2: {bytes_to_hexstring(get_key(msg2, encrypted_2))}"
    )
    # print(f"decrypted message 2: {byte_xor(b, key)}")
    # msg2 = "The quick brown fox jumps over the lazy dog"
