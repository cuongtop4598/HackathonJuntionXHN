import re
import random
import hashlib
from .const import *
from .evalute import *
from .decoder import transform_column
from .utils import escape_format
from .utils import common_string, cs_compress
from itertools import combinations

def cs_filter(cs_set):
    length = 1
    while True :
        cs_set = set(filter(lambda x : len(x) >= length, cs_set))
        if len(cs_set) < 10 :
            break
        length += 1
    return cs_set

def split_fixed(strings_set, filtered_set):
    cs_combination = []
    for i in range(len(filtered_set), 0, -1):
        _next_combination = list(combinations(filtered_set, i))
        random.shuffle(_next_combination)
        cs_combination.extend(_next_combination)
    for per in cs_combination :
        _const = None
        reg = str(f"({'|'.join([escape_format(p) for p in per])})")
        output_set = []
        for ss in strings_set :
            const = '&'.join([ hashlib.md5(find.group().encode()).hexdigest() for find in re.finditer(reg, ss)])
            if _const == None :
                _const = const
            if _const != None and const != _const :
                break
            tmp = re.split(reg, ss)
            output = []
            for s in tmp :
                if s in per :
                    output.append(filtered_set.index(s))
                else :
                    output.append(s)
            output_set.append(output)
        else :
            return output_set
    else :
        return [ [strs] for strs in strings_set]

def preprocessor(target):
    cs_set = common_string(target)
    cs_set = cs_compress(cs_set)
    filtered_set = list(cs_filter(cs_set))
    split_str = split_fixed(target, filtered_set)

    return split_str, filtered_set

def parser(arr, filtered_set, gene, positive=[], negative=[]):
    output = []
    value = 0
    for i in range(len(arr[0])):
        column = [val[i] for val in arr]
        if i == 0 and len(''.join(column)) == 0:
            output.append('^')
        elif i == len(arr[0])-1 and len(''.join(column)) == 0:
            output.append('$')
        elif type(column[0]) == int:
            value += 500
            output.append(escape_format(filtered_set[column[0]]))
        else:
            possible, seq = transform_column(column, gene)
            seq = fitness(possible, seq, positive, negative)
            output.append(possible)
            value += seq
    return output, value
