import math
import hashlib
 
# Function to left
# rotate n by d bits
def leftRotate(n, d):
    INT_BITS = 8
    return (n << d) & 0xFF | (n >> (INT_BITS - d)) 
 
# Function to right
# rotate n by d bits
def rightRotate(n, d):
    INT_BITS = 8
    return (n >> d) | (n << (INT_BITS - d)) & 0xFF

def ByteIntArrayToHex(byteintarray):
    hexString = ''
    for byteint in (byteintarray):
        temp = (hex(byteint)[2:])
        if (len(temp)==1):
            hexString = hexString + '0' + temp
        else:
            hexString = hexString + temp
    return hexString

def HexToByteIntArray(hexString):
    byteintarray = []
    for i in range (len(hexString)//2):
        temp = '0x'
        temp = temp + hexString[i*2:i*2+2]
        temp = int(temp,16)
        byteintarray.append(temp)
    return byteintarray

def StringToByteIntArray(string):
    # Mengubah string menjadi array of integer (byte) sesuai dengan ascii/utf-8
    # Input : string
    # Output : array of integer (byte) dari string
    byteint_array = []
    
    for char in string:
        byteint_array.append(ord(char))
        
    return byteint_array

def ByteIntArrayToString (byteint_array):
    # Mengubah string menjadi array of integer (byte) sesuai dengan ascii/utf-8
    # Input : array of integer (byte) 
    # Output : string
    string = "".join([chr(value) for value in byteint_array])
        
    return string

def OpenFileAsByteIntArray(filename):
    # Membuka file dengan nama filename per byte lalu menyimpannya menjadi array of integer (byte)
    # Input : filename
    # Output : array of integer (byte) dari isi file
    
    # Buka file
    input_file = open(filename,"rb")
    
    # Baca isi file per byte hingga habis
    byteint_array = []
    byte = input_file.read(1)
    while (byte):
        # Ubah byte tersebut menjadi integer yang sesuai lalu masukkan ke array
        byteint = int.from_bytes(byte,byteorder='little')
        byteint_array.append(byteint)
        byte = input_file.read(1)
        
    # Tutup file
    input_file.close()
        
    return byteint_array

def EncryptImage(image_byteintarray):
    init = 255
    text_byteintarray = []
    for byteint in (image_byteintarray):
        xor = init^byteint
        enc = leftRotate(xor, 3)
        text_byteintarray.append(enc)
        init = enc  
    return text_byteintarray

def DecryptText(text_byteintarray):
    init = 255
    image_byteintarray = []
    for byteint in (text_byteintarray):
        dec = rightRotate(byteint, 3)
        xor = init^dec
        image_byteintarray.append(xor)
        init = byteint
    return image_byteintarray