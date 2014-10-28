#!/usr/bin/python
# -*- coding: utf-8 -*-
import extract
from parse_giza import *
from sys import stderr

sentence2 = 'See you on Sunday at 6 : 30 . '.split()
alignment2 = parse('NULL ({ }) Hẹn ({ 1 }) gặp ({ }) lại ({ }) anh ({ 2 }) vào ({ }) chủ ({ 3 }) nhật ({ 4 }) lúc ({ 5 }) 6 ({ 6 }) giờ ({ 7 }) 30 ({ 8 }) . ({ 9 }) ')

sentence1 = 'Hẹn gặp lại anh vào chủ nhật lúc 6 giờ 30 . '.split()
alignment1 = parse('NULL ({ }) See ({ 1 2 3 }) you ({ 4 }) on ({ }) Sunday ({ 5 6 7 }) at ({ 8 }) 6 ({ 9 }) : ({ 10 }) 30 ({ 11 }) . ({ 12 }) ')


fout = open("output.html", "w")
tables=[]
tables.append(html_table(sentence1, sentence2, alignment2))
#fout.write('<br>')
tables.append( html_table(sentence1, sentence2, transform(alignment1)))
#fout.write('<br>')
lex = extract.lexicon()

tables.append( html_table(sentence1, sentence2, lex.build_bi_alignment(sentence1, sentence2, transform(alignment1), alignment2)))
fout.write("<table>" + gen_row(tables) + "</table>")
fout.close()

input1 = open("vi_en").readlines()
input2 = open("en_vi").readlines()

lex = extract.lexicon()

for comment_line in range(0, min(min(len(input1), len(input2)), 100*3), 3):
    print >> stderr, "parsing", comment_line/3
    source_line = comment_line + 1
    alignment_line = comment_line + 2
    sentence1 = input1[source_line].split()
    sentence2 = input2[source_line].split()
    alignment1 = parse(input1[alignment_line])
    alignment2 = parse(input2[alignment_line])

    alignment2 = transform(alignment2)
#    alignment1 = transform(alignment1)

    #lex.build_bi_alignment(sentence1,  sentence2, alignment1, alignment2)
    lex.train(sentence1, sentence2, alignment1, alignment2)

    
lex.generate_output()
    

#print pretty_table(sentence1, sentence2, alignment2)






