from Crypto.Cipher import AES
from sys import argv
from Crypto import Random
from array import array
from itertools import cycle


def main():
   cipher = submit()
   print(cipher)

def submit():
  plainText = producePlainText()
  return cbc_plainText_encrypt(plainText)  
 
# Encodes a plainText to be like urls  
def urlEncode(plainText):
   i = 0
   for c in plainText:
      if c == ';':
         plainText = plainText[:i] + '%3B'  + plainText[i+1:]
      elif c == '=':
         plainText = plainText[:i] + '%3D'  + plainText[i+1:]
      i += 1
   print(plainText)
   return plainText

# Takes user input, url encodes it, and prepares the PlainText  
def producePlainText():

   string = input("What string would you like to submit()? ")
   string = urlEncode(string)
   return "userid=456;userdate=" + string + "session-id=31337"
            
def pkcs7(plaintext):
   if len(plaintext) == 16:
      pad_len = 16
   else:
      pad_len = 16 - len(plaintext)
   pad_char = pad_len.to_bytes(1, byteorder='big')
   pad_utf8 = pad_char.decode('utf-8', 'raise')
   pad_str = ''
   for i in range(pad_len):
      plaintext += pad_char
   return plaintext

def cbc_plainText_encrypt(plainText):
   
   key = Random.get_random_bytes(16) 
   aes = AES.new(key)
   iv = bytearray(Random.get_random_bytes(16))
 
   i = 0 
   j = 15
   
   lastMBlock = False
   data = bytearray(plainText, 'utf8')
   # read the plaintext and pad if necessary to create block of 16 bytes
   mblock0 = data[:j]
    
   if len(mblock0) < 16:
      mblock0_padded = pkcs7(mblock0)
      lastMBlock = True
   else:
      mblock0_padded = mblock0
   
   # xor message with IV and encrypt it
   to_encrypt0 = xor(mblock0_padded, iv)
   cipher0 = aes.encrypt(bytes(to_encrypt0))
   completeCipher = cipher0
   print(completeCipher)   
   print(lastMBlock)
   prev_cipher = cipher0
   while not lastMBlock:
      i +=  16
      j +=  16
      # read the plaintext and pad if necessary to create block of 16 bytes
      mblock = data[i:j]
      if len(mblock) == 0:
         break
      mblock_padded = pkcs7(mblock)

      # xor message with previous cipher and encrypt it
      to_encrypt = xor(mblock_padded, prev_cipher)
      new_cipher = aes.encrypt(bytes(to_encrypt))
         
      # write the new cipher to the outfile
      completeCipher += new_cipher
      print("Added to cipher is: " + completeCipher)
      prev_cipher = new_cipher
 
   return completeCipher   
  
def xor(x,y):
    return bytearray([a^b for a, b in zip(x, cycle(y))])

if __name__ == '__main__':
   main()
