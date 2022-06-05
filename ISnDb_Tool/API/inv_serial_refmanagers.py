import requests
from os import makedirs
from os.path import exists



def Paths():
    ##Crypter
    encrypted_file = 'Ref_Files\\InventorySerialNumberDatabase.encrypted.dat'
    base_file = 'Inter_Files\\InventorySerialNumberDatabase.base.dat'
    key_file = 'Inter_Files\\InventorySerialNumberDatabase.key.dat'
    outputted_file = 'Inter_Files\\InventorySerialNumberDatabase.out.dat'
    final_file = 'Output_Files\\InventorySerialNumberDatabase.dat'

    ##Organizer
    base_file = 'Inter_Files\\InventorySerialNumberDatabase.base.dat' #File to be sorted
    Output = 'Inter_Files\\InventorySerialNumberDatabase.out.dat' #This is the file that will be written to
    placeholderFile = 'Ref_Files\\InventorySerialNumberDatabase.placeholders.dat' #placeholder file
    placeholderOutput = 'Inter_Files\\InventorySerialNumberDatabase.placeholder.out.dat' #placeholder file
    InputFile = 'Mod\\InventorySerialNumberDatabase.mod.dat' #data to be added
    GuidFile = 'Output_Files\\InventorySerialNumberDatabase.guid.dat' #file with asset guids
    return encrypted_file, base_file, key_file, outputted_file, final_file, Output, placeholderFile, placeholderOutput, InputFile, GuidFile


def get_Ref_Files():
    #Create a folder name Ref_Files if it doesnt already exist
    if not exists('Ref_Files'):
        makedirs('Ref_Files')
    #Create a folder name Output_Files if it doesnt already exist
    if not exists('Output_Files'):
        makedirs('Output_Files')
    #Create a folder name Inter_Files if it doesnt already exist
    if not exists('Inter_Files'):
        makedirs('Inter_Files')

    #download_file_from_url(https://github.com/oh-yes-0-fps/BL3-and-WL-pak-tools/blob/main/Intermediate_Resources/InventorySerialNumberDatabase.encrypted.dat?raw=true) save in subdir Ref_Files as InventorySerialNumberDatabase.encrypted.dat
    r = requests.get('https://github.com/oh-yes-0-fps/BL3-and-WL-pak-tools/blob/main/Intermediate_Resources/InventorySerialNumberDatabase.encrypted.dat?raw=true', stream=True)
    with open('Ref_Files/InventorySerialNumberDatabase.encrypted.dat', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    #download_file_from_url(https://raw.githubusercontent.com/oh-yes-0-fps/BL3-and-WL-pak-tools/main/Intermediate_Resources/InventorySerialNumberDatabase.placeholders.dat) save in subdir Ref_Files as InventorySerialNumberDatabase.placeholders.dat
    r = requests.get('https://raw.githubusercontent.com/oh-yes-0-fps/BL3-and-WL-pak-tools/main/Intermediate_Resources/InventorySerialNumberDatabase.placeholders.dat', stream=True)
    with open('Ref_Files/InventorySerialNumberDatabase.placeholders.dat', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    #creates an InventorySerialNumberDatabase.dat if it doesn't already exist
    if not exists('Output_Files/InventorySerialNumberDatabase.dat'):
        with open('Output_Files/InventorySerialNumberDatabase.dat', 'w') as f:
            f.write("Data will go here")

def Check_update(can_organize, can_decrypt, check_for_update):
    if not exists('Mod/InventorySerialNumberDatabase.mod.dat'):
        #download_file_from_url(https://raw.githubusercontent.com/oh-yes-0-fps/BL3-and-WL-pak-tools/main/Intermediate_Resources/InventorySerialNumberDatabase.mod.dat) save in subdir Ref_Files as InventorySerialNumberDatabase.encrypted.dat
        r = requests.get('https://raw.githubusercontent.com/oh-yes-0-fps/BL3-and-WL-pak-tools/main/Intermediate_Resources/InventorySerialNumberDatabase.mod.dat', stream=True)
        with open('Mod/InventorySerialNumberDatabase.mod.dat', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    #Check if the user wants to update the files
    #print(check_for_update)
    if check_for_update == 'y':
        if exists('Ref_Files/InventorySerialNumberDatabase.placeholders.dat') and exists('Ref_Files/InventorySerialNumberDatabase.encrypted.dat'):
                #download_file_from_url(https://raw.githubusercontent.com/oh-yes-0-fps/BL3-and-WL-pak-tools/main/Intermediate_Resources/InventorySerialNumberDatabase.placeholders.dat) save in subdir Ref_Files as InventorySerialNumberDatabase.placeholders.dat
            r = requests.get('https://raw.githubusercontent.com/oh-yes-0-fps/BL3-and-WL-pak-tools/main/Intermediate_Resources/InventorySerialNumberDatabase.placeholders.dat', stream=True)
            with open('Ref_Files/InventorySerialNumberDatabase.newplaceholders.dat', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            #compare Ref_Files/InventorySerialNumberDatabase.newplaceholders.dat and Ref_Files/InventorySerialNumberDatabase.placeholders.dat
            #if they are different, then update the Ref_Files/InventorySerialNumberDatabase.placeholders.dat
            with open('Ref_Files/InventorySerialNumberDatabase.newplaceholders.dat', 'r') as f:
                with open('Ref_Files/InventorySerialNumberDatabase.placeholders.dat', 'r') as f2:
                    if f.read() != f2.read():
                        with open('Ref_Files/InventorySerialNumberDatabase.placeholders.dat', 'w') as f3:
                            f3.write(f.read())
                        can_organize = False
                        can_decrypt = False
                        print("Placeholder file has been updated to latest patch")
                        return can_organize, can_decrypt
                    else:
                        print("Placeholder file is up to date")
                        can_organize = True
                        can_decrypt = True
                        return can_organize, can_decrypt
        else:
            get_Ref_Files()
            print('Ref_Files downloaded\nRun again')
            can_organize = False
            can_decrypt = False
            return can_organize, can_decrypt
    else:
        can_organize = True
        can_decrypt = True
        return can_organize, can_decrypt









