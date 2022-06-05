#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2020-2021 CJ Kucera (cj@apocalyptech.com)
# 
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the authors be held liable for any damages arising from
# the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software in a
#    product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 
# 3. This notice may not be removed or altered from any source distribution.

from Crypto.Cipher import AES
from API.inv_serial_refmanagers import Paths, get_Ref_Files
from os.path import exists
Decrypt = True #If false will encrypt, if true will decrypt

encrypted_file, base_file, key_file, outputted_file, final_file, Output, placeholderFile, placeholderOutput, InputFile, GuidFile = Paths()
###
### Decryption bit.  Thanks to Baysix for this!
###
### Basically, the encryption key for the file is stored in the final 32 bits
### of the file, but *that* key is encrypted using the first 32 bits of the
### encrypted file itself.  Just an extra little bit of obfuscation for us all.
###

# encrypted_file = 'InventorySerialNumberDatabase.encrypted.dat'
# base_file = 'InventorySerialNumberDatabase.base.dat'
# key_file = 'InventorySerialNumberDatabase.key.dat'




def decrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

def decrypt_db(data):
    """
    Returns a tuple -- the first element is the decrypted file data, and
    the second is the encryption key.
    """
    key = decrypt(data[:32], data[-32:])
    return (decrypt(key, data[:-32]).rstrip(b'\x00'), key)

def writes_decrypt_file(encrypted_file, base_file, key_file):
    with open(encrypted_file, 'rb') as df:
        with open(base_file, 'wb') as odf:
            with open(key_file, 'wb') as kdf:
                decrypted, key = decrypt_db(df.read())
                odf.write(decrypted)
                kdf.write(key)

def early_decrypt(encrypted_file, base_file, key_file, can_organize):
    if exists('Ref_Files/InventorySerialNumberDatabase.encrypted.dat') and not exists('Inter_Files/InventorySerialNumberDatabase.base.dat'):
        writes_decrypt_file(encrypted_file, base_file, key_file)
        print('Decrypted InventorySerialNumberDatabase.encrypted.dat | Run again')
        can_organize = False
        return can_organize
    elif not exists('Ref_Files/InventorySerialNumberDatabase.encrypted.dat'):
        get_Ref_Files()
        print("Ref_Files/InventorySerialNumberDatabase.encrypted.dat does not exist")
        can_organize = False
        return can_organize
    else:
        print('Base File already exists')
        can_organize = True
        return can_organize



#################################################################################

# outputted_file = 'InventorySerialNumberDatabase.out.dat'
# final_file = 'InventorySerialNumberDatabase.dat'
# key_file = 'InventorySerialNumberDatabase.key.dat'



def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    # AES uses 16-byte blocksize; pad with NULLs if needed.  This isn't
    # necessarily the best way to pad, but it's what GBX seem to be
    # doing, so that's what we're doing, too.
    if len(data) % 16 == 0:
        num_to_pad = 0
    else:
        num_to_pad = 16 - (len(data) % 16)
    return cipher.encrypt(data + b'\x00'*num_to_pad)

def encrypt_db(key, data):
    main_bit = encrypt(key, data)
    return main_bit + encrypt(main_bit[:32], key)


def writes_encrypt_file(key_file, outputted_file, final_file):
    with open(key_file, 'rb') as kdf:
        key = kdf.read()

    with open(outputted_file, 'rb') as df:
        with open(final_file, 'wb') as odf:
            odf.write(encrypt_db(key, df.read()))
            print('encrypted file written to {}'.format(final_file))


#If Decrypt false will encrypt, if true will decrypt
if Decrypt == True:
    writes_decrypt_file(encrypted_file, base_file, key_file)
else:
    writes_encrypt_file(key_file, outputted_file, final_file)