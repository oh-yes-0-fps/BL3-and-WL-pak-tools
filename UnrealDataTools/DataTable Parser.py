import json
import csv



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




def datatable_to_csv(json_file,Output):
    with open(json_file) as json_data:
        json_data = json.load(json_data)['Exports']
        print('Json Loaded')

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
    #Gets stat values from Values2
    Stats_entries = []
    for i in Values2:
        if 'Value' in i:
            Stats_entries.append(i['Value'])
    #change objects in list to strings
    for i in range(len(Stats_entries)):
        Stats_entries[i] = str(Stats_entries[i])
    #Truncate all values to 6 cahracters
    for i in range(len(Stats_entries)):
        Stats_entries[i] = Stats_entries[i][:6]
    #Round all values to 2 decimal places
    for i in range(len(Stats_entries)):
        Stats_entries[i] = round(float(Stats_entries[i]),2)
    #change objects in list to strings # Im actually not sure whats going on here but i don't question it
    for i in range(len(Stats_entries)):
        Stats_entries[i] = str(Stats_entries[i])
    #if entry does not have a '+' or '-' add '+' to the front
    for i in range(len(Stats_entries)):
        if '+' not in Stats_entries[i] and '-' not in Stats_entries[i]:
            Stats_entries[i] = '+' + Stats_entries[i]
    #group entries into lists of 3
    Stats_entries = [Stats_entries[i:i+3] for i in range(0, len(Stats_entries), 3)]
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
    print('CSV Created')

import argparse
def main():
    
    parser = argparse.ArgumentParser(description='Interprets UE4 data table files and writes them to a csv file')
    # action = parser.add_mutually_exclusive_group()
    # action2 = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-i', '--input', help='Input file(Json or UAsset)', required=True)
    parser.add_argument('-d', '--datatable', help='is datatable', action='store_true')
    args = parser.parse_args()
    if args.input:
        input_file = args.input
        file_extension = input_file.split('.')[-1]
        if file_extension == 'json':
            json_file = input_file
            Output_file = input_file.replace('.json', '.csv')
            if args.datatable:
                Type = get_type(json_file)
                if Type == 'UDataTable':
                    print('DataTable Found')
                    datatable_to_csv(json_file, Output_file)
                else :
                    print('DataTable Not Found')
                    exit()
            else:
                print('Not a DataTable')
                print('Please use -d to specify if the file is a datatable')
                exit()
        else:
            print('File extension not supported')
            exit()


if __name__ == '__main__':
    main()
