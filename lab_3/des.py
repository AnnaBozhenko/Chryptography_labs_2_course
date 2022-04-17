#-*- coding: utf8 -*-
ENCRYPT = 0
DECRYPT = 1

def string_to_bit_array(text):#Convert a string into a list of bits
    array = list()
    for char in text:
        binval = binvalue(char, 8)#Get the char value on one byte
        array.extend([int(x) for x in list(binval)]) #Add the bits to the final list
    return array


def bit_array_to_string(array): #Recreate the string from the bit array
    res = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in  nsplit(array,8)]])   
    return res


def binvalue(val, bitsize):
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "Binary value larger than the expected size."
    while len(binval) < bitsize:
        binval = "0" + binval 
    return binval


def nsplit(s, n):
    """Split a list into sublists of size 'n'"""
    return [s[k:k+n] for k in range(0, len(s), n)]


class DES():
        #Initial permut matrix for the datas
    __PI = [58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7]

    #Initial permut made on the key
    __CP_1 = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    #Permut applied on shifted key to get Ki+1
    __CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32]

    #Expand matrix to get a 48bits matrix of datas to apply the xor with Ki
    __E = [32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1]

    #SBOX
    __S_BOX = [
            
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],  

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ], 

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ], 

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]
    ]

    #Permut made after each SBox substitution for each round
    __P = [16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25]

    #Final permut for datas after the 16 rounds
    __PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]

    #Matrix that determine the shift for each round of keys
    __SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()
        

    def run(self, key, text, action, padding):
        if len(key) < 8:
            raise "Key should be 8 bytes long."
        elif len(key) > 8:
            key = key[:8] 
        
        self.password = key
        self.text = text

        if action == ENCRYPT:
            # show log
            print(f"\n{' ENCRYPTION '.center(114, '=')}\n")
            if padding:
                self.addPadding()
            elif len(self.text) % 8 != 0:
                raise "Text length must be divisible by 8 if padding not supplied."
    
        self.generatekeys()        

        if action == DECRYPT:
            # show log
            print(f"\n{' DECRYPTION '.center(114, '=')}\n")
            self.keys.reverse()

        text_blocks = nsplit(self.text, 8)
        result = []
        for block in text_blocks: 
            block = string_to_bit_array(block)
            # show log            
            print("#"*114)
            show_log("Block:", show_bit_arr(block, 8), 42)

            block = self.permute(block, DES.__PI) 
            left, right = nsplit(block, 32) 
            tmp = None

            for i in range(16): 
                # show log
                print(f"--ROUND #{i}--")
                show_log(f"Left_{i}:", show_bit_arr(left, 8), 42)
                show_log(f"Right_{i}:", show_bit_arr(right, 8), 42)

                right_e = self.permute(right, DES.__E)
                # show log
                show_log(f"Key_{i}:", show_bit_arr(self.keys[i], 8), 42)
                show_log(f"Right_{i} (after permutation):", show_bit_arr(right_e, 8), 42)

                tmp = self.xor(self.keys[i], right_e)
                # show log
                show_log(f"Right_{i} (after XOR with key_{i}:", show_bit_arr(tmp, 8), 42)

                tmp = self.substitute(tmp) 
                # show log
                show_log(f"Right_{i} (after passing through S-boxes):", show_bit_arr(tmp, 4), 42)

                tmp = self.permute(tmp, DES.__P)
                # show log
                show_log(f"Right_{i} (after permutation):", show_bit_arr(tmp, 8), 42)

                tmp = self.xor(left, tmp)
                # show log
                show_log(f"{i} XOR changed Right_{i}:", show_bit_arr(tmp, 8), 42)
                left = right
                right = tmp

            result += self.permute(right + left, DES.__PI_1) 
            # show log
            show_log(f"Final result:", show_bit_arr(result[-64:], 8), 42)

        final_res = bit_array_to_string(result)
        if action == DECRYPT and padding:
            return self.removePadding(final_res) 
        else:
            return final_res 
    

    def substitute(self, d_e):
        """Pass block of 48 bits through operation with S-boxes to gain block of 32 bits"""
        subblocks = nsplit(d_e, 6) 
        result = []
        for idx, block in enumerate(subblocks):
            row = int(str(block[0]) + str(block[-1]), 2)
            column = int(''.join(str(x) for x in block[1:][:-1]), 2)
            val = DES.__S_BOX[idx][row][column] 
            result += [int(x) for x in binvalue(val, 4)] 
        return result
        

    def permute(self, block, table):
        """ Transform block (represented as list of bits) using bit position table """
        return [block[x - 1] for x in table]
    

    def xor(self, t1, t2):
        return [x^y for x, y in zip(t1, t2)]
    

    def generatekeys(self):
        """ Generate all 16 bit shifted versions of key at once"""
        self.keys = []

        print(f"\n{' KEYS GENERATING '.center(114, '=')}\n")
        key = string_to_bit_array(self.password)
        key = self.permute(key, DES.__CP_1)

        show_log("Key permutation:", show_bit_arr(key, 8), 42) 
        left, right = nsplit(key, 28) 
        show_log("Splitted key (left part):", show_bit_arr(left, 4), 42)
        show_log("Splitted key (right part):", show_bit_arr(left, 4), 42)
        for i in range(16): 
            left, right = self.shift(left, right, DES.__SHIFT[i]) 
            show_log(f"Shifted left_{i} part", show_bit_arr(left, 4), 42)
            show_log(f"Shifted right_{i} part:", show_bit_arr(right, 4), 42)
            tmp = left + right 
            show_log("United parts:", show_bit_arr(tmp, 8), 42)
            self.keys.append(self.permute(tmp, DES.__CP_2)) 
            show_log(f"Permuted key_{i}", show_bit_arr(self.keys[-1], 8), 42)
        print("#"*114)


    def shift(self, left, right, n):
        """ Shift a list of the given value cyclically to the LEFT"""
        return left[n:] + left[:n], right[n:] + right[:n]
    

    def addPadding(self):
        """Add padding to the data using PKCS5 specification"""
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)
    

    def removePadding(self, data):
        """Remove the padding of the plain text (it is assumed that there is padding)"""
        pad_len = ord(data[-1])
        return data[:-pad_len]
    

    def encrypt(self, key, text, padding):
        return self.run(key, text, ENCRYPT, padding)
    

    def decrypt(self, key, text, padding):
        return self.run(key, text, DECRYPT, padding)



def hex_string_to_text(hex_string):
    return [chr(int(x, 16)) for x in hex_string.split()]


def text_to_hex_string(text):
    return ' '.join('{0:0>2}'.format(hex(ord(x))[2:].upper()) for x in text)


def show_byte_blocks(text):
    """text - string, function returns string in byte-blocks representation, 
    where every byte corresponds to ascii number of char"""
    s = []
    for i in text:
        a = bin(ord(i))[2:]
        if len(a) > 8:
            raise "Binary value larger than the expected size."
        s.append((8 - len(a)) * '0' + a)
    return ' '.join(s)


def show_bit_arr(arr, n):
    """arr - array of bits, function returns string representation of bits grouped in n-blocks"""
    return ' '.join(''.join(str(c) for c in i) for i in nsplit(arr, n))


def show_log(first_p, last_p, n):
    """function prints log that contains first_p aligned to left on n, and then prints last_p"""
    print(f"{first_p:_<{n}} {last_p}")
  

if __name__ == '__main__':

    t = "EC 0D 8C 83 00 78 14 63 25 CE B5 27 9F E4 73 69"
    key_hex =  '13 34 57 79 9B BC DF F1'
    t = hex_string_to_text(t)
    k = hex_string_to_text(key_hex)
    # need_to_pad = not len(t) % 8 == 0

    print(f"Key as blocks of bytes: {show_byte_blocks(k)}")
    print(f"Text as blocks of bytes: {show_byte_blocks(t)}") 
    # print(f"Text as blocks of bytes: {show_bit_arr(t, 8)}")

    
    d = DES()
    # r = d.encrypt(k, t, False)

    r2 = d.decrypt(k, t, False)
    # show_log("Ciphered:", f"{r!r}", 42)
    show_log("Deciphered:", f"{r2!r}", 42)
    # print("Ciphered (hex): {0}".format(text_to_hex_string(r)))
    print("Deciphered (hex): {0}".format(text_to_hex_string(r2)))
    