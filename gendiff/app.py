from os import path

from gendiff._formaters import handle_ast
from gendiff._utils import get_diff_ast, get_parsed_data


def generate_diff(first_file, second_file, format="stylish"):
    filepath1, filepath2 = path.abspath(first_file), path.abspath(second_file)
    data1 = get_parsed_data(filepath1)
    data2 = get_parsed_data(filepath2)
    ast = get_diff_ast(data1, data2)
    # print('ast =>>>', ast)
    data = handle_ast(ast, format)
    f = open("tmp.txt", "w")
    f.write(data)
    f.close()
    return data
