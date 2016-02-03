#!/usr/bin/env python

"""
This program inputs a text (.rtf) file, finds its bibtex entries
and reorders its items in a designated order that DFB likes.

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
    The main() function does the main part of script

    """

    # define the folder to search .bib files in (here: I assume the current dir)
    cwd = os.getcwd()

    # list the input .bib files to read: it is actually easy in two lines:
    # first define the pattern you are looking for in the current directory:
    pattern = os.path.join(cwd, “*.bib”)
    # then create a list of all files that have the “.bib” name extension
    inFileList = glob.glob(pattern) 

    # if we do not find a “.bib” file in the specified folder, we exit
    if len(inFileList==0):
        print “there are no ‘.bib’ files in folder %s”%cwd
        sys.exit()

    # else, we proceed with the cleaning code:
    else:

        # ------------------ here the actual cleaning begins -------------------
        # create an empty output “biblio.bib” file

        # initialize an empty list to store clean bib_items from all files

        # ------------------------ loop over .bib files ------------------------
        # for each refs.bib file: 
        for ...:

            # read the content of the file as one string
            f = open(filename, ‘r’) # r for read-only
            one_string = f.read()
            f.close()

            # split the contents into bib_item:
            bib_separator = ‘@’
            list_bib_items = file_as_one_string.split(bib_separator)

            # ----------------- loop over unclean bib entries ------------------
            # for each unclean bib_item:
            for ...:

                # split the bib_item into its ref_item (cite_key, title, ...)
                ref_separator = ‘\n’
                list_ref_items = bib_item.split(ref_separator)

                # clean all ref_items of the bib_item
                clean_bib_item = clean_bib(list_ref_items)

                # add clean_bib_item to the list of clean bib_items

            # ---------------- we exit the loop on bib entries -----------------

        # ------------------- we exit the loop on bib files --------------------

        # within the final list of clean_bib_items, compare unique cite_keys and
        # remove duplicates

        # if len(clean_bib_items)==0
            # sort the list of clean bib_items alphabetically 

        # write all non-duplicates, sorted clean bib_items to the master.bib file:
        # NB: what you write is entry_type dependant
        if entry_type=='article':
             write (....)
        elif entry_type=='book': 
             write (....)
        elif entry_type=='chapter':
             write (....)
        elif entry_type=='website':
             write (....)
        else:
             write (....)

    return None

"""
Some possible features to add to the main script:
-------------------------------------------------

I don’t know how difficult would this be, but… what about warning if it finds
entries that have largely coincidental strings?, i.e., duplicates but that have
mistakes on them, that a super thorough examination (one to one) won’t detect.

I think this is too difficult to automate if we have done the cleaning to the
max. At the end, the user will anyway look at the sorted bibliography to get
the cite_keys for LaTex, and he/she can detect “hidden” duplicates and delete
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


#===============================================================================
def clean_bib(list_ref_items):
#===============================================================================

    """
    clean_bib() cleans 1 bibliographic entry that has been separated into its 
    ref_items NB: I assume here we separated the bib_item string into its 
    numerous ref_item strings using the return symbols (‘\n’) as separator

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
        * we use { } instead of “ ”.
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

    # get the cite_key (it’s the first ref_item read from the bib_item)
    cite_key = list_ref_items[0]     # e.g. cite_key is now 'article{Mascle1990271'

    # we discard the bib entry type so we get the string 'Mascle1990271' instead
    clean_cite_key = cite_key.split(‘{’)[1]

    # we clean the other entries: (follow the rules)
		  
    # we store the clean data into a list
    list_clean_ref_items = [clean_cite_key, etc, etc]

    # the function returns that dictionary
    return list_clean_ref_items

#===============================================================================
if __name__=='__main__':
    main()
#===============================================================================
