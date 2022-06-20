
from os import walk, remove
from os.path import exists, dirname
from zipfile import ZipFile
import requests

# Put the latest asset registry file in the same directory as this script with a .base extension
# Tell it the address to the pak you want to get the asset list for for in DirToLookin
# you can also put the pak folder in the same directory as this script and just put the name of the pak folder in dirToLookin
# 
# Should_append_to_new_line is a boolean that tells the script if it should append to the file where it ends or start a new line
#
# will output a text file with the following format: assetpaths   assetnames   assetentries
# 
# 


def AR_grep(file_to_grep):
    file_to_write = file_to_grep.split('_')[0] + '_' + 'blacklist.txt'
    purged_data = ''
    #if file_to_write exists, read lines
    if exists(file_to_write):
        purged_data = []
        with open(file_to_write, 'r') as f:
            lines = f.readlines()
            for line in lines:
                purged_data.append(line.strip())
    else:
        print('blacklist file not found')
        print('creating blacklist file, this could take a bit')
        #open file to grep as bytes, write all ascii characters to debug file
        with open(file_to_grep, 'rb') as r:
            for line in r:
                for char in line:
                    if char in range(32, 127):
                        #turn char into ascii character
                        char = chr(char)
                        #add char to string
                        purged_data += char
                    else:
                        purged_data += ';'
        # split string into list of strings
        purged_data = purged_data.split(';')
        # remove empty strings
        purged_data = [x for x in purged_data if x]
        # remove duplicates
        purged_data = list(set(purged_data))

        #if entry less than 5 characters, remove from list
        purged_data = [x for x in purged_data if len(x) > 4]
        #if entry has + or { or } or [ or ] or ^ or ~ or = or # or @ or $ or $ or & or ( or ), remove from list
        purged_data = [x for x in purged_data if not (x.find('+') > -1 or x.find('{') > -1 or x.find('}') > -1 or x.find('[') > -1 or x.find(']') > -1 or x.find('^') > -1 or x.find('~') > -1 or x.find('=') > -1 or x.find('#') > -1 or x.find('@') > -1 or x.find('$') > -1 or x.find('%') > -1 or x.find('&') > -1 or x.find('(') > -1 or x.find(')') > -1 or x.find('!') > -1 or x.find('=') > -1 or x.find(',') > -1) or x.find(';') > -1 or x.find('\"') > -1 or x.find(':') > -1]

        file_to_write = file_to_grep.split('_')[0] + '_' + 'blacklist.txt'
        with open(file_to_write, 'w') as w:
            for i in range(len(purged_data)):
                w.write(purged_data[i] + '\n')
            print(f'wrote blacklist to {file_to_write}')

    return purged_data

def extract_asset_data(DirToLookIn, DataToAdd, File_Extension, UseSubDir, subDir):
    if not exists(DataToAdd):
        print('Created ModsRegistry.txt')
        with open(DataToAdd, 'x') as w:
            w.close()
    #gets path to all files in directory with .uasset extension
    def get_files(dir):
        files = []
        for path, subdirs, file_names in walk(dir):
            for name in file_names:
                if name.endswith(File_Extension):
                    files.append(path + "\\" + name)
        return files
    #concatenates directory and subdirectory
    def get_dir(dir, subdir):
        return dir + subdir
    #uses get_file_paths to get all file paths in a folder
    if UseSubDir == True:
        file_paths = get_files(get_dir(DirToLookIn, subDir))
    else:
        file_paths = get_files(DirToLookIn)
    #converts to relative game path
    for i in range(len(file_paths)):
        file_paths[i] = file_paths[i].replace((DirToLookIn + '\\OakGame\\Content'), "/Game") 
    #replaces all \\ with /
    for i in range(len(file_paths)):
        file_paths[i] = file_paths[i].replace("\\", "/")
    #removes .uasset
    for i in range(len(file_paths)):
        file_paths[i] = file_paths[i].replace(File_Extension, "")
    #gets name to all files in directory with .uasset extension
    def get_names(dir):
        files = []
        for path, subdirs, file_names in walk(dir):
            for name in file_names:
                if name.endswith(File_Extension):
                    files.append(name)
        return files
    #uses get_file_paths to get all file paths in a folder
    file_names = get_names(DirToLookIn)
    #removes .uasset
    for i in range(len(file_names)):
        file_names[i] = file_names[i].replace(File_Extension, "")
    #combines entries of file paths and names
    file_entries = []
    for i in range(len(file_paths)):
        file_entries.append(file_paths[i] + "." + file_names[i])
    return file_entries, file_paths, file_names






#writes file entries, file paths, and file names to a text file
def Writes_to_ModsRegistry(file_entries, file_paths, file_names, Should_append_to_new_line, DataToAdd):
    #if Should_append_to_new_line is true, pramble = '\n' else pramble = ''
    if Should_append_to_new_line:
        pramble = '\n'
        print('started new line')
    else:
        pramble = ''
        print('appended to end of file')
    with open(DataToAdd, 'w') as rr:
        rr.write(pramble)
        rr.write("   ")
        for i in range(len(file_entries)):
            rr.write(file_entries[i])
            rr.write("   ")
            rr.write(file_paths[i])
            rr.write("   ")
            rr.write(file_names[i])
            rr.write("   ")
        rr.close()
        print('wrote to ModsRegistry.txt')


# print(file_paths)
# print(file_names)
# print(file_entries)

def Appends_to_new_Registry(AssetRegistryToAppend, FileToOutput, DataToAdd):
    #opens asset registry to append to and writes to filetooutput
    with open(AssetRegistryToAppend, 'rb') as r:
        with open(FileToOutput, 'wb') as w:
            w.write(r.read())
            r.close()
            w.close()
    #opens file to output and appends data to it
    with open(FileToOutput, 'ab') as w:
        with open(DataToAdd, 'rb') as r:
            w.write(r.read())
            r.close()
            w.close()


#Updates registries
def Update_func(zip_name):
    print('Downloading asset registry zip')
    r = requests.get('https://github.com/oh-yes-0-fps/BL3-and-WL-pak-tools/blob/main/AssetRegistries/AssetRegistries.zip?raw=true', stream=True)
    with open(zip_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print('Downloaded asset registry zip')
    print('unzipping ' + zip_name)
    with ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(dirname(zip_name))
    print('unzipped ' + zip_name)
    if exists(zip_name):
        remove(zip_name)
        print('removed ' + zip_name)

def filter_dupes(file_entries, file_paths, file_names, blacklist, extra):
    #If entry in file_entries is in blacklist, remove it from file_entries
    iter_num = 0
    if extra == True:
        num_wanted = 150
    else:
        num_wanted = 50
    while iter_num < num_wanted:
        for i in file_entries:
            if i in blacklist:
                file_entries.remove(i)
        for i in file_paths:
            if i in blacklist:
                file_paths.remove(i)
        for i in file_names:
            if i in blacklist:
                file_names.remove(i)
        iter_num += 1
    return file_entries, file_paths, file_names

import argparse
def main():
    DataToAdd = 'ModsRegistry.txt'
    subDir = ''
    zip_name = 'AssetRegistries.zip'
    extra = False
    parser = argparse.ArgumentParser(description='Appends data to an asset registry file')
    action = parser.add_mutually_exclusive_group()
    action2 = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-d', '--dir', action='store', help='Change directory to look in(Required)', required=True)
    parser.add_argument('-s', '--subdir', action='store', help='Use subdirectory')
    parser.add_argument('-o', '--output', action='store', help='Change output file name(default: AssetRegistry.bin)')
    parser.add_argument('-a', '--append', action='store_true', help='Append to end of file or start a new line')
    parser.add_argument('-e', '--extension', action='store', help='Change extension(.uasset is default)')
    parser.add_argument('-r', '--reiterate', action='store_true', help='use this if some blacklisted files slip through')
    action.add_argument('-u', '--update', action='store_true', help='updates the asset registries')
    action2.add_argument('-b', '--bl3', action='store_true', help='adds to latest bl3 registry(Required)')
    action2.add_argument('-w', '--wl', action='store_true', help='adds to latest wl registry(Required)')
    args = parser.parse_args()
    if args.subdir:
        UseSubDir = True
        subDir = args.subdir
    else:
        UseSubDir = False
    if args.output:
        FileToOutput = args.output
    else:
        FileToOutput = 'AssetRegistry.bin'
    if args.append:
        Should_append_to_new_line = True
    else:
        Should_append_to_new_line = False
    if args.dir:
        DirToLookIn = args.dir
    else:
        print('No directory specified')
        exit()
    if args.extension:
        File_Extension = args.extension
    else:
        File_Extension = '.uasset'
    if args.update:
        Update_func(zip_name)
    if args.bl3:
        AssetRegistryToAppend = 'AssetRegistries\\BL3_AssetRegistry.base.bin'
    if args.wl:
        AssetRegistryToAppend = 'AssetRegistries\\WL_AssetRegistry.base.bin'
    if args.reiterate:
        extra = True
    if not exists(AssetRegistryToAppend):
        print('AssetRegistry base does not exist')
        todownload = input('would you like to download the asset registries? (y/n)')
        if todownload == 'y':
            Update_func(zip_name)
        else:
            print('exiting')
            exit()
    
    file_entries, file_paths, file_names = extract_asset_data(DirToLookIn, DataToAdd, File_Extension, UseSubDir, subDir)
    blacklist = AR_grep(AssetRegistryToAppend)
    file_entries, file_paths, file_names = filter_dupes(file_entries, file_paths, file_names, blacklist, extra)
    Writes_to_ModsRegistry(file_entries, file_paths, file_names, Should_append_to_new_line, DataToAdd)
    Appends_to_new_Registry(AssetRegistryToAppend, FileToOutput, DataToAdd)


if __name__ == '__main__':
    main()

if exists('AssetRegistry.bin'):
    print("Asset Registry Made")

