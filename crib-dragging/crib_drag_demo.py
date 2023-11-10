import crib_drag as cd

import sys
CLEAR = "\x1b[2K"


def clear_console():
    for _ in range(50):
        print()
    print(CLEAR)


def crib_dragger(msg1, msg2, bytes_a, bytes_b, crib):
    found_strings = cd.run_crib_drag(cd.byte_xor(bytes_a, bytes_b), crib)
    return msg1 in found_strings or msg2 in found_strings


def main():
    args = sys.argv[1:]
    if args[0] == '--default':
        with open("default_msgs.txt", "r") as f:
            msg1 = f.readline().strip()
            msg2 = f.readline().strip()
    else:
        # get two messages from the user
        confirmed = False
        while not confirmed:
            msg1 = input("Enter first message: ").strip()
            msg2 = input("Enter second message: ").strip()
            confirm_str = input(
                f"Confirm these messages?\nMessage 1: {msg1} (length {len(msg1)})\nMessage 2: {msg2}(length {len(msg2)})\n[y/n]: "
            )
            confirmed = confirm_str.lower() == "y"
    clear_console()

    # generate a random key
    key = cd.gen_key(max(len(msg1), len(msg2)))

    # write the key and messages to a answers file
    with open("answer.txt", "w") as f:
        f.write(f"key: {cd.bytes_to_hexstring(key)}\n")
        f.write(f"msg1: {msg1}\n")
        f.write(f"msg2: {msg2}\n")

    # encrypt the messages with the random key
    cipher_hex = [
        bytearray.fromhex(cd.encrypt_to_hexstring(msg1, key)),
        bytearray.fromhex(cd.encrypt_to_hexstring(msg2, key)),
    ]

    msg_1_truncated = msg1[: min(len(msg1), len(msg2))]
    msg_2_truncated = msg2[: min(len(msg1), len(msg2))]

    ready = False
    while not ready:
        ready = input("Ready to continue? [y/n]: ").lower() == "y"
    clear_console()

    found = False
    guess_count = 0
    while not found:
        # decrypt the messages with the crib
        crib = input(f"Enter crib (guess #{guess_count + 1}): ")
        found = crib_dragger(
            msg_1_truncated, msg_2_truncated, cipher_hex[0], cipher_hex[1], crib
        )
        guess_count += 1

    print(f"Messages decrypted successfully! Total guesses: {guess_count}")
    print(f"Message 1: {msg1}")
    print(f"Message 2: {msg2}")
    print(f"Key: {cd.bytes_to_hexstring(key)}")
    return


if __name__ == "__main__":
    main()
