#!/usr/bin/python
# -*- coding: utf-8 -*-
import extract
from parse_giza import *
from sys import stderr

sentence2 = 'See you on Sunday at 6 : 30 . '.split()
alignment2 = parse('NULL ({ }) Hẹn ({ 1 }) gặp ({ }) lại ({ }) anh ({ 2 }) vào ({ }) chủ ({ 3 }) nhật ({ 4 }) lúc ({ 5 }) 6 ({ 6 }) giờ ({ 7 }) 30 ({ 8 }) . ({ 9 }) ')

sentence1 = 'Hẹn gặp lại anh vào chủ nhật lúc 6 giờ 30 . '.split()
alignment1 = parse('NULL ({ }) See ({ 1 2 3 }) you ({ 4 }) on ({ }) Sunday ({ 5 6 7 }) at ({ 8 }) 6 ({ 9 }) : ({ 10 }) 30 ({ 11 }) . ({ 12 }) ')


#sentence1 = 'Tôi có một cuộc hẹn vào tối thứ 7 lúc 7 giờ 30 .'.split()
#alignment1 = parse('NULL ({ }) I ({ 1 }) have ({ 2 }) an ({ 3 }) appointment ({ 4 5 }) Saturday ({ 6 }) evening ({ 7 }) at ({ }) 7 ({ 8 9 10 11 }) : ({ 12 }) 30 ({ 13 }) .. ({ 14 })')

#sentence2 = 'I have an appointment Saturday evening at 7 : 30 ..'.split() 
#alignment2 = parse('NULL ({ }) Tôi ({ 1 }) có ({ 2 }) một ({ }) cuộc ({ 3 }) hẹn ({ 4 }) vào ({ 5 }) tối ({ 6 }) thứ ({ }) 7 ({ 11 }) lúc ({ 7 }) 7 ({ 8 }) giờ ({ 9 }) 30 ({ 10 }) . ({ }) ')

# Sentence pair (17) source length 13 target length 11 alignment score : 6.33582e-13
sentence1 = 'Tôi đã làm như nhưng vẫn chưa có trả lời . '.split()
alignment1 = parse('NULL ({ 8 }) I ({ 1 }) &apos;ve ({ 2 }) already ({ }) done ({ 3 4 }) that ({ }) , ({ }) but ({ 5 }) there ({ }) &apos;s ({ }) no ({ }) reply ({ 6 7 }) yet ({ 9 10 }) . ({ 11 }) ')

# Sentence pair (17) source length 11 target length 13 alignment score : 2.07412e-16
sentence2 = 'I &apos;ve already done that , but there &apos;s no reply yet . '.split()
alignment2 = parse('NULL ({ 6 9 }) Tôi ({ 1 }) đã ({ 2 }) làm ({ 3 4 }) như ({ 5 }) nhưng ({ 7 }) vẫn ({ 8 10 }) chưa ({ 11 }) có ({ }) trả ({ 12 }) lời ({ }) . ({ 13 }) ')

fout = open("output.html", "w")
tables=[]
tables.append(html_table(sentence1, sentence2, alignment2))
#fout.write('<br>')
#tables.append( html_table(sentence1, sentence2, transform(alignment1)))
tables.append( html_table(sentence1, sentence2, transform(alignment1)))
#fout.write('<br>')
lex = extract.lexicon()

tables.append( html_table(sentence1, sentence2, lex.build_bi_alignment(sentence1, sentence2, transform(alignment1), alignment2)))
fout.write("<table>" + gen_row(tables) + "</table>")
fout.close()

input1 = open("vi_en").readlines()
input2 = open("en_vi").readlines()

lex = extract.lexicon()

for comment_line in range(0, min(min(len(input1), len(input2)), 17*3), 3):
    print >> stderr, "parsing", comment_line/3
    source_line = comment_line + 1
    alignment_line = comment_line + 2
    sentence1 = input1[source_line].split()
    sentence2 = input2[source_line].split()
    alignment1 = parse(input1[alignment_line])
    alignment2 = parse(input2[alignment_line])

#    alignment2 = transform(alignment2)
    alignment1 = transform(alignment1)
    #print
    #print 'sentence1 = ', sentence1
    #print 'alignment1 = ', alignment1
    #print 'sentence2', sentence2
    #print 'alignment2', alignment2
    #print 
    #lex.build_bi_alignment(sentence1,  sentence2, alignment1, alignment2)
    lex.train(sentence1, sentence2, alignment1, alignment2)

    
lex.generate_output()
    

#print pretty_table(sentence1, sentence2, alignment2)






