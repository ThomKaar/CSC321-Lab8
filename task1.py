# Written by His grace

from Crypto.Cipher import AES
from sys import argv
from Crypto import Random
from array import array
from itertools import cycle

def main(argv):
   #ecb_encrypt(argv[1], argv[2])
   cbc_encrypt(argv[1], argv[2])
 

def ecb_encrypt(inFileName, outFileName):
   # open the file
   file = open(inFileName, "rb")
   outFile = open(outFileName, "wb")
   # Create the AES obj
   randomGen = Random.new()
   obj = AES.new(randomGen.read(16))


   header, file = traverseBMPHeader(file)
   outFile.write(header)
    
   while(True):
      message = file.read(16)
      if( len(message) == 0):
         break
      elif len(message) != 16:
         notFullBlock = True
         message = pkcs7(message)
      ciphertext = obj.encrypt(message)
      outFile.write(ciphertext)
   return



def cbc_encrypt(inFileName, outFileName):
   
   key = Random.get_random_bytes(16) 
   aes = AES.new(key)
   iv = bytearray(Random.get_random_bytes(16))

   infile = open(inFileName, 'rb')
   outfile = open(outFileName, 'wb')
  
   header, infile = traverseBMPHeader(infile)
   outfile.write(header)
   

 
   lastMBlock = False
   
   # read the plaintext and pad if necessary to create block of 16 bytes
   mblock0 = bytearray(infile.read(16))
   
   if len(mblock0) < 16:
      mblock0_padded = pkcs7(mblock0)
      lastMBlock = True
   else:
      mblock0_padded = mblock0
   
   # xor message with IV and encrypt it
   to_encrypt0 = xor(mblock0_padded, iv)
   cipher0 = aes.encrypt(bytes(to_encrypt0))
   outfile.write(cipher0)
   
   prev_cipher = cipher0
   while not lastMBlock:
      # read the plaintext and pad if necessary to create block of 16 bytes
      mblock = bytearray(infile.read(16))
      if len(mblock) == 0:
         break
      mblock_padded = pkcs7(mblock)

      # xor message with previous cipher and encrypt it
      to_encrypt = xor(mblock_padded, prev_cipher)
      new_cipher = aes.encrypt(bytes(to_encrypt))
      
      # write the new cipher to the outfile
      outfile.write(new_cipher)
      prev_cipher = new_cipher
   
   infile.close()
   outfile.close()
   
      
       
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


def traverseBMPHeader(file):
   header = file.read(54)
   return header, file


def xor(x,y):
    return bytearray([a^b for a, b in zip(x, cycle(y))])


if __name__ == '__main__':
   main(argv)
