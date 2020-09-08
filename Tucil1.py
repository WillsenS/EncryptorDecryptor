import random
import string
from collections import OrderedDict
import numpy as np

# menghapus tanda baca dan spasi, serta membuat text menjadi huruf kecil
# input : Text
# Output : Text yang sudah dibersihkan
def ArrangeText(text):
    text.lower()
    newText = ""
    for i in range(len(text)):
        if (ord(text[i]) < 97) or (ord(text[i]) > 122):
            pass
        else :
            newText += text[i]
    return newText

#***************** BASIC VIGENERE ********************

# Mengenkripsi kata dengan basic vigenere sesuai key (hanya 26 alfabet)
# Input: text , key
# output: Text yang terenkripsi dalam upper case
# catatan: Tanda baca beserta spasi tidak dibuang
def VigenereEncrypt(text,key):
    text = text.lower()
    key = ArrangeText(key.lower())
    encrypted = ""
    j = 0
    for i in range(len(text)):
        if (ord(text[i]) < 97) or (ord(text[i]) > 122):
            encrypted += text[i]
        else:
            encrypted += chr(((ord(text[i])-97) + (ord(key[(j % len(key))]) - 97))  % 26 + 97)
            j += 1
    return encrypted.upper()

# Dekripsi Vigenere sesuai key
# Input: text , key
# output: Text yang terdekripsi
def VigenereDecrypt(text,key):
    text = text.lower()
    key = ArrangeText(key.lower())
    decrypted = ""
    j = 0
    for i in range(len(text)):
        if (ord(text[i]) < 97) or (ord(text[i]) > 122):
            decrypted += text[i]
        else:
            decrypted += chr(((ord(text[i])-97) - (ord(key[(j % len(key))]) - 97))  % 26 + 97)
            j += 1
    return decrypted()

#**************** EXTENDED VIGENERE *************************

# Mengenkripsi kata dengan extended vigenere sesuai key (256 ASCII)
# input: text, key
# output: text yang terenkripsi
def ExtendedVigenereEncrypt(text,key):
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(((ord(text[i])) + (ord(key[(i % len(key))]))))
    return encrypted

def ExtendedVigenereDecrypt(text,key):
    decrypted = ""
    for i in range(len(text)):
        decrypted += chr(((ord(text[i])) - (ord(key[(i % len(key))]))))
    return decrypted

#************** AUTOKEY VIGENERE ***************************

# Mengenkripsi kata dengan Auto Key Vigenere sesuai key
# Input: text , key
# output: Text yang terenkripsi dalam upper case
def AutoKeyVigenereEncrypt(text,key):
    text = text.lower()
    ProcessedText = ArrangeText(text)
    key = ArrangeText(key.lower())
    encrypted = ""
    if (len(ProcessedText) > len(key)):
        i = 0
        while (len(key) < len(ProcessedText)):
            key += ProcessedText[i]
            i += 1
    j = 0
    for i in range(len(text)):
        if (ord(text[i]) < 97) or (ord(text[i]) > 122):
            encrypted += text[i]
        else:
            encrypted += chr(((ord(text[i])-97) + (ord(key[(j % len(key))]) - 97))  % 26 + 97)
            j += 1
    return encrypted.upper()

# Dekripsi Auto Key Vigenere
# Input : text, key
# Output: String tanpa tanda baca dan spasi
def AutoKeyVigenereDecrypt(text,key):
    text = text.lower()
    text = ArrangeText(text)
    key = ArrangeText(key.lower())
    decrypted = ""
    j = 0
    for i in range(len(text)):
        temp = ""
        temp = chr(((ord(text[i])-97) - (ord(key[(i % len(key))]) - 97))  % 26 + 97)
        key += temp
        decrypted += temp
    return decrypted

#**************** FULL VIGENERE *********************

# Mengenerate sebuah Table berisi random alfabet unik dalam upper case
# Return Table of random generated alphabet
def RNDTableGenerator():
    table = []
    for i in range (26):
        data = list(string.ascii_uppercase)
        random.shuffle(data)
        table.append(data)
    return table

# Full Vigenere
# Input: text , key, table
# output: Text yang terenkripsi dalam upper case
def FullVigenereC(text,key,table):
    text = text.lower()
    key = ArrangeText(key.lower())
    encrypted = ""
    j = 0
    for i in range(len(text)):
        if (ord(text[i]) < 97) or (ord(text[i]) > 122):
            encrypted += text[i]
        else:
            baris = ord(key[(j % len(key))]) - 97
            kolom = ord(text[i]) - 97
            encrypted += table[baris][kolom]
            j += 1
    return encrypted.upper()


#******************* PLAYFAIR CIPHER********************

# Mengenerate Bigram dari text sesuai dengan aturan playfair cipher
# Mengganti huruf J menjadi i dan menambahkan x jika duplikat/ganjil
# Input: text
# output: List of 2 char
def bigram(text):
    text = text.lower()
    text = ArrangeText(text)
    text = text.replace("j", "i")
    text = text.upper()
    bigramList = []
    for i in range(len(text)):
        if (i > 0) and (i % 2 == 1):
            continue
        if text[i] == text[i+1]:
            text = text[:i+1] + "X" + text[i+1:]
            i+= 1
        else:
            i += 1
    if len(text) % 2 == 1:
        text += "X"
    bigramList = [(text[i:i+2]) for i in range(0, len(text), 2)]
    return bigramList


# Mencari posisi text pada table
# Input: table, char 
# Output: index text
def findPosition(table,text):
    for i in table:
        if text in i:
            return (table.index(i), i.index(text))


# Enkripsi Playfair
# input: table, string bigram
# output: list of bigram
def PlayfairEncrypt(table,bigram):
    NewBigram = []
    for i in range(len(bigram) // 2):
        pos1 = findPosition(table,bigram[i*2])
        pos2 = findPosition(table,bigram[i*2 + 1])
        if pos1[0] == pos2[0]:
            temp = table[pos1[0]][(pos1[1] + 1) % 5] + table[pos2[0]][(pos2[1] + 1) % 5]
            NewBigram.append(temp)
        elif pos1[1] == pos2[1]:
            temp = table[(pos1[0] + 1) % 5][pos1[1]] + table[(pos2[0] + 1) % 5][pos2[1]]
            NewBigram.append(temp)
        else:
            temp = table[(pos1[0])][pos2[1]] + table[(pos2[0])][pos1[1]]
            NewBigram.append(temp)
    return NewBigram


# Dekripsi Playfair menjadi bigram
# input: table, text
# output: text
def PlayfairDecrypt(table,text):
    bigram = ""
    bigram = bigram.join(text)
    NewBigram = []
    for i in range(len(bigram) // 2):
        pos1 = findPosition(table,bigram[i*2])
        pos2 = findPosition(table,bigram[i*2 + 1])
        if pos1[0] == pos2[0]:
            temp = table[pos1[0]][(pos1[1] + 4) % 5] + table[pos2[0]][(pos2[1] + 4) % 5]
            NewBigram.append(temp)
        elif pos1[1] == pos2[1]:
            temp = table[(pos1[0] + 4) % 5][pos1[1]] + table[(pos2[0] + 4) % 5][pos2[1]]
            NewBigram.append(temp)
        else:
            temp = table[(pos1[0])][pos2[1]] + table[(pos2[0])][pos1[1]]
            NewBigram.append(temp)
    decrypt = ""
    decrypt = decrypt.join(NewBigram)
    decrypt = decrypt.replace("X","")
    return(decrypt.lower())

# Mengenerate playfair table
def playfairTable(text,key):
    text= text.upper()
    key = key.lower()
    MagicKey = "abcdefghijklmnopqrstuvwxyz"
    NewKey = ArrangeText(key)
    NewKey += MagicKey
    NewKey = "".join(OrderedDict.fromkeys(NewKey))
    NewKey = NewKey.replace("j","")
    NewKey = NewKey.upper()
    table = []
    for i in range(5):
        data = []
        for j in range (5):
            data.append(NewKey[i*5 + j])
        table.append(data)
    return table

# inisialisasi playfair
# return bigram encrypted
def PlayfairC(table,text,key):
    bigramList = bigram(text)
    NewText = ""
    NewText = NewText.join(bigramList)
    return(PlayfairEncrypt(table,NewText))


#******************* SUPER ENCRYPT ***********************

# Super Encrypt
# Dengan enkripsi vigenere basic dan transpose matrix dengan 2 kolom
# input: text,key
# output: text terenkripsi (upper case)  
def SuperEncrypt(text, key):
    FirstEncrypt = VigenereEncrypt(text,key)
    FirstEncrypt = ArrangeText(FirstEncrypt.lower())
    if (len(FirstEncrypt) % 2) == 1 :
        FirstEncrypt += "z"
    print("firstencrypt : " + FirstEncrypt)
    matrix = []
    j = 0
    for i in range(len(FirstEncrypt) // 2):
        TempArray = [FirstEncrypt[j],FirstEncrypt[j+1]]
        matrix.append(TempArray)
        j += 2
    numpyArray = np.array(matrix)
    numpyTranspose = numpyArray.T
    TransposeMatrix = numpyTranspose.tolist()
    print(TransposeMatrix)
    Encrypted = ""
    for i in range(2):
        for j in TransposeMatrix[i]:
            Encrypted += j
    return Encrypted.upper()

#************** AFFINE CIPHER ********************

# Check if a is coprime to b
# return boolean
def checkCoprime (a,b):
    if (a % 2) == 0 :
        return False
    else :
        if (b % a) == 0 :
            return False
        else:
            return True

# Affine Encryption
# Input: String, integer(coprime dengan 26), integer
# output: String uppercase
def affineCipherEncrypt (text,m,b):
    text = ArrangeText(text.lower())
    Encrypted = ""
    for i in text:
        Encrypted += chr(( (m * (ord(i) - 97) + b) % 26) + 97)
    return Encrypted.upper()

# mencari modulus multiplication inverse
# input: int, int
# output: int
def modInverse(a,b):
    i = 1
    found = False
    while not(found):
        if (a*i) % b == 1:
           found = True
        else:
            i += 1
    return i

# Dekripsi Affine
# input: string text, int key(coprime dengan 26), int key
# output: string text (lowercase)
def affineCipherDecrypt (text,m,b):
    text = ArrangeText(text.lower())
    Decrypted = ""
    mInverse = modInverse(m,26)
    print (mInverse)
    for i in text:
        Decrypted += chr( (mInverse * (ord(i) - 97 - b) % 26) + 97)
    return Decrypted


#************** MAIN PROGRAM *********************

print("Welcome to encryptor")
print("masukkan pilihan :")
print("1. basic vigenere")
print("2. full vigenere")
print("3. Auto key vigenere")
print("4. Extended vigenere")
print("5. Playfair vigenere")
print("6. Super Encryption")
print("7. Affine")
pilihan = input("pilihan anda: ")

if (pilihan == "1"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    print("Terenkripsi : " + VigenereEncrypt(text,key))

if (pilihan == "2"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    table = RNDTableGenerator()
    print(table)
    print("Terenkripsi : " + FullVigenereC(text,key,table))

if (pilihan == "3"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    enc = AutoKeyVigenereEncrypt(text,key)
    print("Terenkripsi : " + enc)
    print("Dekripsi : " + AutoKeyVigenereDecrypt(enc,key))

if (pilihan == "4"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    print("Terenkripsi : " + ExtendedVigenereEncrypt(text,key))

if (pilihan == "5"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    table = playfairTable(text,key)
    print("encrypted : " ,end ="")
    print(PlayfairC(table,text,key))
    print(PlayfairDecrypt(table, PlayfairC(table,text,key)))

if (pilihan == "6"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    print(SuperEncrypt(text,key))

if (pilihan == "7"):
    text = input("Masukan Teks: ")
    checkKey = False
    while not(checkKey):
        keyA = int(input("Masukkan Key integer yang koprima dengan 26: "))
        if checkCoprime(keyA,26):
            checkKey = True
        else:
            print("tidak koprima!")
    keyB = int(input("Masukkan Key integer ke 2: "))
    enc = affineCipherEncrypt(text,keyA,keyB)
    print(enc)
    print(affineCipherDecrypt(enc,keyA,keyB))