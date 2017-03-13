import io
import re
from sys import argv

def read_log_file():

    with io.open("/var/log/system.log", 'r', encoding='utf-8') as f:
        loc_log_buffer=f.read()
    f.close()
    return loc_log_buffer

def read_line_log_file():

    with io.open("/var/log/system.log", 'r', encoding='utf-8') as f:
        for line in f:
            #print "* -> %r" % line
            for regex in pattern:
                #print 'Looking for "%s" in "%s" ->' % (regex.pattern, line),
                if regex.search(line):
                    print 'found a match!\n'
                    print line
                # else:
                #     print 'no match\n'
    f.close()
    return

def read_line_pattern_file():

    with io.open("config-unix-message.in", 'r', encoding='utf-8') as f:
        for line in f:
            print "* -> %r" % line[:-1]
            pattern.append(re.compile(line[:-1]))
        f.close()

    print pattern
    return



# Pre-compile the patterns
# regexes = [ re.compile(p) for p in [ 'this',
#                                      'that',
#                                      ]
#             ]
# text = 'Does this text match the pattern?'
#
# for regex in regexes:
#     print 'Looking for "%s" in "%s" ->' % (regex.pattern, text),
#
#     if regex.search(text):
#         print 'found a match!'
#     else:
#         print 'no match'


# ------------- Main program -------------
pattern=[]
#log_buffer=read_log_file()
read_line_pattern_file()

read_line_log_file()





#print (log_buffer)
