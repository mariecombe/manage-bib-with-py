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
