def encode(text, alphabet, step):
    encoded_text = ""
    for symb in text:
        ind = alphabet.find(symb)
        if ind != -1:
            encoded_text += chr(ord(alphabet[0]) + ((ind + step) % len(alphabet)))
        else:
            encoded_text += symb
    return encoded_text


def decode(text, alphabet, step):
    decoded_text = ""
    for symb in text:
        ind = alphabet.find(symb)
        if ind != -1:
            decoded_text += chr(ord(alphabet[0]) + (len(alphabet) + ind - step) % len(alphabet))
        else:
            decoded_text += symb
    return decoded_text


if __name__ == "__main__":
    # Encoding of the given string
    str = "There is no love sincerer than the love of food".upper()
    A = ord('A')
    alpha = "".join([chr(i) for i in range(A, A + 26)])
    encode(str, alpha, 5)
    print(f"Encoded string: {str}")


    # Decoding of the given string
    # str = """Duw lv wkh surshu wdvn ri olih.""".upper()
    # print("Encoded string: " + str)
    # A = ord('A')
    # alpha = "".join([chr(i) for i in range(A, A + 26)])
    # print("------------------------------")
    # for i in range(26):
    #     decoded = decode(str, alpha, i)
    #     print(f"Decoded string({i}): {decoded}")
