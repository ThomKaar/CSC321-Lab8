#Written by His grace

from Crypto.Cipher import AES
from sys import argv
from Crypto import Random


def main(argv):
   ecb_encrypt(argv[1], argv[2])
 

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


def cbc_encrypt():
   pass



if __name__ == '__main__':
   main(argv)

