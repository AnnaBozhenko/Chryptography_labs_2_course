def eng_alpha():
    start = ord('A')
    # 26 in the following formula is length of english alphabet
    return [chr(el) for el in range(start, start + 26)]


def ukr_alpha():
    alpha_string = "а, б, в, г, ґ, д, е, є, ж, з, и, і, ї, й, к, л, м, н, о, п, р, с, т, у, ф, х, ц, ч, ш, щ, ь, ю, я".upper()
    return [el for el in alpha_string if el != ',' and el != ' ']


def ru_alpha():
    alpha_string = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    return [el for el in alpha_string]


def table(alpha):
    for i in range(len(alpha)):
        for j in range(len(alpha)):
            if j == len(alpha) - 1:
                print(alpha[(i + j) % len(alpha)])
            else:
                print(alpha[(i + j) % len(alpha)] + " ", end="")


def vigenere_encode(text, key_word, alpha):
    encoded_text = []
    for position in range(len(text)):
        key_letter = key_word[position % len(key_word)]
        encoded_letter = alpha[(alpha.index(text[position]) + alpha.index(key_letter)) % len(alpha)]
        encoded_text.append(encoded_letter)
    return ''.join(encoded_text)


def vigenere_decode(text, key_word, alpha):
    decoded_text = []
    for position in range(len(text)):
        key_letter = key_word[position % len(key_word)]
        decoded_letter = alpha[(alpha.index(text[position]) - alpha.index(key_letter)) % len(alpha)]
        decoded_text.append(decoded_letter)
    return ''.join(decoded_text)


alphabet = eng_alpha()
print(alphabet)
string = "WHATAWONDERFULWORLD"
key = "SUNRISE"
encoded = vigenere_encode(string, key, alphabet)
print(encoded)
print(vigenere_decode(encoded, key, alphabet))
# table(alphabet)
