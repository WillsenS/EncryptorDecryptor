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

def ArrangeEncription(text):
    text = ArrangeText(text.lower())
    newText = ' '.join(text[i:i+5] for i in range(0, len(text), 5))
    return newText.upper()

#***************** BASIC VIGENERE ********************

# Mengenkripsi kata dengan basic vigenere sesuai key (hanya 26 alfabet)
# Input: text , key
# output: Text yang terenkripsi dalam upper case
def VigenereEncrypt(text,key):
    text = ArrangeText(text.lower())
    key = ArrangeText(key.lower())
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(((ord(text[i])-97) + (ord(key[(i % len(key))]) - 97))  % 26 + 97)
    return ArrangeEncription(encrypted)

# Dekripsi Vigenere sesuai key
# Input: text , key
# output: Text yang terdekripsi
def VigenereDecrypt(text,key):
    text = ArrangeText(text.lower())
    key = ArrangeText(key.lower())
    decrypted = ""
    for i in range(len(text)):
        decrypted += chr(((ord(text[i])-97) - (ord(key[(i % len(key))]) - 97))  % 26 + 97)
    return decrypted

#**************** EXTENDED VIGENERE *************************

# Mengenkripsi kata dengan extended vigenere sesuai key (256 ASCII)
# input: text, key
# output: text yang terenkripsi
def ExtendedVigenereEncrypt(text,key):
    encrypted = ""
    for i in range(len(text)):
        encrypted += chr(((ord(text[i])) + (ord(key[(i % len(key))]))) % 256)
    return encrypted

def ExtendedVigenereDecrypt(text,key):
    decrypted = ""
    for i in range(len(text)):
        decrypted += chr(((ord(text[i])) - (ord(key[(i % len(key))]))) % 256)
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
    return ArrangeEncription(encrypted)

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
# Return Table of random generated alphabet uppercase
def RNDTableGenerator():
    table = []
    for _ in range (26):
        data = list(string.ascii_uppercase)
        random.shuffle(data)
        table.append(data)
    return table

# Full Vigenere Encrypt
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
    return ArrangeEncription(encrypted)

# Full Vigenere Encrypt
# Input: text , key, table
# output: Text yang dekripsi
def FullVigenereDecrypt(text,key,table):
    text = ArrangeText(text.lower())
    key = ArrangeText(key.lower())
    decrypted = ""
    for i in range(len(text)):
        baris = ord(key[(i % len(key))]) - 97
        found = False
        j = 0
        while not(found):
            if(text[i].upper() == table[baris][j]):
                found = True
            else:
                j += 1
        decrypted += chr(j + 97)
    return decrypted


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
        if not(i >= len(text)-1):
            if (text[i] == text[i+1]):
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
    bigram = bigram.join(text).upper()
    NewBigram = []
    for i in range(len(bigram) // 2):
        pos1 = findPosition(table,bigram[i*2])
        pos2 = findPosition(table,bigram[i*2 + 1])
        if pos1[0] == pos2[0]:
            temp = table[pos1[0]][(pos1[1] + 4) % 5] + table[pos2[0]][(pos2[1] + 4) % 5]
        elif pos1[1] == pos2[1]:
            temp = table[(pos1[0] + 4) % 5][pos1[1]] + table[(pos2[0] + 4) % 5][pos2[1]]
        else:
            temp = table[(pos1[0])][pos2[1]] + table[(pos2[0])][pos1[1]]
        NewBigram.append(temp.rstrip('X'))
    decrypt = ""
    decrypt = decrypt.join(NewBigram)
    decrypt = decrypt.rstrip("X")
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
    matrix = []
    j = 0
    for i in range(len(FirstEncrypt) // 2):
        TempArray = [FirstEncrypt[j],FirstEncrypt[j+1]]
        matrix.append(TempArray)
        j += 2
    numpyArray = np.array(matrix)
    numpyTranspose = numpyArray.T
    TransposeMatrix = numpyTranspose.tolist()
    Encrypted = ""
    for i in range(2):
        for j in TransposeMatrix[i]:
            Encrypted += j
    return ArrangeEncription(Encrypted)

#Mengubah sebuah string menjadi list of char
def Convert(string): 
    list1=[] 
    list1[:0]=string 
    return list1

# Super Decrypt
# input: text,key
# output: text
def SuperDecrypt(text,key):
    text = ArrangeText(text.lower())
    key = ArrangeText(key.lower())
    listchar = []
    temp = text[:(len(text)//2)]
    listchar.append(Convert(temp))
    temp = text[(len(text)//2):]
    listchar.append(Convert(temp))
    listnumpy = np.array(listchar)
    arrnp = listnumpy.T
    TransposedList = arrnp.tolist()
    firstEnc = ""
    for i in TransposedList:
        for j in range(2):
            firstEnc += i[j]
    if (firstEnc[-1].upper() == 'Z') and (not(firstEnc[-2].upper() == 'Z')):
        firstEnc = firstEnc[:-1]
    decript = VigenereDecrypt(firstEnc,key)
    return decript


#************** AFFINE CIPHER ********************

# Extended Euclidean algorithm
# input: a, b : int
# output: g, x, y : int sehingga g = gcd(a, b) = ax + by
def egcd(a, b):
    xb, yb, x, y = 1, 0, 0, 1
    g, r = a, b
    while r:
        q = g // r
        g, r = r, g % r
        xb, x = x, xb - q * x
        yb, y = y, yb - q * y
    assert (a * xb + b * yb) == g
    return g, xb, yb

# Check if a is coprime to b
# return boolean
def checkCoprime (a,b):
    g, _, _ = egcd(a, b)
    return g == 1

# Affine Encryption
# Input: String, integer(coprime dengan 26), integer
# output: String uppercase
def affineCipherEncrypt (text,m,b):
    text = ArrangeText(text.lower())
    Encrypted = ""
    for i in text:
        Encrypted += chr(( (m * (ord(i) - 97) + b) % 26) + 97)
    return ArrangeEncription(Encrypted)

# mencari multiplication inverse dari a modulo n
# input: int, int
# output: int
def modInverse(a, n):
    g, x, _ = egcd(a, n)
    if g == 1:
        if x < 0: x += n
        assert 0 < x < n
        assert ((x * a) % n) == 1
        return x
    else:
        raise Exception('integer is not invertible')

# Dekripsi Affine
# input: string text, int key(coprime dengan 26), int key
# output: string text (lowercase)
def affineCipherDecrypt (text,m,b):
    text = ArrangeText(text.lower())
    Decrypted = ""
    mInverse = modInverse(m,26)
    for i in text:
        Decrypted += chr( (mInverse * (ord(i) - 97 - b) % 26) + 97)
    return Decrypted

#****************** Hill Cipher *************************

# Meminta user memasukan matrix dengan dimensi m x m
# return list of list
def inputMatrixKey(m):
    matrix = []
    for i in range(m):
        templist = []
        for j in range(m):
            masukan = input("masukkan matrix[" +str(i)+ "][" +str(j)+ "] : ")
            templist.append(int(masukan))
        matrix.append(templist)
    return matrix

# enkripsi hill cipher
# return string upper
def hillCipherEncrypt(text,m,table):
    text = ArrangeText(text.lower())
    m = int(m)
    sub = len(text) % m
    if sub != 0:
        for i in range (sub):
            text += "x"
    npTable = np.array(table)
    Encrypted = ""
    for i in range(len(text) // m):
        charlist = []
        for j in range(m):
            charlist.append(ord(text[i*m + j]) - 97)
        npCharList = np.array(charlist)
        encTable = npTable.dot(npCharList)
        for k in range(m):
            Encrypted += chr((encTable[k] % 26) + 97)
    return ArrangeEncription(Encrypted)

#Hill Decrypt
def hillCipherDecrypt(text,m,table):
    text = ArrangeText(text.lower())
    m = int(m)
    sub = len(text) % m
    if sub != 0:
        raise ValueError('input length must be a multiple of m')
    npTable = np.array(table)
    det = np.around(np.linalg.det(npTable))
    inv_det = modInverse(det, 26)
    npTable = inv_det * np.around(det * np.linalg.inv(npTable))
    Decrypted = ""
    for i in range(len(text) // m):
        charlist = []
        for j in range(m):
            charlist.append(ord(text[i*m + j]) - 97)
        npCharList = np.array(charlist)
        encTable = npTable.dot(npCharList)
        for k in range(m):
            Decrypted += chr((int(encTable[k]) % 26) + 97)
    return Decrypted

            
#************** MAIN PROGRAM *********************
def main():

    print("Welcome to encryptor")
    print("masukkan pilihan :")
    print("1. basic vigenere")
    print("2. full vigenere")
    print("3. Auto key vigenere")
    print("4. Extended vigenere")
    print("5. Playfair vigenere")
    print("6. Super Encryption")
    print("7. Affine")
    print("8. Hill")
    pilihan = input("pilihan anda: ")

    if (pilihan == "1"):
        text = input("Masukan Teks: ")
        key = input("Masukkan Key: ")
        enc = VigenereEncrypt(text,key)
        enc = ArrangeEncription(enc)
        print("Terenkripsi : " + enc)
        print(VigenereDecrypt(enc,key))

    if (pilihan == "2"):
        text = input("Masukan Teks: ")
        key = input("Masukkan Key: ")
        table = RNDTableGenerator()
        enc = FullVigenereC(text,key,table)
        print("Terenkripsi : " + enc)
        print(FullVigenereDecrypt(enc,key,table))

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
        enc = SuperEncrypt(text,key)
        print(enc)
        print(SuperDecrypt(enc,key))

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

    if (pilihan == "8"):
        text = input("Masukan Teks: ")
        m = input("dimensi: " )
        table = inputMatrixKey(int(m))
        enc = hillCipherEncrypt(text,m,table)
        print(enc)


if __name__ == '__main__':
    main()
