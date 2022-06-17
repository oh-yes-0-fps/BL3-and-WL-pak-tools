import json
import csv
import re



def key_cleanse(json_data,keytokeep):
    #gtes list of all keys besides Table
    unwantedkeys = []
    keytokeep1 = keytokeep[0]
    keytokeep2 = keytokeep[1]
    keytokeep3 = keytokeep[2]
    keytokeep4 = keytokeep[3]
    for i in json_data:
        for key in i:
            if key != keytokeep1 and key != keytokeep2 and key != keytokeep3 and key != keytokeep4:
                unwantedkeys.append(key)
    unwantedkeys = list(set(unwantedkeys))
    #removes keys that are in unwantedkeys
    for i in json_data:
        for key in unwantedkeys:
            del i[key]
    return json_data


def get_type(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)['Exports']
    Type = []
    for i in data:
        Type.append(i['Table']['$type'])
    for i in range(len(Type)):
        Type[i] = Type[i].replace('UAssetAPI.', '')
        Type[i] = Type[i].replace(', UAssetAPI', '')
        Type = Type[i]
        print(f'File type is {Type}')
        return Type

def import_mapper(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)['Imports']
    #remove keys $type and ClassPackage from data
    for i in data:
        del i['$type']
        del i['ClassPackage']
    #make a dict from data with keys as outerindex and value as objectname
    data_dict = {}
    num_idx = 1
    for i in data:
        data_dict[(num_idx * -1)] = i['OuterIndex']
        num_idx += 1

    #make a dict from data with keys as length from start of list and value as objectname
    data_dict2 = {}
    num_idx = 1
    for i in data:
        data_dict2[(num_idx * -1)] = i['ObjectName']
        num_idx += 1
    return data_dict, data_dict2

def import_interpreter(dict1, dict2, obj_idx):
    #get object name from dict2
    obj_name = dict2[obj_idx]
    #get object index from dict1
    package_idx = dict1[obj_idx]
    package_path = dict2[package_idx]
    full_path = package_path + '.' + obj_name
    #print(f'{obj_name} imported as {full_path}')
    return full_path




def datatable_to_csv(json_file,Output):
    with open(json_file) as json_data:
        json_data = json.load(json_data)['Exports']
        print('Json Loaded')
    dict1, dict2 = import_mapper(json_file)
    #Removes unwanted keys
    json_data = key_cleanse(json_data, ['Table','','',''])
    #only gets json_data after key "Data"
    json_data = json_data[0]['Table']['Data']

    #Replace all Name keys with RowName
    for i in json_data:
        i['RowName'] = i['Name']
        del i['Name']
    #if entry has a key other than RowName delet it
    keytokeep = ['RowName', 'Value','','']
    json_data = key_cleanse(json_data,keytokeep)
    #print(json_data)

    #make append values to collumn name list if key is 'RowName'
    Row_names = []
    for i in json_data:
        for key in i:
            if key == 'RowName':
                Row_names.append(i[key])
    #print(Row_names)

    #make append values to collumn name list if key is 'Value'
    Values = []
    for i in json_data:
        for key in i:
            if key == 'Value':
                Values.append(i[key])
    #print(Values)
    Values2 = []
    for i in json_data:
        for key in i:
            for name in i[key]:
                Values2.append(name)
    #if entry in Values2 is more than 1 character long, add it to new list
    ValuesCleaned = []
    for i in Values2:
        if len(i) > 1:
            ValuesCleaned.append(i)
    Values2 = ValuesCleaned
    #print(Values2[7])


    #if name is in entry in list Values2 add it to new list
    collumn_names = ['Names',]
    for i in Values2:
        if 'Name' in i:
            collumn_names.append(i['Name'])
    collumn_names_length = len(list(set(collumn_names)))
    collumn_names = collumn_names[:collumn_names_length]
    #if entry length is greater than 36 then truncate it to the first x characters, where x is the length of the entry -36
    for i in range(len(collumn_names)):
        if len(collumn_names[i]) > 36:
            entry_length = (len(collumn_names[i])-36)
            collumn_names[i] = collumn_names[i][:entry_length]
    #if $type is in entry in list Values2, add it to new list
    collumn_types_dirty = []
    collumn_types = []
    for i in Values2:
        if '$type' in i:
            collumn_types_dirty.append(i['$type'])
    for j in collumn_types_dirty:
        if 'StructTypes.' in j:
            collumn_types.append('StructPropertyData')
            #print('StructPropertyData')
        else:
            clean_entry = (re.search(r'(?<=UAssetAPI\.PropertyTypes\.)[^,]*(?=, UAssetAPI)', j).group(0))
        #print(f'collumn type entry: {clean_entry}')
            collumn_types.append(clean_entry)
    #print(collumn_types)

    #print(Values2)

    if len(collumn_types) != len(Values2):
        print('Error: Collumn names and collumn types are not the same length')
        print(f'Values2 length: {len(Values2)}')
        print(f'Collumn types length: {len(collumn_types)}')
        exit()
    Stats_entries = []
    num_of_iterations = 0
    FloatProperties = 0
    TextProperties = 0
    BoolProperties = 0
    SoftObjectProperties = 0
    ObjectProperties = 0
    ArrayProperties = 0
    NameProperties = 0
    VectorProperties = 0
    RotatorProperties = 0
    strProperties = 0
    IntProperties = 0
    for k in collumn_types:
        if k == 'FloatPropertyData':
            if 'Value' in Values2[num_of_iterations]:
                   dataentry = str(Values2[num_of_iterations]['Value'])
            dataentry = dataentry[:6]
            dataentry = round(float(dataentry),2)
            dataentry = str(dataentry)
            if '+' not in dataentry and '-' not in dataentry:
                dataentry = '+' + dataentry
            Stats_entries.append(dataentry)
            num_of_iterations += 1
            FloatProperties += 1
        if k == 'TextPropertyData':
            s = str(Values2[num_of_iterations])
            infokeys = (re.findall(r'(?<=\')[^\']\w*(?=\'\:)', s))
            for i in infokeys:
                if 'Value' not in i and '$type' not in i and 'Flags' not in i and 'HistoryType' not in i and 'Namespace' not in i and 'DuplicationIndex' not in i and 'Name' not in i:
                    textkey = str(i)
            if textkey in Values2[num_of_iterations]:
                    Stats_entries.append(Values2[num_of_iterations][textkey])
            num_of_iterations += 1
            TextProperties += 1
        if k == 'BoolPropertyData':
            if 'Value' in Values2[num_of_iterations]:
                    Stats_entries.append(Values2[num_of_iterations]['Value'])
            num_of_iterations += 1
            BoolProperties += 1
        if k == 'SoftObjectPropertyData':
            if 'Value' in Values2[num_of_iterations]:
                    Stats_entries.append(Values2[num_of_iterations]['Value'])
            num_of_iterations += 1
            SoftObjectProperties += 1
        if k == 'ObjectPropertyData':
            if 'Value' in Values2[num_of_iterations]:
                    obj_path = import_interpreter(dict1, dict2, int(Values2[num_of_iterations]['Value']))
                    Stats_entries.append(obj_path)
            num_of_iterations += 1
            ObjectProperties += 1
        if k == 'NamePropertyData':
            if 'Value' in Values2[num_of_iterations]:
                    Stats_entries.append(Values2[num_of_iterations]['Value'])
            num_of_iterations += 1
            NameProperties += 1
        if k == 'StrPropertyData':
            if 'Value' in Values2[num_of_iterations]:
                    Stats_entries.append(Values2[num_of_iterations]['Value'])
            num_of_iterations += 1
            strProperties += 1
        if k == 'IntPropertyData':
            if 'Value' in Values2[num_of_iterations]:
                    Stats_entries.append(Values2[num_of_iterations]['Value'])
            num_of_iterations += 1
            IntProperties += 1
        if k == 'VectorPropertyData':
            Stats_entries.append('N/A')
            num_of_iterations += 1
            VectorProperties += 1
        if k == 'RotatorPropertyData':
            Stats_entries.append('N/A')
            num_of_iterations += 1
            RotatorProperties += 1
        if k == 'StructPropertyData':
            Stats_entries.append('Struct')
            num_of_iterations += 1
        if k == 'ArrayPropertyData':
            arr_types = []
            arr_entries = []
            arr_Values = (Values2[num_of_iterations]['Value'])
            num_of_arr_iterations = 0
            arr_types = (re.findall(r'(?<=UAssetAPI\.PropertyTypes\.)[^,]*(?=, UAssetAPI)', str(arr_Values)))
            for o in arr_types:
                if o == 'FloatPropertyData':
                    if 'Value' in arr_Values[num_of_arr_iterations]:
                        dataentry = str(arr_Values[num_of_arr_iterations]['Value'])
                        dataentry = dataentry[:6]
                        dataentry = round(float(dataentry),2)
                        dataentry = str(dataentry)
                        if '+' not in dataentry and '-' not in dataentry:
                            dataentry = '+' + dataentry
                        arr_entries.append(dataentry)
                        num_of_arr_iterations += 1
                if o == 'TextPropertyData':
                    s = str(arr_Values[num_of_arr_iterations])
                    infokeys = (re.findall(r'(?<=\')[^\']\w*(?=\'\:)', s))
                    for i in infokeys:
                        if 'Value' not in i and '$type' not in i and 'Flags' not in i and 'HistoryType' not in i and 'Namespace' not in i and 'DuplicationIndex' not in i and 'Name' not in i:
                            textkey = str(i)
                    if textkey in arr_Values[num_of_arr_iterations]:
                        arr_entries.append(arr_Values[num_of_arr_iterations][textkey])
                    num_of_arr_iterations += 1
                if o == 'ObjectPropertyData':
                    if 'Value' in arr_Values[num_of_arr_iterations]:
                        obj_path = import_interpreter(dict1, dict2, int(arr_Values[num_of_arr_iterations]['Value']))
                        arr_entries.append(obj_path)
                    num_of_arr_iterations += 1
                if o == 'BoolPropertyData' or o == 'SoftObjectPropertyData' or o == 'NamePropertyData' or o == 'StrPropertyData' or o == 'IntPropertyData':
                    if 'Value' in arr_Values[num_of_arr_iterations]:
                        arr_entries.append(arr_Values[num_of_arr_iterations]['Value'])
                    num_of_arr_iterations += 1
            #print(f'Array Types: {arr_types}')
            #print(f'Array Values: {arr_Values}')
            #print(f'Array Entries: {arr_entries}')
            arr_dataentries = ' | '.join(arr_entries)
            Stats_entries.append(arr_dataentries)
            num_of_iterations += 1
            ArrayProperties += 1
        if k != 'FloatPropertyData' and k != 'TextPropertyData' and k != 'BoolPropertyData' and k != 'SoftObjectPropertyData' and k != 'ObjectPropertyData' and k != 'ArrayPropertyData' and k != 'NamePropertyData' and k != 'VectorPropertyData' and k != 'RotatorPropertyData' and k != 'StrPropertyData' and k != 'IntPropertyData' and k != 'StructPropertyData':
            print('Error: Unknown property type')
            print(f'{k} was not recognized\nThis can jeopardize output integrity')
            num_of_iterations += 1
    if VectorProperties > 0:
        print(f'{VectorProperties} VectorProperties can\'t be parsed in a csv')
    if RotatorProperties > 0:
        print(f'{RotatorProperties} RotatorProperties can\'t be parsed in a csv')
    if RotatorProperties > 0 or VectorProperties > 0:
        print('Properties that can\'t be parsed in a csv will be output as \"N/A\"')
    #group entries into lists
    l = len(collumn_names) - 1
    Stats_entries = [Stats_entries[i:i+l] for i in range(0, len(Stats_entries), l)]
    print('Data extracted and sorted')
    #print(Stats_entries)
    #add Row_names to stats_entries list at the begining of groups
    for i in range(len(Stats_entries)):
        Stats_entries[i].insert(0,Row_names[i])
    #write to csv
    with open(Output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(collumn_names)
        for i in Stats_entries:
            writer.writerow(i)
    print('imports interpreted successfully')
    print('CSV Created')






import argparse
def main():
    
    parser = argparse.ArgumentParser(description='Interprets UE4 data table files and writes them to a csv file ; Use UassetGUI to get the json file')
    # action = parser.add_mutually_exclusive_group()
    # action2 = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-i', '--input', help='Input file(Json or UAsset)', required=True)
    args = parser.parse_args()
    if args.input:
        input_file = args.input
        file_extension = input_file.split('.')[-1]
        if file_extension == 'json':
            json_file = input_file
            Output_file = input_file.replace('.json', '.csv')
            Type = get_type(json_file)
            if Type == 'UDataTable':
                print('DataTable Found')
                dict1, dict2 = import_mapper(json_file)
                datatable_to_csv(json_file, Output_file)
            else :
                print('DataTable Not Found')
                exit()
        else:
            print('File extension not supported')
            exit()


if __name__ == '__main__':
    main()
