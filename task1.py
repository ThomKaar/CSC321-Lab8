# Written by His grace

from Crypto.Cipher import AES
from sys import argv
from Crypto import Random


def main(argv):
   # ecb_encrypt(argv[1], argv[2])
   cbc_encrypt(argv[1], argv[2])
 

def ecb_encrypt(inFileName, outFileName):
   # open the file
   file = open(inFileName, "r")
   outFile = open(outFileName, "wb")
   # Create the AES obj
   randomGen = Random.new()
   obj = AES.new("0123456789123456")
   
   while(True):
      message = file.read(16)
      if( message == ''):
         print("We've broken")
         break   
      elif len(message) != 16:
         print("We need to pad")
         while(len(message) != 16):
            message += "0"
      obj = AES.new(randomGen.read(16))
      ciphertext = obj.encrypt(message)
      outFile.write(ciphertext)
   return


def cbc_encrypt(inFileName, outFileName):
   
   key = Random.get_random_bytes(16) 
   aes = AES.new(key)
   iv = Random.get_random_bytes(16)

   infile = open(inFileName, 'r')
   outfile = open(outFileName, 'w')
   
   lastMBlock = False
   
   # read the plaintext and pad if necessary to create block of 16 bytes
   mblock0 = infile.read(16)
   
   if len(mblock0) < 16:
      mblock0_padded = pkcs7(mblock0)
      lastMBlock = True
   else:
      mblock0_padded = mblock0
   
   # xor message with IV and encrypt it
   to_encrypt0 = iv ^ mblock0_padded
   cipher0 = aes.encrypt(to_encrypt0)
   outfile.write(cipher0)
   
   prev_cipher = cipher0
   while not lastMBlock:
      # read the plaintext and pad if necessary to create block of 16 bytes
      mblock = infile.read(16)
      if mblock == '':
         break
      mblock_padded = pkcs7(mblock)

      # xor message with previous cipher and encrypt it
      to_encrypt = prev_cipher ^ mblock_padded
      new_cipher = aes.encrypt(to_encrypt)
      
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
      pad_str += pad_utf8
   return plaintext + pad_str

if __name__ == '__main__':
   main(argv)
