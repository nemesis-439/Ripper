import sys
import platform
import io
import re

# ------------- CLASS PART of PROGRAM -------------

class pattern_object(object):
    """objekt s metodami pro regex a write log dat. """
    def __init__(self, loc_pattern_line, loc_pattern_file):
        self.pattern_line=loc_pattern_line
        self.pattern_mask=re.compile(self.pattern_line)
        self.pattern_file_name=loc_pattern_file
        self.f=''
        self.counter=0
        return

    def close_file(self):
        self.f.close()
        return

    def open_file(self):
        #print " open_file: ", self.pattern_file
        self.f=io.open(self.pattern_file_name, 'w', encoding='utf-8')
        return



class pattern_list_object(object):
    """Objekt s metodami spravujici pattern objekty. Nacte config ini file a rozdeli jej do objektu."""
    def __init__(self, loc_file_name):
        self.file_name = loc_file_name
        self.f=''
        self.counter=0
        self.pattern_list=[]
        return

    def close_file(self):
        self.f.close()
        return

    def open_file(self):
        self.f=io.open(self.file_name, 'r', encoding='utf-8')
        return

    def read_line_pattern_file(self):
        self.open_file()
        self.counter=0
        for line in self.f:
        #    print "* -> %r | log-rip-%i.txt" % (line[:-1], i)
            loc_pattern_obj=pattern_object( line[:-1],"log-rip-%i.txt" % (self.counter) )
            self.pattern_list.append(loc_pattern_obj)
            self.counter+=1
        self.close_file()
        return


class log_list_object(object):
    """Objekt s metodami spravujici pattern objekty. Nacte config ini file a rozdeli jej do objektu."""
    def __init__(self, loc_file_name):
        self.file_name = loc_file_name
        self.f=''
        self.match_pattern_list=[]
        self.no_match_pattern=pattern_object( "","log-no-match.txt" )
        return

    def close_file(self):
        self.f.close()
        for match_pattern in self.match_pattern_list:
            match_pattern.close_file()
        self.no_match_pattern.close_file()
        return

    def open_file(self):
        self.f=io.open(self.file_name, 'r', encoding='utf-8')
        for match_pattern in self.match_pattern_list:
            match_pattern.open_file()
        self.no_match_pattern.open_file()
        return

    def print_resume(self):
        print "--------------- Result report ---------------";
        for regex in self.match_pattern_list:
           print "For pattern=%r\t are found %i lines and results are written to file=%r." %(regex.pattern_line, regex.counter, regex.pattern_file_name)
        print "I can not match %i lines and this lines are written to file=%r." %(self.no_match_pattern.counter, self.no_match_pattern.pattern_file_name)
        return

    def read_line_log_file(self):
        self.open_file()
        for line in self.f:
            state=False
            for regex in self.match_pattern_list:
                #print 'Looking for "%s" in "%s" ->' % (regex.pattern_line, line),
                if regex.pattern_mask.search(line):
                    # print 'found a match!\n'
                    # print line
                    regex.f.write(line)
                    regex.counter+=1
                    state=True
                    break
            if not state :
                self.no_match_pattern.f.write(line)
                self.no_match_pattern.counter+=1
        self.close_file()
        return

# ------------- MAIN PART of PROGRAM -------------
print platform.system() + " " + platform.release() + "\nPython " + sys.version + "\n"

p=pattern_list_object("config-unix-message.in")
p.read_line_pattern_file()

l=log_list_object("/var/log/system.log")
l.match_pattern_list=p.pattern_list
l.read_line_log_file()
l.print_resume()

del l
del p
# ------------- END PART of PROGRAM -------------
