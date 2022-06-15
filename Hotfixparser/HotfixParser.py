from dataclasses import replace
import re
from types import NoneType

Input_file =  'hotfix_test.hfm'
Output_file = 'debug.json'
def parse_hf_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    for i in lines:
        if '#' in i:
            lines.remove(i)
    lines = [i.strip() for i in lines]
    for i in lines:
        if '#' in i:
            lines.remove(i)
    for i in lines:
        if '#' in i:
            lines.remove(i)
    return lines




#search for a regex (?<=Entry,\(1,). in a list of lines
def get_hf_details(input, List = True):
    #(re.search(r'', i).group(0))

    def parser_integrated(i, islist):
        Shows_previous_value = False
        specific_arr_address = False
        data = []
        if 'Entry' in i and '#' not in i:
            #universals
            if ',0,,' not in i:
                Shows_previous_value = True
            Entry = re.search(r'.*(?=,\(\d,\d,\d)', i).group(0)
            Type = (re.search(r'(?<=Entry,\(1,).', i).group(0))
            if Type == '1' in i or Type == '2' in i or Type == '7' in i or Type == '4' in i or Type == '5' in i or Type == '8' in i:
                is_map_edit = False
                obj_path = '/Game' + (re.search(r'(?<=\),\/Game)[^,:]*', i).group(0)).split('.')[0]
                obj_name = (re.search(r'(?<=\),\/Game)[^,:]*', i).group(0)).split('.')[1]
            elif Type == '6' in i or Type == '11' in i:
                is_map_edit = True
                map_path = '/Game' + (re.search(r'(?<=\),\/Game)[^,:]*', i).group(0))
                obj_path = '/' + (re.search(r'(?<=,\/)(?<!\),\/)[^,:.]*', i).group(0))
                obj_name = (re.search(r'(?<=,)(?<!\(\d,)(?<!Entry,)[^,:.]*(?=,\d)', i).group(0))
            if Entry != 'SparkPatchEntry':
                entry_guide = (re.search(r'(?<=\(\d,\d,\d,)[^\)]*', i).group(0))
                print(f'Entry info- type: {Entry} Guide: {entry_guide}')
                data.append(f'"entry": "{Entry}",')
                data.append(f' "entry_guide": "{entry_guide}",')
            else:
                print(f'Entry type: {Entry}')
                data.append(f'"entry": "{Entry}",')
            print(f'Type: {Type}')
            data.append(f'"Type": "{Type}",')
            if is_map_edit:
                print(f'"Map: {map_path}",')
                data.append(f'"Map": "{map_path}",')
            print(f'OBJ path : {obj_path}')
            data.append(f'"OBJ path": "{obj_path}",')
            print(f'OBJ name : {obj_name}')
            data.append(f'"OBJ name": "{obj_name}",')
            if Type == '1' in i:
                if ':' in i:
                    sub_obj_name = (re.search(r'(?<=:)[^,]*', i).group(0))
                    print(f'Sub object: {sub_obj_name}')
                    data.append(f'"Sub object": "{sub_obj_name}",')
                if '].' in i and not '[/' in i:
                    specific_arr_address = True
                if '].' not in i:
                    specific_arr_address = False
                if Type == '1' in i:
                    property_list = (re.search(r'(?<=,)[^,]{3,99}(?=,)', i).group(0))
                    if '.' in property_list:
                        property_list = property_list.split('.')
                        prop_num = 1
                        for j in property_list:
                            print(f'Property, layer {prop_num}: {j}')
                            data.append(f'"Property__layer{prop_num}": "{j}",')
                            prop_num += 1
                    else:
                        print(f'Property: {property_list}')
                        data.append(f'"Property": "{property_list}",')

                    
                # if '].' in i and not '[/' in i:
                #     specific_arr_address = True
                #     arr_name = (re.search(r'(?<=(,|.))[^,.:]*(?=\[\d)', i).group(0))
                #     arr_idx = (re.search(r'(?<=\[)\d[^\]]*', i).group(0))
                #     print(f'Array name: {arr_name}')
                #     data.append(f'"Array index": "{arr_idx}",')
                #     print(f'Array Index: {arr_idx}')
                #     data.append(f'"Array name": "{arr_name}",')
                # if '].' not in i:
                #     specific_arr_address = False
                #     property_list = (re.search(r'(?<=,)[^,]{3,99}(?=,)', i).group(0))
                #     if '.' in property_list:
                #         property_list = property_list.split('.')
                #         prop_num = 1
                #         for i in property_list:
                #             print(f'Property, layer {prop_num}: {i}')
                #             data.append(f'"Property__layer{prop_num}": "{i}",')
                #             prop_num += 1
                #     else:
                #         print(f'Property: {property_list}')
                #         data.append(f'"Property": "{property_list}",')
                if Shows_previous_value == False:
                    new_value = (re.search(r'(?<=,0,,).*(?=$)', i).group())
                    print(f'New value: {new_value}')
                    data.append(f'"New value": "{new_value}"')
                else:
                    size_of_new_value = (re.findall(r'(?<=,)[^,]*', i)[6])
                    oldandnewValues = i.split(','+size_of_new_value+',')[-1]
                    old_value = oldandnewValues[:int(size_of_new_value)]
                    new_value = oldandnewValues[int(size_of_new_value):]
                    if new_value[0] == ',':
                        new_value = new_value[1:]
                        print(f'old value: {old_value}')
                        print(f'new value: {new_value}')
                        data.append(f'"old value": "{old_value}",')
                        data.append(f'"new value": "{new_value}"')
                    else:
                        print("Error occured in length of previous value string")
                        data.append('"Error": "occured in length of previous value string",')
                        print('Debug Suggestion: Remove previous value and change # to 0')
                        data.append('"Debug_Suggestion": "Remove previous value and change # to 0"')
            if Type == '7' in i:
                Shows_previous_value = False
                values = (re.findall(r'(?<=:)[^,]{3,999}', i))
                values_len = (re.findall(r'(?<=,)[^,]{1,4}(?=:)', i))
                addresses = (re.findall(r'(?<=\d,)[^,]{2,5}(?=,\d)', i))
                num_of_addresses = len(addresses)
                if num_of_addresses == 1:
                    print(f'Changes {int(num_of_addresses)} value at: {addresses[0]}')
                    data.append(f'"Changes {int(num_of_addresses)} value at": "{addresses[0]}",')
                elif num_of_addresses == 2:
                        print(f'Changes {int(num_of_addresses)} values at: {addresses[0]}, {addresses[1]}')
                        data.append(f'"Changes {int(num_of_addresses)} values at": "{addresses[0]}, {addresses[1]}",')
                elif num_of_addresses == 3:
                        print(f'Changes {int(num_of_addresses)} values at: {addresses[0]}, {addresses[1]}, {addresses[2]}')
                        data.append(f'"Changes {int(num_of_addresses)} values at": "{addresses[0]}, {addresses[1]}, {addresses[2]}",')
                elif num_of_addresses == 4:
                        print(f'Changes {int(num_of_addresses)} values at: {addresses[0]}, {addresses[1]}, {addresses[2]}, {addresses[3]}')
                        data.append(f'"Changes {int(num_of_addresses)} values at": "{addresses[0]}, {addresses[1]}, {addresses[2]}, {addresses[3]}",')
                elif num_of_addresses == 5:
                        print(f'Changes {int(num_of_addresses)} values at: {addresses[0]}, {addresses[1]}, {addresses[2]}, {addresses[3]}, {addresses[4]}')
                        data.append(f'"Changes {int(num_of_addresses)} values at": "{addresses[0]}, {addresses[1]}, {addresses[2]}, {addresses[3]}, {addresses[4]}",')
                print(f'Previous value: {values_len[0]}:{values[0]}')
                data.append(f'"Previous value": "{values_len[0]}:{values[0]}",')
                print(f'New value: {values_len[1]}:{values[1]}')
                data.append(f'"New value": "{values_len[1]}:{values[1]}"')
            if Type == '2' in i:
                DT_info = (re.findall(r'(?<=,)[^,]{3,99}(?=,[^\)])', i))
                #new_value = (re.search(r'(?<=,)[^,]*(?=$)', i).group()) #added functionality elsewhere thats more consistent
                Row_name = DT_info[0]
                Header_name = DT_info[1]
                print(f'Row name: {Row_name}')
                data.append(f'"Row name": "{Row_name}",')
                print(f'Header name: {Header_name}')
                data.append(f'"Header name": "{Header_name}",')
                if Shows_previous_value == False:
                    new_value = (re.search(r'(?<=0,,).*(?=$)', i).group())
                    print(f'New value: {new_value}')
                    data.append(f'"New value": "{new_value}"')
                else:
                    size_of_new_value = (re.findall(r'(?<=,)[^,]*', i)[7])
                    oldandnewValues = i.split(','+size_of_new_value+',')[-1]
                    #replace " with \" in oldandnewValues
                    old_value = oldandnewValues[:int(size_of_new_value)]
                    new_value = oldandnewValues[int(size_of_new_value):]
                    if new_value[0] == ',':
                        new_value = new_value[1:]
                        print(f'old value: {old_value}')
                        print(f'new value: {new_value}')
                        data.append(f'"old value": "{old_value}",')
                        data.append(f'"new value": "{new_value}"')
                    else:
                        print('Error occured in length of previous value string')
                        data.append('"Error": "occured in length of previous value string",')
                        print('Debug Suggestion: Remove previous value and change # to 0')
                        data.append('"Debug_Suggestion": "Remove previous value and change # to 0"')

            if Type == '6' in i or Type == '11' in i:
                location = (re.search(r'(?<=,")[^|]*(?=\|)', i).group(0))
                rotation = (re.search(r'(?<=\|)[^|]*(?=\|)', i).group(0))
                scale = (re.search(r'(?<=\|)[^"]*(?=")', i).group(0))
                print(f'Location [X,Y,Z]: {location}')
                data.append(f'"Location [X,Y,Z]": "{location}",')
                print(f'Rotation [pitch,yaw,roll]: {rotation}')
                data.append(f'"Rotation [pitch,yaw,roll]": "{rotation}",')
                print(f'Scale [X,Y,Z]: {scale}')
                if Type == '6' in i:
                    Opacity = i[-1]
                    if Opacity == '1':
                        Opacity = 'Transparent'
                    elif Opacity == '0':
                        Opacity = 'Opaque'
                    print(f'Opacity: {Opacity}')
                    data.append(f'"Scale [X,Y,Z]": "{scale}",')
                    data.append(f'"Opacity": "{Opacity}"')
                else:
                    data.append(f'"Scale [X,Y,Z]": "{scale}"')
            print('\n')
            # data.append('\n')
            
            return data
        else:
            return 'Error'
            
    if List == True:
        for i in input:
            parser_integrated(i, True)
            return 'done'
    elif List == False:
        output = parser_integrated(input,False)
        return output

def write_json(input):
    input_ext = input.split('.')[-1]
    Output_file = Input_file.replace(input_ext, '_output.json')
    with open(Output_file, 'w') as f:
        entry_num = 0
        f.write('{')
        info = parse_hf_file(Input_file)
        info = [i for i in info if '#' not in i]
        info = [i for i in info if i != '']
        for i in info:
            entry_num += 1
            f.write(','+'\n')
            f.write(f'\"Entry#{entry_num}\" :')
            f.write('{'+'\n')
            out = get_hf_details(i, False)
            for j in out:
                f.write('    ' + j)
                f.write('\n')
            f.write('}')
        f.write('}')
    with open(Output_file, 'r') as f:
        data = f.read()
        data = re.sub(r'(?<=\')(?<! |\\)"(?!:|,| |Entry|}|\n)', '\\\"', data, flags=re.MULTILINE)
        data = re.sub(r'(?<! |\\)"(?=\')(?!:|,| |Entry|}|\n)', '\\"', data, flags=re.MULTILINE)
        data = re.sub(r'(\"(?=,ValueName=)|(?<=ValueName=)"|(?<=RowName=)\"|\"(?=\),))', '\\\"', data, flags=re.IGNORECASE)
        data = re.sub(r'{,\n', '{', data, flags=re.MULTILINE)
        with open(Output_file, 'w') as f:
            f.write(data)








def main():
    import argparse
    parser = argparse.ArgumentParser(description='Parse a hotfix file')
    parser.add_argument('-i', '--input', help='Input file', required=True)
    args = parser.parse_args()
    if args.input:
        Input_file = args.input
        write_json(Input_file)
















if __name__ == '__main__':
    main()