#Version 1.0.0
#!/usr/bin/env python3
from time import sleep
from os.path import exists
from os import makedirs, remove
from API.inv_serial_refmanagers import Check_update, Paths
from API.inv_serial_organization import ISNDBparse, Versioning, ISNDB_Final_Write, ISNDBguids

#create folder named mod if it doesnt already exist
if not exists('mod'):
    makedirs('mod')
if not exists('Ref_Files'):
    makedirs('Ref_Files')
if not exists('Inter_Files'):
    makedirs('Inter_Files')
if not exists('Output_Files'):
    makedirs('Output_Files')

encrypted_file, base_file, key_file, outputted_file, final_file, Output, placeholderFile, placeholderOutput, InputFile, GuidFile = Paths()

UsePlaceholders = True #If true, will use placeholder file

make_encrypted_out = True #If true, will make encrypted output file

if not exists('Ref_Files/InventorySerialNumberDatabase.placeholders.dat') or not exists('Ref_Files/InventorySerialNumberDatabase.encrypted.dat'):
    check_for_update = 'y'
else:
    check_for_update = input('Check for update? (y/n) ')
can_organize = True #If true, will organize the file
can_decrypt = False #If true, will decrypt the file

#Does alot of the work
can_organize, can_decrypt = Check_update(can_organize, can_decrypt, check_for_update)
#print('Checked for updates')
#Decrypt the file
from API.inv_serial_crypter import writes_encrypt_file, early_decrypt
#early_decrypt(encrypted_file, base_file, key_file, can_organize)
if can_decrypt == True and not exists(base_file):
    early_decrypt(encrypted_file, base_file, key_file, can_organize)
if can_organize == True and check_for_update == 'n':
    print('loading.')
    sleep(0.3)
    print('loading..')
    sleep(0.3)
    print('loading...')
    sleep(0.3)

if can_organize == True:
    # if base file exists, then print "found file"
    if exists(base_file) and exists(placeholderFile):
        print('Found file')
        print('starting to sort')
    #Organize the file
    if UsePlaceholders == True and exists(placeholderFile) and exists(base_file):
        classAssetsCleanA,classAssetsCleanV,classList,versionList = ISNDBparse(base_file, placeholderFile)

        classAssetsCleanV = Versioning(classAssetsCleanA,classAssetsCleanV,classList,versionList)

        ISNDB_Final_Write(placeholderOutput, classList, classAssetsCleanA, classAssetsCleanV)

        print('added placeholder data')
        classAssetsCleanA,classAssetsCleanV,classList,versionList = ISNDBparse(placeholderOutput, InputFile)

        classAssetsCleanV = Versioning(classAssetsCleanA,classAssetsCleanV,classList,versionList)

        ISNDB_Final_Write(Output, classList, classAssetsCleanA, classAssetsCleanV)
        print('added mod data')
        ISNDBguids(classAssetsCleanA, GuidFile)
        print('wrote guid file')
    elif exists(base_file) and exists(InputFile) and UsePlaceholders == False:
        classAssetsCleanA,classAssetsCleanV,classList,versionList = ISNDBparse(base_file, InputFile)
        print('Extracted data from base file')
        classAssetsCleanV = Versioning(classAssetsCleanA,classAssetsCleanV,classList,versionList)
        print('version data generated')
        ISNDB_Final_Write(Output, classList, classAssetsCleanA, classAssetsCleanV)
        print('added mod data')
        ISNDBguids(classAssetsCleanA, GuidFile)
        print('wrote guid file')
    else:
        print('Run again to complete')
if make_encrypted_out == True and exists(outputted_file):
    writes_encrypt_file(key_file, outputted_file, final_file)
    print('encrypted file')
if exists('Ref_Files/InventorySerialNumberDatabase.newplaceholders.dat'):
    remove('Ref_Files/InventorySerialNumberDatabase.newplaceholders.dat')