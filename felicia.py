import Tkinter
from Tkinter import BOTH, END, LEFT, INSERT
from ScrolledText import *
import tkMessageBox

# Loading PyCrypto library
from Crypto.Cipher import AES
from Crypto.Cipher import ARC2
from Crypto.Cipher import ARC4
from Crypto.Cipher import Blowfish
from Crypto.Cipher import CAST
from Crypto.Cipher import DES3

# And some other stuff we need
from Crypto import Random
from struct import pack

# Global textPad width
tpwidth ='4'

# Helper module for calculating current column
curCol = '0'
curCol = int(curCol)


# Method to read the data from the text area and send it to the ef()
# method fro encryption
def encryptText():
	s = textPad.get(1.0,END)
	ef(s)
	
def getKey():
	s = keyTextField.get()
	return s

def getIV():
	s = IVTextField.get()
	return s

######### The encryption part ################	
	
def ef(s):
	key = getKey()
	iv = getIV()
	s = s

	try:
		cipherType = cipherTextField.get()
		
		# Select which cipher to use for encryption
		
		if cipherType =='AES':
			cipher = AES.new(key, AES.MODE_CFB, iv)
			e = cipher.encrypt(s)

		if cipherType =='ARC2':
			cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
			e = cipher.encrypt(s)
			
		
		# ARC4 does not make use of IV
		if cipherType =='ARC4':
			cipher = ARC4.new(key)
			e = cipher.encrypt(s)

			
		# Blowfish uses an IV of eight bytes. Blowfish is a block cipher.
		elif cipherType =='Blowfish':
			bs = Blowfish.block_size
			key = getKey()
			iv = getIV()
			cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
			
			# Since Blowfish likes its plain text in blocks of 7 we need to
			# chew the text a bit before feeding it to the cipher
			plen = bs - divmod(len(s),bs)[1]
			padding = [plen]*plen
			padding = pack('b'*plen, *padding)
			e = cipher.encrypt(s+padding)
		
		elif cipherType =='CAST':
			bs = CAST.block_size
			key = getKey()
			iv = getIV()
			cipher = CAST.new(key, CAST.MODE_OPENPGP, iv)
			e = cipher.encrypt(s)
			
		elif cipherType =='DES3':
			bs = DES3.block_size
			key = getKey()
			iv = getIV()
			cipher = DES3.new(key, DES3.MODE_OFB, iv)
			
			# Since DES3 likes its plain text in blocks of 7 we need to
			# chew the text a bit before feeding it to the cipher
			plen = bs - divmod(len(s),bs)[1]
			padding = [plen]*plen
			padding = pack('b'*plen, *padding)
			e = cipher.encrypt(s+padding)

	except ValueError as e:
		tkMessageBox.showinfo("Info", e)
		
	except TypeError as e:
		tkMessageBox.showinfo("info", e)
		
	eRes(cipherType, key, iv, s)
		
	f = open('secrets.txt', 'w+')
	f.write(e)
	f.close()

#################################################	
	
def eRes(cipherType, key, iv, s):
	cipherType = cipherType 
	key = key
	iv = iv
	s = s
	
	
	e = s+' was written to file using '+cipherType+' with key '+key+' and an initialization vector of '+iv
	
	
	textPad.insert(INSERT,e)
	textPad.grid(row=0, column=0, columnspan=tpwidth, padx=5, pady=5)	

####################### The decryption part ##############	
	
	
def ref():
	# Open secret file
	f = open('secrets.txt','r')
	s = f.readline()
	
	textPad.delete(1.0,END)
	# Setup and perform the decryption
	
	key = getKey()
	iv = getIV()
	cipherType = cipherTextField.get()
	
	try:
		if cipherType =='AES':
			cipher = AES.new(key, AES.MODE_CFB, iv)
			e = 'THE DECRYPTED CONTENT IS: '+cipher.decrypt(s)+'\n'
			
		if cipherType =='ARC2':
			cipher = ARC2.new(key, ARC2.MODE_CFB, iv)
			e = 'THE DECRYPTED CONTENT IS: '+cipher.decrypt(s)+'\n'	

		if cipherType =='ARC4':
			cipher = ARC4.new(key)
			e = 'THE DECRYPTED CONTENT IS: '+cipher.decrypt(s)+'\n'	
			
		elif cipherType =='Blowfish':
			cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
			e = 'THE DECRYPTED CONTENT IS: '+cipher.decrypt(s)+'\n'
			
		elif cipherType =='CAST':
			eiv = s[:CAST.block_size+2]
			ciphertext = s[CAST.block_size+2:]
			cipher = CAST.new(key, CAST.MODE_OPENPGP, eiv)
			e = 'THE DECRYPTED CONTENT IS: '+cipher.decrypt(ciphertext)
			
		elif cipherType =='DES3':
			cipher = DES3.new(key, DES3.MODE_OFB, iv)
			e = 'THE DECRYPTED CONTENT IS: '+cipher.decrypt(s)+'\n'
	
	except ValueError as e:
		tkMessageBox.showinfo("Info", e)
		
	except TypeError as e:
		tkMessageBox.showinfo("info", e)
	
	# Write file content to textPad
	textPad.insert(INSERT,e)
	textPad.grid(row=0, column=0, columnspan=tpwidth, padx=5, pady=5)
	
	# Close secret file
	f.close()
	
###########################################################
	
def currentCol(curCol):
		curCol = curCol+1
		return curCol
	

# Draw window main window, labels, fields and set a default value to 
# the textPad
top = Tkinter.Tk()
top.title('Felicia')
textPad = ScrolledText(top, width=60, height=20)
textPad.grid(row=0, column=0, columnspan=tpwidth, padx=5, pady=5)
textPad.insert(INSERT,'ASCII clear text')

curCol = currentCol(curCol)
IVTextFieldLabel = Tkinter.Label(top, text='IV, salt, seed, or nonce')
IVTextFieldLabel.grid(row=1, column=curCol, padx=5, pady=5)

curCol = currentCol(curCol)
IVTextField = Tkinter.Entry(top, width=30)
IVTextField.insert(0,'11111111')
IVTextField.grid(row=1, column=curCol, padx=5, pady=5)

curCol = 0

curCol = currentCol(curCol)
keyTextFieldLabel = Tkinter.Label(top, text='Encryption key')
keyTextFieldLabel.grid(row=2, column=curCol, padx=5, pady=5)

curCol = currentCol(curCol)
keyTextField = Tkinter.Entry(top, width=30)
keyTextField.insert(0,'1111111111111111')
keyTextField.grid(row=2, column=curCol, padx=5, pady=5)

curCol = 0

curCol = currentCol(curCol)
cipherTextFieldLabel = Tkinter.Label(top, text='Cipher (ARC2, ARC4, CAST, AES, Blowfish, DES3)')
cipherTextFieldLabel.grid(row=3, column=curCol, padx=5, pady=5)

curCol = currentCol(curCol)
cipherTextField = Tkinter.Entry(top, width=30)
cipherTextField.insert(0,'DES3')
cipherTextField.grid(row=3, column=curCol, padx=5, pady=5)

curCol = 0

curCol = currentCol(curCol)
b = Tkinter.Button(top, text="Read encrypted file",command = ref)
b.grid(row=4, column=curCol, padx=5, pady=5)

curCol = currentCol(curCol)
b = Tkinter.Button(top, text="Encrypt file",command = encryptText)
b.grid(row=4, column=curCol, padx=5, pady=5)



top.mainloop()
