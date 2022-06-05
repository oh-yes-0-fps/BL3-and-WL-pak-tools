
from os.path import exists
import random
from os import listdir

GuidsFile = 'Output_Files\\InventorySerialNumberDatabase.guid.dat' #the guids file to append to
ModsGuidsFile = 'Mod\\ModsGuids.txt' #replace mods with name of your mod

#see if mods guids file exists
if exists(ModsGuidsFile):
    print('Mods guids file found')
else:
    print('Mods guids file made')
    #write "File to store your used asset guids for your mod"
    with open(ModsGuidsFile, 'w') as w:
        w.write('File to store your used asset guids for your mod\n')





#make a random 32 character string for the asset guid containing digits 0-1 and letters a-f
def makeAssetGuid():
    assetGuid = ''
    for i in range(32):
        assetGuid += random.choice('0123456789abcdef')
    return assetGuid
gennedAssetGuid = makeAssetGuid()

#turns a guids file into a list of guids
def makeGuidsList(guidsfile,modguidsfile):
    guidsList = []
    with open(guidsfile, 'r') as r1:
        for line in r1:
            guidsList.append(line.strip())
    with open(modguidsfile, 'r') as r2:
        for line in r2:
            guidsList.append(line.strip())
    return guidsList
GuidsList = makeGuidsList(GuidsFile,ModsGuidsFile)


#if gennedAssetGuid matches any entries in GuidsList, make a new one
while gennedAssetGuid in GuidsList:
    gennedAssetGuid = makeAssetGuid()

#append gennedAssetGuid to the end of the mods guids file
with open(ModsGuidsFile, 'a') as w:
    w.write(gennedAssetGuid + '\n')
    w.close()

#prints the genned asset guid lower case and uppercase
print(gennedAssetGuid.lower())
print(gennedAssetGuid.upper())




