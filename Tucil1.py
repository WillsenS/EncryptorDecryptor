import random
import string
from collections import OrderedDict
import numpy as np

def ArrangeText(text):
    text.lower()
    newText = ""
    for i in range(len(text)):
        if (ord(text[i]) < 97) or (ord(text[i]) > 122):
            pass
        else :
            newText += text[i]
    return newText

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

def ExtendedVigenereEncrypt(text,key):
    encrypted = ""
    for i in range(len(text)):
            encrypted += chr(((ord(text[i])) + (ord(key[(i % len(key))]))))
    return encrypted

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

def VigenerDecrypt(text,key):
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

def RNDTableGenerator():
    table = []
    for i in range (26):
        data = list(string.ascii_uppercase)
        random.shuffle(data)
        table.append(data)
    return table

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

def bigram(text):
    text = text.lower()
    text = ArrangeText(text)
    text = text.replace("j", "i")
    text = text.upper()
    bigramList = []
    j = 0
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

def findPosition(table,text):
    for i in table:
        if text in i:
            return (table.index(i), i.index(text))

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


def PlayfairC(text,key):
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
    bigramList = bigram(text)
    NewText = ""
    NewText = NewText.join(bigramList)
    print(PlayfairEncrypt(table,NewText))
    
def SuperEncrypt(text, key):
    FirstEncrypt = VigenereEncrypt(text,key)
    FirstEncrypt = ArrangeText(FirstEncrypt.lower())
    text = ArrangeText(text)
    #Define matriks as len(text)


print("Welcome to encryptor")
print("masukkan pilihan :")
print("1. basic vigenere")
print("2. full vigenere")
print("3. Auto key vigenere")
print("4. Extended vigenere")
print("5. Playfair vigenere")
print("6. Super Encryption")
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
    print("Terenkripsi : " + AutoKeyVigenereEncrypt(text,key))

if (pilihan == "4"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    print("Terenkripsi : " + ExtendedVigenereEncrypt(text,key))

if (pilihan == "5"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    PlayfairC(text,key)

if (pilihan == "6"):
    text = input("Masukan Teks: ")
    key = input("Masukkan Key: ")
    print("Terenkripsi : " + VigenereEncrypt(text,key))