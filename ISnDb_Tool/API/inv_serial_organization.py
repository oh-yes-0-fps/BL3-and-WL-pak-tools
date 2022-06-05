#sorts out inv serial entries and versions for you
#
#


#get data from github url to use in the script

FileToSort = 'InventorySerialNumberDatabase.base.dat'
Output = 'InventorySerialNumberDatabase.out.dat'
InputFile = 'InventorySerialNumberDatabase.mod.dat' #data to be added
GuidFile = 'InventorySerialNumberDatabase.guid.dat' #file with asset guids
debug = 'debug.txt'



def ISNDBparse(basefile,filetoadd):
    #getall the lines from the file
    with open(basefile, 'r') as f:
        lines = f.readlines()
    #remove the first two lines
    lines = lines[2:]
    #remove \t and \n from each line
    lines = [line.strip() for line in lines]
    #print(lines)

    #find if list entry has "Version" in it
    #if it does, then it is a version entry
    #if it doesn't, then it is a asset entry
    EntryType = []
    for line in lines:
        if 'Version' in line:
            EntryType.append('Version')
        elif 'Asset' in line:
            EntryType.append('Asset')
        else:
            EntryType.append('Class')
    #print(EntryType)

    #if it is a version entry get the first number in the line
    #and add it to a list
    versionList = []
    for i in range(len(lines)):
        if EntryType[i] == 'Version':
            versionList.append(lines[i][8:10])
    #remove commas from the list
    versionList = [x.replace(',', '') for x in versionList]
    #get the unique values from the list
    versionList = list(set(versionList))
    #convert the list to ints
    versionList = [int(x) for x in versionList]
    #get the length of the list
    #print(versionList)
    #Get classes from the file
    classList = []
    for i in range(len(lines)):
        if EntryType[i] == 'Class':
            classList.append(lines[i])
    #get number of classes
    #print(classList)

    #get lines number for each class
    classLines = []
    for i in range(len(classList)):
        classLines.append(lines.index(classList[i]))
    classLines.append(len(lines))
    #print(classLines)

    #get asset entries for each class
    classAssets = []
    for i in range(len(classLines)-1):
        classAssets.append(lines[classLines[i]+1:classLines[i+1]])
    #get number of lists in classAssets
    #print(classAssets)

    #
    ### Second file
    #

    #get the lines from the file to add
    with open(filetoadd, 'r') as f:
        lines2 = f.readlines()
    #remove the first two lines
    lines2 = lines2[2:]
    #remove \t and \n from each line
    lines2 = [line.strip() for line in lines2]
    #print(lines2)
    
    #find if list entry has "Version" in it
    #if it does, then it is a version entry
    #if it doesn't, then it is a asset entry
    EntryType2 = []
    for line in lines2:
        if 'Version' in line:
            EntryType2.append('Version')
        elif 'Asset' in line:
            EntryType2.append('Asset')
        else:
            EntryType2.append('Class')
    #print(EntryType2)


    #Get classes from the file
    classList2 = []
    for i in range(len(lines2)):
        if EntryType2[i] == 'Class':
            classList2.append(lines2[i])
    #get number of classes
    #print(classList2)

    #get lines number for each class
    classLines2 = []
    for i in range(len(classList2)):
        classLines2.append(lines2.index(classList2[i]))
    classLines2.append(len(lines2))

    #get asset entries for each class
    classAssets2 = []
    for i in range(len(classLines2)-1):
        classAssets2.append(lines2[classLines2[i]+1:classLines2[i+1]])
    #get number of lists in classAssets
    #print(classAssets2)

    #
    ##Binds entries to lists
    #

    #merges classAssets and classAssets2
    classAssetsMerged = []
    for i in range(len(classAssets)):
        classAssetsMerged.append(classAssets[i] + classAssets2[i])

    #isolate asset entries
    classAssetsCleanA = []
    for i in range(len(classAssetsMerged)):
        classAssetsCleanA.append([x for x in classAssetsMerged[i] if 'Version' not in x])
    # for i in range(len(classAssets2)):
    #     classAssetsCleanA.append([x for x in classAssets2[i] if 'Version' not in x])
    #print(classAssetsCleanA)

    #isolate version entries
    classAssetsCleanV = []
    for i in range(len(classAssets)):
        classAssetsCleanV.append([x for x in classAssets[i] if 'Asset' not in x])

    return(classAssetsCleanA,classAssetsCleanV,classList,versionList)









#writes 32 digits after Asset= in classAssetsCleanA in a new list
def ISNDBguids(AssetList, guidfile):
    #create a new list
    AssetGuids = [] 
    #for each list in AssetList
    for i in range(len(AssetList)):
        #for each line in the list
        for j in range(len(AssetList[i])):
            #if the line has "Asset=" in it
            if 'Asset=' in AssetList[i][j]:
                #get the number after "Asset="
                #and add it to a new list
                AssetGuids.append(AssetList[i][j][6:38])
    #print(AssetGuids)
    #get the length of the list
    AssetGuidsLength = len(AssetGuids)
    #get the unique values from the list
    AssetGuidsOld = AssetGuids
    AssetGuids = list(set(AssetGuids))
    #get the length of the list
    AssetGuidsUniqueLength = len(AssetGuids)
    #print lengths
    #print(AssetGuidsLength)
    #print(AssetGuidsUniqueLength)
    if AssetGuidsLength == AssetGuidsUniqueLength:
        with open(guidfile, 'w') as f:
            for i in range(len(AssetGuids)):
                f.write(AssetGuids[i] + '\n')
        return('AssetGuids written to file')
    else:
        print('duplicate guids')
        #get any entries that occur more than once in assetguidsold
        #and add them to a new list
        AssetGuidsDuplicates = []
        for i in range(len(AssetGuidsOld)):
            if AssetGuidsOld.count(AssetGuidsOld[i]) > 1:
                AssetGuidsDuplicates.append(AssetGuidsOld[i])
        print(AssetGuidsDuplicates)
        with open(GuidFile, 'w') as f:
            f.write('Error')
        return('Error')






def Versioning(classAssetsCleanA,classAssetsCleanV,classList,versionList):
    #get final number of each class in classAssetsCleanV
    #and add it to a list
    LatestVersionValues = []
    for i in range(len(classAssetsCleanV)):
        LatestVersionValues.append([x[-2:] for x in classAssetsCleanV[i]])
    LatestVersionValues = [x[-1] for x in LatestVersionValues]
    LatestVersionValues = [x.replace(',', '') for x in LatestVersionValues]
    #changes list to int
    LatestVersionValues = [int(x) for x in LatestVersionValues]
    #print(LatestVersionValues)

    #get number of items in each class
    classItems = []
    for i in range(len(classAssetsCleanA)):
        classItems.append(len(classAssetsCleanA[i]))
    #print(classItems)

    #is value is power of 2
    def isPowerOfTwo(n):
        return (n != 0) and ((n & (n - 1)) == 0)
    #if the value in classitems is greater than the value in 2^LatestVersionValues
    #then see what the closes power of 2 is to the value in classitems thats greater than the value in classitems
    #and use that as the value for classitems
    ClassVersionSize = []
    for i in range(len(classItems)):
        if classItems[i] < 2**int(LatestVersionValues[i]):
                ClassVersionSize.append(LatestVersionValues[i])
        elif 2**(int(LatestVersionValues[i])+1) > classItems[i] > 2**(int(LatestVersionValues[i])):
                ClassVersionSize.append(int(LatestVersionValues[i])+1)
        elif 2**(int(LatestVersionValues[i])+2) > classItems[i] > 2**(int(LatestVersionValues[i])+1):
                ClassVersionSize.append(int(LatestVersionValues[i])+2)
        elif 2**(int(LatestVersionValues[i])+3) > classItems[i] > 2**(int(LatestVersionValues[i])+2):
                ClassVersionSize.append(int(LatestVersionValues[i])+3)
        elif 2**(int(LatestVersionValues[i])+4) > classItems[i] > 2**(int(LatestVersionValues[i])+3):
                ClassVersionSize.append(int(LatestVersionValues[i]+4))
        elif 2**(int(LatestVersionValues[i])+5) > classItems[i] > 2**(int(LatestVersionValues[i])+4):
                ClassVersionSize.append(int(LatestVersionValues[i]+5))
        elif isPowerOfTwo(classItems[i]):
                ClassVersionSize.append(int(LatestVersionValues[i])+1)
        else :
            ClassVersionSize.append('Error')
    #get the length of the list
    ClassVersionSizeLength = len(ClassVersionSize)
    #print(ClassVersionSizeLength)
    #print(ClassVersionSize)

    #makes list for determining which values were changed
    VersionsCompared = []
    for i in range(len(LatestVersionValues)):
        if ClassVersionSize[i] == LatestVersionValues[i]:
            VersionsCompared.append(0)
        else:
            VersionsCompared.append(1)
    #print(VersionsCompared)

    #print(LatestVersionValues)
    #print(ClassVersionSize)
    #print(classList)

    #create a version entry for each class
    #and add it to a list
    VersionEntries = []
    versionList.sort()
    versionList.append(versionList[-1]+1)
    #print(versionList)
    for i1 in range(len(VersionsCompared)):
        if VersionsCompared[i1] == 1:
            versionListLast = versionList[-1]
            versionListLast = str(versionListLast)
            CVStmp = str(ClassVersionSize[i1])
            VersionEntries.append('Version=' + versionListLast + ',' + CVStmp)
            versionListLast = str(versionListLast)
            versionListLastPlus1 = int(versionListLast) + 1
            versionListLastPlus1 = str(versionListLastPlus1)
            versionList.append(versionListLastPlus1)
        else:
            VersionEntries.append('')
    #put version entries in a list in a list
    VersionEntriesList = []
    for i in range(len(classList)):
        VersionEntriesList.append([VersionEntries[i]])
    #append versionentrieslist to classAssetsCleanv if not empty(still outputs empty somehow?)
    for i in range(len(classAssetsCleanV)):
        blanktmp = ['']
        if classAssetsCleanV[i] != blanktmp:
            classAssetsCleanV[i].append(VersionEntries[i])
    classAssetsCleanV = [x for x in classAssetsCleanV if x != ['']]
    #print(classAssetsCleanV)
    #print(VersionEntries)
    #print(classList)
    #print(VersionEntriesList)
    return(classAssetsCleanV)

def ISNDB_Final_Write(Output, classList, classAssetsCleanA, classAssetsCleanV):
    #write class list and subclassoutput to output file
    f = open(Output, 'w')
    f.write('InvSnDb\nFileVersion=1\n')
    for i in range(len(classList)):
        f.write(classList[i])
        f.write('\n')
        for j in range(len(classAssetsCleanV[i])):
            f.write('\t')
            f.write(str(classAssetsCleanV[i][j]))
            f.write('\n')
        for j in range(len(classAssetsCleanA[i])):
            f.write('\t')
            f.write(str(classAssetsCleanA[i][j]))
            f.write('\n')
    f.close()

    #Removes tab lines from file
    with open(Output, 'r') as f:
        lines = f.readlines()
        with open(Output, 'w') as f:
            for line in lines:
                if line.strip():
                    f.write(line)

#
##Runs the functions
#

# classAssetsCleanA,classAssetsCleanV,classList,versionList = ISNDBparse(FileToSort,InputFile)

# classAssetsCleanV = Versioning(classAssetsCleanA,classAssetsCleanV,classList,versionList)

# ISNDB_Final_Write(Output, classList, classAssetsCleanA, classAssetsCleanV)

# ISNDBguids(classAssetsCleanA, GuidFile)



