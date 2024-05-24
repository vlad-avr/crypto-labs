import math
import ctypes

# Defining Left and Right Rotate
def left_Rotate(x, n):
    return ((x << n) % (2 ** 32))|(x >> (32 - n))

def right_Rotate(x, n):
    return (x >> n)|((x & ((2 ** n) - 1)) << (32 - n))

# Key gnereration Algorithm
def key_generation():
    P32 = 0xb7e15163 
    Q32 = 0x9e3779b9
    S = [0] * (2 * r + 4)
    S[0] = P32
    for i in range(1, 2 * r + 4):
        S[i] = S[i - 1] + Q32
    A = B = i = j = 0
    v = 3 * max(c, 2 * r + 4)
    for s in range(1, v + 1):
        A = S[i] = left_Rotate((S[i] + A + B) % (2 ** 32) ,3)
        B = L[j] = left_Rotate((L[j] + A + B) % (2 ** 32), (A + B) % (1 << 5))
        i = (i + 1) % (2 * r + 4)
        j = (j + 1) % c
    return S

# Encryption function
def encryption():
    P = [0] * c 
    for i in range(c):
        P[i] = 0
    for i in range(len(plaintext) -1, -1, -1):
        h = int(i/v)
        P[h] = (P[h] << 8) + plaintext[i]
# Rgisters for Function
    A = P[0]
    B = P[1]
    C = P[2]
    D = P[3]
    B = (B + S[0]) % (2 ** 32)
    D = (D + S[1]) % (2 ** 32)
    for i in range (1,r+1):
        t = left_Rotate(((B * (2 * B + 1)) % (2 ** 32)), log_value) % (2 ** 32)
        u = left_Rotate(((D * (2 * D + 1)) % (2 ** 32)), log_value) % (2 ** 32)
        t1 = t % (1 << 5)
        u1 = u % (1 << 5)
        A = left_Rotate((A ^ t), u1) + S[2 * i] 
        C = left_Rotate((C ^ u), t1) + S[2 * i + 1] 
        A = A % (2 ** 32)
        C = C % (2 ** 32)
        # Swapping of Registers
        A, B , C, D = B, C, D, A

    A = (A + S[2 * r + 2]) % (2 ** 32)
    C = (C + S[2 * r + 3]) % (2 ** 32)
    
    #Encrypting the text
    encrypted = A.to_bytes(4, byteorder = 'little') + B.to_bytes(4, byteorder = 'little') + C.to_bytes(4, byteorder = 'little') + D.to_bytes(4, byteorder = 'little')
    sourceFile = open('output.txt','w')
    print('ciphertext: ', end = "", file = sourceFile)
    for i in range(len(encrypted)):
        print('{:02x}'.format(encrypted[i]), end = " ", file = sourceFile)
    sourceFile.close()

# Decryption Function   
def decryption():  
    P = [0] * c             
    for i in range(c):
        P[i] = 0
    for i in range(len(ciphertext) -1, -1, -1):
        h = int(i/v)
        P[h] = (left_Rotate(P[h], 8) % (2 ** 32)) + ciphertext[i]
    #Registers for Function
    A = P[0]
    B = P[1]
    C = P[2]
    D = P[3]
    C = (C - S[2 * r + 3]) % (2 ** 32)
    A = (A - S[2 * r + 2]) % (2 ** 32)
    for i in range (r, 0, -1):
        A, B, C, D = D, A, B, C
        u = left_Rotate(((D * (2 * D + 1)) % (2 ** 32)), log_value) % (2 ** 32)
        t = left_Rotate(((B * (2 * B + 1)) % (2 ** 32)), log_value) % (2 ** 32)
        t1 = t %(1 << 5)
        u1 = u % (1 << 5)
        C = (((right_Rotate((C - S[2 * i + 1]) % (2 ** 32), t1)) % (2 ** 32)) ^u)
        A = (((right_Rotate((A - S[2 * i]) % (2 ** 32), u1)) % (2 ** 32)) ^t)
        A = A % (2 ** 32)
        C = C % (2 ** 32)
        
    D = (D - S[1]) % (2 ** 32)
    B = (B - S[0]) % (2 ** 32)

    # Decrypting the Text
    decrypted = A.to_bytes(4, byteorder = 'little') + B.to_bytes(4, byteorder = 'little') + C.to_bytes(4, byteorder = 'little') + D.to_bytes(4, byteorder = 'little')
    sourceFile = open('output.txt','w')
    print('plaintext: ', end="",file = sourceFile)
    for i in range(len(decrypted)):
        print('{:02x}'.format(decrypted[i]), end = " ", file = sourceFile)
    sourceFile.close()

f = open('input.txt','r')
Lines = f.readlines()

variable_key = Lines[2][9:]

userkey = ""
for i in range(len(variable_key)):
    if variable_key[i] != " ":
        userkey += variable_key[i]

Key = bytearray.fromhex(userkey) 

w, r, b = 32, 20, len(Key)
v = w/8
c = int(b/v)
log_value = int(math.log2(w))
                
for i in range(c):
    L = [0] * c

for i in range(b - 1, - 1, -1):
    h = int(i/v)
    L[h] = (L[h] << 8 ) + Key[i]

S = key_generation()

data = ""
#Checking for Encryption or Decryption
if Lines[0] == 'encryption\n':
    text = Lines[1][11:]
    for i in range(len(text)):
        if text[i] != " ":
            data += text[i]
    plaintext = bytearray.fromhex(data)
    encryption()

else:
    text = Lines[1][12:]
    for i in range(len(text)):
        if text[i] != " ":
            data += text[i]
    ciphertext = bytearray.fromhex(data)
    decryption()