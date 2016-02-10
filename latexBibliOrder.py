#!/usr/bin/env python

"""
This program reads one or more bib file, separates its bibtex entries
and reorders its items in a designated order.

Processing include:
    -- reordering
    -- reassignation of key_name
    -- inclusion of double curly braquets in title
    -- removal of eprint, abstract, ... if any
    -- hide url from output file, but keep it for excelBibData.py
    -- save file as latexBibliOrder.bib
"""

import sys, os, glob, re
import numpy as np


#===============================================================================
def main():
#===============================================================================

    """
    This main() function does the main part of script

    """

    # make python get the fullpath to the current working directory
    # and define useful folder names
    cwd           = os.getcwd()
    input_folder  = os.path.join(cwd, 'bib_input_files/')
    output_folder = os.path.join(cwd, 'bib_output_file/')

    # list the input .bib files to read in the input folder (two steps)
    # a- define the pattern you are looking for:
    pattern       = os.path.join(input_folder, '*.bib')
    # b- create a list of all files that fullfil this pattern
    inFileList    = glob.glob(pattern) 
    print inFileList

    # a- we warn the user
    # b- we exit the script
    if len(inFileList)==0:
        print 'there are no .bib files in folder %s' %cwd
        sys.exit()

    # now we proceed with cleaning the input files:

    # ------------------ here the actual cleaning begins -------------------

    # initialize an empty string to store clean bib_items from all files
    files_as_one_string = ''

    # ------------------------ loop over .bib files ------------------------

    # for each input file: 
    for filename in inFileList:

        # read the content of the file as one string then close the file
        f = open(filename, 'r') # r for read-only
        files_as_one_string += f.read()
        f.close()

    # ------------------- we exit the loop on bib files --------------------

    # split the contents into bib_item:
    bib_separator = '@'
    bib_items     = files_as_one_string.split(bib_separator)

    # we remove the first item which is an empty string:
    del bib_items[0]

    # ----------------- loop over unclean bib entries ----------------------

    # we initialize a matrix in which to store the product of our cleaning
    # number of columns = number of bib entries
    # number of rows    = number of ref items per entry
    nbrows  = 17
    nbcols  = len(bib_items)
    # NB: because we want the array to store strings and not floats, we have
    # to set the data type of that array to 'arbitrary object':
    clean_entries = np.array([['']*nbcols]*nbrows, dtype=object)


    # for each bib_item of the total list:
    for i in range(nbcols):

        # split the bib_item into its ref_item (cite_key, title, ...)
        if ',\r\n' in files_as_one_string:
            ref_item_separator = ',\r\n'
        else:
            ref_item_separator = ',\n'

        list_ref_items     = bib_items[i].split(ref_item_separator)

        # loop over the rows:
        for j,stuff in enumerate(list_ref_items):

            if j==0: 
                bib_type     = stuff.split('{')[0]
                bib_cite_key = stuff.split('{')[1]
                print bib_type, bib_cite_key

                clean_entries[0][i] = bib_type
                clean_entries[1][i] = bib_cite_key        
            else:
                key    = stuff.split('=')[0].strip(' ') #NB: we remove the white spaces before and after the string
                value  = stuff.split('=')[1].strip(' ')
                print key, value

                if key=='author':      clean_entries[2][i] = value
                if key=='editor':      clean_entries[3][i] = value  
                if key=='title':       clean_entries[4][i] = value  
                if key=='booktitle':   clean_entries[5][i] = value  
                if key=='chapter':     clean_entries[6][i] = value  
                if key=='institution': clean_entries[7][i] = value  
                if key=='school':      clean_entries[8][i] = value  
                if key=='journal':     clean_entries[9][i] = value  
                if key=='volume':      clean_entries[10][i] = value  
                if key=='number':      clean_entries[11][i] = value  
                if key=='pages':       clean_entries[12][i] = value  
                if key=='note':        clean_entries[13][i] = value  
                if key=='url':         clean_entries[14][i] = value  
                if key=='doi':         clean_entries[15][i] = value  
                if key=='year':        clean_entries[16][i] = value  

    print clean_entries

    # clean the ref_items and store them into out matrix
    #clean_entries[column,:] = clean_bib(list_ref_items)
    # ---------------- we exit the loop on bib entries ---------------------

    # Finally: remove duplicates from matrix

    # sort alphabetically 

    # initialize an output file, which will be stored in the 'output' folder

    #res = open('test.txt','wb')
    #for stuff in bib_items:
    #    res.write(stuff)
    #res.close()


    # write all non-duplicates, sorted clean bib_items to the master.bib file:
    # NB: what you write is entry_type dependant

    #for ...

    #    if entry_type=='article':
    #         output_file.write (....)
    #    elif entry_type=='book': 
    #         output_file.write (....)
    #    elif entry_type=='chapter':
    #         output_file.write (....)
    #    elif entry_type=='website':
    #         output_file.write (....)
    #    else:
    #         output_file.write (....)

    # close the output file

    # write a message to user to report success of the cleaning, and where to
    # find the clean file

    # exit the script
    return None



#===============================================================================
def clean_bib(list_ref_items):
#===============================================================================

    """
    clean_bib() cleans 1 bibliographic entry that has been separated into its 
    ref_items NB: I assume here we separated the bib_item string into its 
    numerous ref_item strings using the return symbols ('\n') as separator

    For example, we provide the following of ref_items to the function:
    [ 'article{Mascle1990271',
    'title = "Shallow structure and (...) on continuous reflection profiles "',
    'journal = "Marine Geology "',
    'volume = "94"',
    'number = "4"',
    'pages = "271 - 299"',
    'year = "1990"',
    'note = ""',
    'issn = "0025-3227"',
    'doi = "http://dx.doi.org/10.1016/0025-3227(90)90060-W"',
    'url = "http://www.sciencedirect.com/science/article/pii/002532279090060W"',
    'author = "Jean Mascle and Laure Martin"',
    'abstract = "A dense grid of (...) subduction is still active. "\r\n}\r\n']

    We want to convert the ref_items with the following rules:
    - for all ref_items: 
        * we use { } instead of "".
        * we write as ref_item = {Sth sth sth}, instead of other formats that
          are more chunky. Note the position of the brackets and that of the 
          comma and the spacing among elements above.
        * no ref_item has spaces at the beginning or the end of the {}.

    - we format some specific ref_items: 
        * cite_key  last_name:YYa
        * title     title = {{title_text}}
        * author    author = {Last_name1, Initials, Last_name2, Initials, etc}
        * pages     pages = {number--number}
        * year      year = {YYYY}
        * volume    volume = {volume_string}
        * number    number = {number}

    - we remove the following ref_items:
        abstract, type, series, organization, note, annote, crossref, edition, 
        howpublished, month, issn

    - we reorder the ref_items inside each bib_entry as follows
        @entry_type{cite_key,
        author,
        title,
        journal,
        volume,
        number (if any),
        pages,
        doi (if any),
        year
        }

    """

    # get the cite_key (it's the first ref_item read from the bib_item)
    cite_key = list_ref_items[0]     # e.g. cite_key is now 'article{Mascle1990271'

    # we discard the bib entry type so we get the string 'Mascle1990271' instead
    clean_cite_key = cite_key.split('{')[1]

    # we clean the other entries: (follow the rules)
		  
    # we store the clean data into a list
    list_clean_ref_items = [clean_cite_key, etc, etc]

    # the function returns that list
    return list_clean_ref_items

#===============================================================================
if __name__=='__main__':
    main()
#===============================================================================

"""
Some possible features to add to the main script:
-------------------------------------------------

I don't know how difficult would this be, but... what about warning if it finds
entries that have largely coincidental strings, i.e., duplicates but that have
mistakes on them, that a super thorough examination (one to one) won't detect.

I think this is too difficult to automate if we have done the cleaning to the
max. At the end, the user will anyway look at the sorted bibliography to get
the cite_keys for LaTex, and he/she can detect "hidden" duplicates and delete
them (they will follow each other in the clean list, since such duplicates
should have almost same authors, year, title)


Define what an individual bibtex entry is:
    bib_item = []
    key_string = "@"
    separator = re.findall(r'{@}',exampleString)

def bib_item():
    for key_string in bib_file:
        if key_string()

Find everthing between @, and include each in bib_item including @ in the first
one, and leaving out the second one

"""
