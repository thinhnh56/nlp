import re
from tabulate import tabulate

def parse(input):
    p = re.compile('\{.*?\}')
    parsed = [ [int(digit) - 1 for digit in numbers[1:-1].split()] for numbers in p.findall(input) [1:] ]

    return set(reduce(list.__add__,
                  [[(target, foreign) for foreign in foreigns] for target, foreigns in enumerate(parsed)]))

def transform(alignment):
    return set([ (j, i) for i, j in alignment])

def pretty_format(sentence1, sentence2, alignment):
    first_column_len = max(map(len, sentence1))
    other_lens = [max(8, l) for l in map(len, sentence2)]

    output = ' ' * (first_column_len + 1)
    output += '|'.join([w.center(l) for l, w in zip(other_lens, sentence2)])
    output += '\n'

    for index_in_1, word_in_1 in enumerate(sentence1):
        output += word_in_1.center(first_column_len + 1)
        for index_in_2 in range(len(sentence2)):
            mark = 'X' if (index_in_1, index_in_2) in alignment else ' ';
            output += mark.center(other_lens[index_in_2] + 1)

        output += '\n\n'

    return output
    
def gen_row(col_datas):
    return "<tr>" + ''.join(["<td>" + data + "</td>" for data in col_datas]) + "</tr>"

def html_table(sentence1, sentence2, alignment):
    first_column_len = max(map(len, sentence1))
    other_lens = [max(8, l) for l in map(len, sentence2)]

    result = gen_row([''] + sentence2)
    
    for index_in_1, word_in_1 in enumerate(sentence1):
        output = []

        result += gen_row([word_in_1, ] +
                          ['X' if (index_in_1, index_in_2) in alignment else ' '
                           for index_in_2 in range(len(sentence2))])
    return "<table border=1>" + result + "</table>"
    
def pretty_table(sentence1, sentence2, alignment):
    header = [' '] + sentence2
    table = [[sentence1[ind1]]+['X' if (ind1, ind2) in alignment else ' ' for ind2 in range(len(sentence2))]
      for ind1 in range(len(sentence1)) ]
    print tabulate(table, header, tablefmt="grid")
    
    
#print parse('NULL ({ }) I ({ 1 }) hope ({ 2 3 4 }) so ({ 5 }) , ({ }) too ({ 6 }) . ({ 7 }) ')

