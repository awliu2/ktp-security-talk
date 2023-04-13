import binascii
import sys


cipher_hex = [b'c2b8fd15d46e6008a97cc3644390b24a2cc784a7a4144dd504f431ec4a0456dfccdfb06d428d8016fc583526b73287deea40',
			  b'ccabe40695025d15ec61d164729ae6563e8b9cb6e15378d31ffb3af8190558c3c993f358559c811df7143838ee53afc8e21a'
]

recovered = []


cipher_bin = [binascii.unhexlify(c) for c in cipher_hex]
# xors two byte arrays
def byte_xor(a, b):
    if len(a) > len(b):
        a = a[:len(b)]
    else:
        b = b[:len(a)]
    return ([(ch_a ^ ch_b) for ch_a, ch_b in zip(a, b)])


# function to crib drag, and write meaningful results to an outfile
def crib_drag(xor_ed, crib):    
    f = open('cribs.txt', 'w')
    f.write(f"crib: [{crib}]")
    for i in range(len(xor_ed)):
        
        out_b = byte_xor(xor_ed[i:], bytearray(crib.encode()))
        string = ''.join([chr(c) for c in out_b])
        if all(x.isalnum() or x.isspace() or x =='.' for x in string):
            msg = f'\n[{i}]\n{string}'
            print(msg)
            f.write(msg + '\n')


# xors two byte arrays
def byte_xor(a, b):
    if len(a) > len(b):
        a = a[:len(b)]
    else:
        b = b[:len(a)]
    return ([(ch_a ^ ch_b) for ch_a, ch_b in zip(a, b)])


def verify():
    key = (byte_xor(cipher_bin[2], recovered[2]))
    # for i, p in enumerate(recovered):
    #     key = (byte_xor(ctxts_bin[i], p))
    #     print(key)

    for b in cipher_bin:
        asciis = [byte for byte in (byte_xor(b, key))]
        chars = [chr(byte) for byte in (byte_xor(b, key))]
        print(asciis)
        print(''.join(chars), end='')
        

def main():
    if ('-v') in sys.argv:
            verify()
            sys.argv.remove('-v')
    if len(sys.argv) > 1:
        arr1 = int(sys.argv[1])
        arr2 = int(sys.argv[2])
        crib = sys.argv[3]
        if (not 0 <= arr1 <= 3) or (not 0 <= arr2 <= 3):
            print('arrays out of range')
            exit()
        
        crib_drag(byte_xor(cipher_bin[arr1], 
                        cipher_bin[arr2]),
                        crib)

if __name__ == '__main__':
    main()