#runs a series of commands to unpacke the files, convert them to json and then delete unwanted files
from os import getcwd, listdir, makedirs, remove, system
from os.path import exists

def open_pak(pak_list, paks_to_open, exe_path,folder_to_export):
    cryptokeys = 'Crypto.json'
    cwd = getcwd()
    #create a folder to export to
    if not exists(cwd + folder_to_export):
        makedirs(cwd + folder_to_export)
    folder_to_export = cwd + folder_to_export
    cryptokeys = cwd + '\\' + cryptokeys
    print(cryptokeys)
    for i in pak_list:
        system(exe_path + ' "' +paks_to_open + '\\' + i + '" -Extract "' + folder_to_export + '" -cryptokeys=' + cryptokeys + ' -extracttomountpoint')# + ' -extracttomountpoint'
        print(exe_path + ' "' +paks_to_open + '\\' + i + '" -Extract "' + folder_to_export + '" -cryptokeys=' + cryptokeys + ' -extracttomountpoint')#

def wl_pak_dict(pakType_ID):
    GameplayData = ['pakchunk0-WindowsNoEditor']
    MaterialsTextuersParticleSystemsMehses = ['pakchunk1-WindowsNoEditor','pakchunk6-WindowsNoEditor','pakchunk19-WindowsNoEditor']
    Dungeon = ['pakchunk15-WindowsNoEditor','pakchunk16-WindowsNoEditor','pakchunk17-WindowsNoEditor','pakchunk18-WindowsNoEditor','pakchunk44-WindowsNoEditor','pakchunk45-WindowsNoEditor','pakchunk46-WindowsNoEditor','pakchunk47-WindowsNoEditor']
    SoundEffects  = ['pakchunk2-WindowsNoEditor']
    Dialogue_English = ['pakchunk3-WindowsNoEditor']
    Dialogue_French = ['pakchunk48-WindowsNoEditor']
    Dialogue_German = ['pakchunk49-WindowsNoEditor']
    Dialogue_Spanish = ['pakchunk50-WindowsNoEditor']
    Dialogue_Japanese = ['pakchunk51-WindowsNoEditor']
    Dialogue_Korean = ['pakchunk52-WindowsNoEditor']
    Dialogue_Chinese = ['pakchunk53-WindowsNoEditor']
    Menu_P = ['pakchunk4-WindowsNoEditor','pakchunk5-WindowsNoEditor']
    Tutorial_P = ['pakchunk7-WindowsNoEditor','pakchunk8-WindowsNoEditor']
    Intro_P = ['pakchunk9-WindowsNoEditor','pakchunk10-WindowsNoEditor']
    Graveyard_P = ['pakchunk11-WindowsNoEditor','pakchunk12-WindowsNoEditor']
    Hubtown_P = ['pakchunk13-WindowsNoEditor','pakchunk14-WindowsNoEditor']
    Goblin_P = ['pakchunk20-WindowsNoEditor','pakchunk21-WindowsNoEditor']
    Mushroom_P = ['pakchunk22-WindowsNoEditor','pakchunk22-WindowsNoEditor']
    Abyss_P = ['pakchunk24-WindowsNoEditor','pakchunk25-WindowsNoEditor']
    AbyssBoss_P = ['pakchunk26-WindowsNoEditor','pakchunk27-WindowsNoEditor']
    Beanstalk_P = ['pakchunk28-WindowsNoEditor','pakchunk29-WindowsNoEditor']
    Climb_P = ['pakchunk30-WindowsNoEditor','pakchunk31-WindowsNoEditor']
    Pirate_P = ['pakchunk32-WindowsNoEditor','pakchunk33-WindowsNoEditor']
    Seabed_P = ['pakchunk34-WindowsNoEditor','pakchunk35-WindowsNoEditor']
    Oasis_P = ['pakchunk36-WindowsNoEditor','pakchunk37-WindowsNoEditor']
    Pyramid_P = ['pakchunk38-WindowsNoEditor','pakchunk39-WindowsNoEditor']
    PyramidBoss_P = ['pakchunk40-WindowsNoEditor','pakchunk41-WindowsNoEditor']
    Sands_P = ['pakchunk42-WindowsNoEditor','pakchunk43-WindowsNoEditor']
    Overworld_P = ['pakchunk15-WindowsNoEditor','pakchunk16-WindowsNoEditor']
    #make a list of all the paks
    All = GameplayData + MaterialsTextuersParticleSystemsMehses + Dungeon + SoundEffects + Dialogue_English + Dialogue_French + Dialogue_German + Dialogue_Spanish + Dialogue_Japanese + Dialogue_Korean + Dialogue_Chinese + Menu_P + Tutorial_P + Intro_P + Graveyard_P + Hubtown_P + Goblin_P + Mushroom_P + Abyss_P + AbyssBoss_P + Beanstalk_P + Climb_P + Pirate_P + Seabed_P + Oasis_P + Pyramid_P + PyramidBoss_P + Sands_P
    #make a dictionary of all the lists
    pak_dict = {0:All, 1:GameplayData, 2:MaterialsTextuersParticleSystemsMehses, 3:Dungeon, 4:SoundEffects, 
                11:Dialogue_English, 12:Dialogue_French, 13:Dialogue_German, 14:Dialogue_Spanish, 15:Dialogue_Japanese, 16:Dialogue_Korean, 17:Dialogue_Chinese, 
                101:Menu_P, 102:Tutorial_P, 103:Intro_P, 104:Graveyard_P, 105:Hubtown_P, 106:Overworld_P, 107:Goblin_P, 108:Mushroom_P, 109:Abyss_P, 110:AbyssBoss_P, 111:Beanstalk_P, 112:Climb_P, 113:Pirate_P, 114:Seabed_P, 115:Oasis_P, 116:Pyramid_P, 117:PyramidBoss_P, 118:Sands_P}
    return pak_dict[pakType_ID]


def bl3_pak_dict(pakType_ID):
    print(f'extracting {pakType_ID}')
    print('oooopsies still a WIP')


def get_sub_paks(pak_list, paks_to_open):
    listof25 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    #Get list of files in the paks folder
    pakss = listdir(paks_to_open)
    #if entry in pakss has any of the pak_list entries in it, then add it to new list
    new_pak_list = []
    for i in pakss:
        for j in pak_list:
            if j in i:
                new_pak_list.append(i)
    print(f'extracting {new_pak_list}')
    return new_pak_list

def configerator():
    config_file = 'Unpacker.config'
    #if config file doesn't exist, create it
    if not exists(config_file):
        with open(config_file, 'w') as c:
            c.write('Persistent data for Unpacker(use single \\)\n')
            c.write('Unrealpak.exe Location\n')
            c.write('\n')
            c.write('Wonderlands paks filepath\n')
            c.write('\n')
            c.write('Borderlands 3 paks filepath\n')
            c.write('\n')
            c.write('UAssetGUI filepath\n')
            c.write('\n')
    #open the config file into a list of lines
    with open(config_file, 'r') as f:
        config_list = f.readlines()
    #print(config_list)
    if len(config_list) == 0:
        print('ERROR: Config file is empty\nDelete the config file and run the program again')
        return
    if len(config_list) < 6:
        print('ERROR: Config file is missing some lines\nDelete the config file and run the program again')
        return
    if config_list[2] == '\n':
        print('If this is your first time using this script make sure you have read the README.md file')
        print('If you have all requirments installed then continue')
        input('Press enter to continue')
        UPE = input('Enter the path to Unrealpak.exe: ')
        config_list[2] = (UPE + '\n')
        answer1 = input('Will this tool be used for Borderlands 3 paks? (y/n)')
        if answer1 == 'y':
            config_list[6] = (input('Enter the path to the Borderlands 3 paks: ') + '\n')
        answer2 = input('Will this tool be used for Wonderlands paks? (y/n)')
        if answer2 == 'y':
            config_list[4] = (input('Enter the path to the Wonderlands paks: ') + '\n')
        if answer1 == 'n' and answer2 == 'n':
            print('ERROR: You must use this tool for at least one pak')
            return
        answer = input('Will this tool be used for UAssetGUI? (y/n)')
        if answer == 'y':
            config_list[8] = (input('Enter the path to the UAssetGUI: ') + '\n')
        print('Config file has been updated')
    else:
        print('Config file has been loaded')
    #print(config_list)
    #write the list back to the config file
    with open(config_file, 'w') as f:
        for i in config_list:
            f.write(i)

def Get_cfg_data():
    config_file = 'Unpacker.config'
    #open the config file into a list of lines
    with open(config_file, 'r') as f:
        config_list = f.readlines()
    #remove the newline characters from the list
    for i in range(len(config_list)):
        config_list[i] = config_list[i].rstrip('\n')
    #Read data from config file
    Unrealpak_path = config_list[2]
    Borderlands3_path = config_list[6]
    Wonderlands_path = config_list[4]
    UAssetGUI_path = config_list[8]
    return Unrealpak_path, Borderlands3_path, Wonderlands_path, UAssetGUI_path

def get_pak_type(selected_game):
    if selected_game == 'bl3':
        print('Borderlands 3 paks are a WIP')
        return
    if selected_game == 'wl':
        return wl_type_menu1()
    if selected_game == 'close':
        exit()
    if selected_game == 'debug':
        debug_menu()
    else:
        print('ERROR: Invalid game selected')
        return get_pak_type(input('Enter the name of the game you want to unpack(wl/bl3/close): '))

def debug_menu():
    print("----------------------------------------\n"
    "debug menu\n"
    "1 : delete extracted WL paks\n"
    "2 : delete extracted BL3 paks\n"
    "3 : debug pak run\n"
    "4 : verify config file\n"
    "5 : print current directory\n"
    "6 : exit\n")
    answer = input('Enter the number of the option you want to select: ')
    cwd = getcwd()
    if answer == '1':
        print('deleting extracted WL paks')
        wl_pak_list = listdir(cwd + '\\WL_Output')
        for i in wl_pak_list:
            remove(cwd + '\\WL_Output\\' + i)
        print('WL paks deleted')
    if answer == '2':
        print('deleting extracted BL3 paks')
        bl3_pak_list = listdir(cwd + '\\BL3_Output')
        for i in bl3_pak_list:
            remove(cwd + '\\BL3_Output\\' + i)
        print('BL3 paks deleted')
    if answer == '3':
        print('debug pak run')
        selectedgame = input('Enter the name of the game you want to unpack(wl/bl3/close): ')
        print(f'Return idx is: {get_pak_type(selectedgame)}')
    if answer == '4':
        print('verifying config file')
        with open ('Unpacker.config', 'r') as f:
            config_list = f.readlines()
        if config_list[2] == '\n':
            print('ERROR: Config file is empty')
        if config_list[4] == '\n':
            print('INFO: Wonderlands paks filepath is empty')
        if config_list[6] == '\n':
            print('INFO: Borderlands 3 paks filepath is empty')
        if config_list[8] == '\n':
            print('INFO: UAssetGUI filepath is empty')
    if answer == '5':
        print(cwd)
    if answer == '6':
        exit()




def wl_type_menu2():
    offset = 10
    print("----------------------------------------\n"
    "1 : Dialogue_English\n"
    "2 : Dialogue_French\n"
    "3 : Dialogue_German\n"
    "4 : Dialogue_Spanish\n"
    "5 : Dialogue_Japanese\n"
    "6 : Dialogue_Korean\n"
    "7 : Dialogue_Chinese\n"
    "back ::" )
    answer = input('Enter the language(whats before the :): ')
    if answer.isdigit() and answer >= '0' and answer <= '8':
        return (int(answer) + offset)
    elif answer == 'back':
        return wl_type_menu1()
    else:
        print('Invalid input')
        return wl_type_menu2()

def wl_type_menu3():
    offset = 100
    print("-----------------------------------------\n"
    "1 : Menu_P\n"
    "2 : Tutorial_P\n"
    "3 : Intro_P\n"
    "4 : Graveyard_P\n"
    "5 : Hubtown_P\n"
    "6 : Overworld_P\n"
    "7 : Goblin_P\n"
    "8 : Mushroom_P\n"
    "9 : Abyss_P\n"
    "10 : AbyssBoss_P\n"
    "11 : Beanstalk_P\n"
    "12 : Climb_P\n"
    "13 : Pirate_P\n"
    "14 : Seabed_P\n"
    "15 : Oasis_P\n"
    "16 : Pyramid_P\n"
    "17 : PyramidBoss_P\n"
    "18 : Sands_P\n"
    "back ::")
    answer = input('Enter the level(whats before the :): ')
    if answer.isdigit() and int(answer) > 0 and int(answer) < 19:
        return (int(answer) + offset)
    elif answer == 'back':
        return wl_type_menu1()
    else:
        print('Invalid input')
        return wl_type_menu3()

def wl_type_menu1():
    print("-----------------------------------------\n"
    "0 : All\n"
    "1 : GameplayData\n"
    "2 : Materials/Textuers/ParticleSystems/Mehses\n"
    "3 : Dungeon\n"
    "4 : SoundEffects\n"
    "dialog : Open Dialog Page\n"
    "maps : Open Maps Page\n"
    "back ::")
    answer = input('Enter the pak type(whats before the :): ')
    if answer.isdigit() and answer >= '0' and answer <= '19':
        return int(answer)
    elif answer == 'dialog':
        return wl_type_menu2()
    elif answer == 'maps' or answer == 'map':
        return wl_type_menu3()
    elif answer == 'back':
        selected_game = input('Enter the name of the game you want to unpack(wl/bl3/close): ')
        return get_pak_type(selected_game)
    else:
        print('Invalid input')
        return wl_type_menu1()







def main():
    print('starting')
    configerator()
    Unrealpak_path, Borderlands3_path, Wonderlands_path, UAssetGUI_path = Get_cfg_data()
    selected_game = input('Enter the name of the game you want to unpack(wl/bl3/close): ')
    if selected_game == 'wl' or selected_game == 'wonderlands':
        folder_to_export = '\\WL_Output'
        paks_to_open = Wonderlands_path
        dict_idx = get_pak_type(selected_game)
        pak_list = get_sub_paks(wl_pak_dict(dict_idx),Wonderlands_path)
        print(pak_list)
    elif selected_game == 'bl3' or selected_game == 'borderlands3':
        folder_to_export = '\\BL3_Output'
        paks_to_open = Borderlands3_path
        dict_idx = get_pak_type(selected_game)
        pak_list = get_sub_paks(bl3_pak_dict(dict_idx),Borderlands3_path)
    elif selected_game == 'debug':
        get_pak_type(selected_game)
    elif selected_game == 'close':
        exit()
    else:
        print('ERROR: Invalid game name')
        return
    if selected_game != 'debug':
        print(paks_to_open)
        open_pak(pak_list,paks_to_open,Unrealpak_path,folder_to_export)
    else:
        selected_game = 'debug'
        get_pak_type(selected_game)















if __name__ == '__main__':
    main()