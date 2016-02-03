import sys
import os
import re

'''
This program inputs a text (.rtf) file, finds its bibtex entries
and reorders its items in a designated order that DFB likes.

Processing include:
    -- reordering
    -- reassignation of key_name
    -- inclusion of double curly braquets in title
    -- removal of eprint, abstract, ... if any
    -- hide url from output file, but keep it for excelBibData.py
    -- save file as latexBibliOrder.bib
 '''

####Steps of the program

bib_file = open("bibliobib.rtf", "wb") #Open file or create, and write
bib_file = open("bibliobib.rtf", "ab+") #Open file or create, read and append
bib_file = open("bibliobib.rtf", "r+") #Open file or create, read and writing

#Define what an individual bibtex entry is

bib_item = []
key_string = "@"
separator = re.findall(r'{@}',exampleString)

def bib_item():
    for key_string in bib_file:
        if key_string()
Find everthing between @, and include each in bib_item including @ in the first one, and leaving out the second one


#Find duplicates and remove them

#Reorder the items inside each entry as follows
    #@entry_type{key_name,
    #author{xxxx},
    #title{xxxx},
    #journal{xxxx},
    #volume{xxxx},
    #number{xxxx}, (if any)
    #pages{xxxx},
    #doi{xxxx}, (if any)
    #year{xxxx}
    #}

#Remove every item that not in the list above

#Generate a key_name with format lastnameYY

#Include two curly braquets in title

#Remove comma in year

#Save file as latexBibliOrder.bib

#Include fields of these data in a excel sheet:
    #key_name
    #year
    #title
    #


'''This below will be tryouts for some of the steps of the program:

long_string = bib.file.read() --- to read what's in the file

entry = dkh - everything that starts with a @ until the next @.
long_string.find("@"), which finds the index value of @
((is probably useful for creating entry))

string = text_in_entry

long_string.find("@"), which finds the index value of @
((expected to be useful for creating entry))

long_string.isalpha --- to be use to determine is everything is letters
long_string.isalnum --- to be use to determine is everything is numbers

string.replace("Replaced", "Replacer") --- to be used to replace words

string.strip() --- to remove white space in the string

quote_list = --string.split(" ") --- slipt the string into a list,
and between () we indicate how we want them to be separated

parts of the string

len(string) --- lenght of the string

bib_file.write(bytes("Something to write\n", 'UFT-8')) --- to write in the file

bib.file.close() -- to close the file

for entry in long_string:


os.remove(name_of_file_to_remove) --- removes file

------------------------------------------------------------------------

To append you can open it with "a":
 with open("foo.txt", "a") as f:
     f.write("new line\n")


If you want to preprend something you have to read from the file first:
with open("foo.txt", "r+") as f:
     old = f.read() # read everything in the file
     f.seek(0) # rewind
     f.write("new line\n" + old) # write the new line before


The fileinput module of the Python standard library will rewrite a file inplace if you use the inplace=1 parameter:

import sys
import fileinput

# replace all occurrences of 'sit' with 'SIT' and insert a line after the 5th
for i, line in enumerate(fileinput.input('lorem_ipsum.txt', inplace=1)):
    sys.stdout.write(line.replace('sit', 'SIT'))  # replace 'sit' and write
    if i == 4: sys.stdout.write('\n')  # write a blank line after the 5th line



Rewriting a file in place is often done by saving the old copy with a modified name. Unix folks add a ~ to mark the old one. Windows folks do all kinds of things -- add .bak or .old -- or rename the file entirely or put the ~ on the front of the name.

import shutil
shutil.move( afile, afile+"~" )

destination= open( aFile, "w" )
source= open( aFile+"~", "r" )
for line in source:
    destination.write( line )
    if <some condition>:
        destination.write( >some additional line> + "\n" )
source.close()
destination.close()
Instead of shutil, you can use the following.

import os
os.rename( aFile, aFile+"~" )


The best way to make "pseudo-inplace" changes to a file in Python is with the fileinput module from the standard library:

import fileinput

processing_foo1s = False

for line in fileinput.input('1.txt', inplace=1):
  if line.startswith('foo1'):
    processing_foo1s = True
  else:
    if processing_foo1s:
      print 'foo bar'
    processing_foo1s = False
  print line,
You can also specify a backup extension if you want to keep the old version around,
but this works in the same vein as your code
-- uses .bak as the backup extension but also removes it once the change has successfully completed.


Recall that an iterator is a first-class object. It can be used in multiple for statements.
Here's a way to handle this without a lot of complex-looking if-statements and flags.

with open(tmptxt, 'w') as outfile:
    with open(txt, 'r') as infile:
        rowIter= iter(infile)
        for row in rowIter:
            if row.startswith('foo2'): # Start of next section
                 break
            print row.rstrip(), repr(row)
        print "foo bar"
        print row
        for row in rowIter:
            print row.rstrip()


fileinput already supports inplace editing. It redirects stdout to the file in this case:
#!/usr/bin/env python3
import fileinput

with fileinput.FileInput(fileToSearch, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(textToSearch, textToReplace), end='')


Another way to simply edit files in place is to use the fileinput module:
import fileinput, sys
for line in fileinput.input(["test.txt"], inplace=True):
    line = line.replace("car", "truck")
    # sys.stdout is redirected to the file
    sys.stdout.write(line)