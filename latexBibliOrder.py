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
from operator import itemgetter


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
    #print inFileList

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

    # we initiate a list of invalid bib references
    invalid_refs = list()


    # for each bib_item of the total list:
    for i in range(nbcols):

        # split the bib_item into its ref_item (cite_key, title, ...)
        if '\r\n' in files_as_one_string:
            ref_item_separator = '\r\n'
        else:
            ref_item_separator = '\n'

        list_ref_items     = bib_items[i].split(ref_item_separator)

        # loop over the rows fro the end to the start:
        for j,stuff in enumerate(list_ref_items):
            
            if j==0:
                bib_type     = stuff.split('{')[0]
                bib_cite_key = stuff.split('{')[1]
                clean_entries[0][i]   = bib_type
                clean_entries[1][i]   = bib_cite_key
                #print bib_type, bib_cite_key
            else:
                if len(stuff.split('='))==2:
                    # we separate the key from the value, and we clean their edges
                    # by removing the empty spaces, quotation marks, curly brackets
                    key = stuff.split('=')[0].strip(' ').strip('"').strip('{').strip('}').strip(' ')
                    value  = stuff.split('=')[1].strip(',').strip(' ').strip('"').strip('{').strip('}').strip(' ')
                    #print key, value
                 
                    if key=='author':      
                        author = cleanName(value, i, bib_type)
                        clean_entries[2][i] = author[0]
                        if author[1]!=None: invalid_refs += [author[1]] # if we detected invalid volume
                    if key=='editor':      
                        editor = cleanName(value, i, bib_type)
                        clean_entries[3][i] = editor[0]
                        if editor[1]!=None: invalid_refs += [editor[1]] # if we detected invalid volume
                    if key=='title':       
                        title  = cleanTitle(value, i, bib_type)   
                        clean_entries[4][i] = title[0]
                        if title[1]!=None: invalid_refs += [title[1]] # if we detected invalid volume
                    if key=='booktitle':   
                        btitle = cleanTitle(value, i, bib_type)
                        clean_entries[5][i] = btitle
                        if btitle[1]!=None: invalid_refs += [btitle[1]] # if we detected invalid volume
                    if key=='chapter':     clean_entries[6][i] = value
                    if key=='institution': clean_entries[7][i] = value
                    if key=='school':      clean_entries[8][i] = value
                    if key=='journal':     clean_entries[9][i] = value
                    if key=='volume':      
                        volume = cleanVolume(value, i, bib_type)
                        clean_entries[10][i] = volume[0]
                        if volume[1]!=None: invalid_refs += [volume[1]] # if we detected invalid volume
                    if key=='number':      
                        number = cleanNumber(value, i, bib_type)
                        clean_entries[11][i] = number[0]
                        if number[1]!=None: invalid_refs += [number[1]] # if we detected invalid number
                    if key=='pages':
                        pages = cleanPages(value, i, bib_type)
                        clean_entries[12][i] = pages[0]
                        if pages[1]!=None: invalid_refs += [pages[1]] # if we detected invalid number
                    if key=='note':        clean_entries[13][i] = value
                    if key=='url':         clean_entries[14][i] = value
                    if key=='doi':         clean_entries[15][i] = value
                    if key=='year':        clean_entries[16][i] = value[0:4]


    #print clean_entries[4]


    # after reading all the information for all bib items, and having 
    # stored it in the table we clean the bib cite key items
    for i in range(nbcols):    
        try:
            clean_entries[1][i] = cleanBibCiteKey(clean_entries[1][i], clean_entries[2][i], 
                                                  clean_entries[4][i], clean_entries[16][i])
        except IndexError: # except "when the computer cannot find an author", then do:
            try:
                clean_entries[1][i] = cleanBibCiteKey(clean_entries[1][i], clean_entries[3][i], 
                                                      clean_entries[4][i], clean_entries[16][i])
            except IndexError: # except "when the computer cannot find an editor", then do:
                clean_entries[1][i] = cleanBibCiteKey(clean_entries[1][i], clean_entries[7][i], 
                                                      clean_entries[4][i], clean_entries[16][i])


    # after cleaning the reference table entirely, we print warning messages to
    # the user about invalid reference items
    if len(invalid_refs)>0: 
        print 'User modifications needed:'
        for ref_nb, message, ref_item in invalid_refs:
            print 'WARNING! %20s : %s (%s)'%(clean_entries[1][ref_nb], message, ref_item) 

    # clean the ref_items and store them into out matrix
    #clean_entries[column,:] = clean_bib(list_ref_items)
    # ---------------- we exit the loop on bib entries ---------------------


    # Finally: remove duplicates from matrix

    # sort alphabetically

    # check for gaps:
    # if something is missing (e.g. an author for an article?) then warn the user to add it

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

#===============================================================================
def cleanPages(pages, ref_nb, ref_type):
#===============================================================================
    
    # 1- cleaning:
    # ------------
    invalidPages = False
    # replace single '-' by double '--'
    if '--' not in pages and '-' in pages:
        pages = pages.replace('-','--')
    # strip empty spaces around '--' when relevant
    if '--' in pages:
        pp = pages.split('--')
        if len(pp)==2:
            pp[0] = pp[0].strip(' ')
            pp[1] = pp[1].strip(' ')
            # if a page bound is missing: invalid format error
            if pp[0]=='' or pp[1]=='': invalidPages
            pages = pp[0]+'--'+pp[1]
        # if we have more than one '--': invalid format error
        else:
            invalidPages = True

    # final search for unauthorized characters in the pages string:
    # we allow only '--' and numerical characters (no puntuation, no letters)
    import string
    unauthorized_chars = string.punctuation + string.ascii_letters
    unauthorized_chars = unauthorized_chars.replace('-','') # remove '-' from list of unauthorized characters
    for char in repr(pages).strip("'"): # to ba able to detect encoding of strange characters
        if char in unauthorized_chars: invalidPages = True; break
    
    # 2- return clean item, and error message if needed
    # -------------------------------------------------
    # return error if the ref item is not provided but is compulsory for a certain bib type
    if (pages == '') and (ref_type == 'article' or ref_type == 'inbook'):
        return pages, (ref_nb, 'missing pages', pages)

    # return error if the item contains unauthorized characters
    elif invalidPages==True:
        return pages, (ref_nb, 'invalid pages', pages)

    # in all other cases, return no error
    else:
        return pages, None

#===============================================================================
def cleanNumber(number, ref_nb, ref_type):
#===============================================================================
    
    # 1- cleaning:
    # ------------
    # ? signs appear to occur instead of - 
    number = number.replace('?','--')
    # replace single '-' by double '--'
    if '--' not in number and '-' in number:
        number = number.replace('-','--')
    # in case of double '--', check if bound by two numbers always
    invalidNumber = False
    if '--' in number:
        bounds = number.split('--')
        if bounds[0]=='' or bounds[1]=='': invalidNumber = True

    # final search for unauthorized characters in the number string:
    # we allow only '--' punctuation characters
    import string
    unauthorized_chars = string.punctuation
    unauthorized_chars = unauthorized_chars.replace('-','') # remove '-' from list of unauthorized characters
    for char in repr(number).strip("'"): # to ba able to detect encoding of strange characters
        if char in unauthorized_chars: invalidNumber = True; break
    
    # 2- return clean item, and error message if needed
    # -------------------------------------------------
    # return an error if the number is not provided for an article
    if (number == '') and (ref_type == 'article'):
        return number, (ref_nb, 'missing issue number of article', number)

    # return error if the item contains unauthorized punctuation (only '--' allowed)
    elif invalidNumber==True:
        return number, (ref_nb, 'invalid issue number', number)

    # in all other cases, return no error
    else:
        return number, None

#===============================================================================
def cleanVolume(volume, ref_nb, ref_type):
#===============================================================================
    
    # 1- cleaning:
    # ------------
    # ? signs appear to occur instead of - 
    volume = volume.replace('?','--')
    # replace single '-' by double '--'
    if '--' not in volume and '-' in volume:
        volume = volume.replace('-','--')
    # in case of double '--', check if bound by two numbers always
    invalidVolume = False
    if '--' in volume:
        bounds = volume.split('--')
        if bounds[0]=='' or bounds[1]=='': invalidVolume = True
 
    # final search for unauthorized characters in the number string:
    # we allow only '--' punctuation characters
    import string
    unauthorized_chars = string.punctuation
    unauthorized_chars = unauthorized_chars.replace('-','') # remove '-' from list of unauthorized characters
    for char in repr(volume).strip("'"): # to ba able to detect encoding of strange characters
        if char in unauthorized_chars: invalidVolume = True; break
    
    # 2- return clean item, and error message if needed
    # -------------------------------------------------
    # return no error if the volume is not provided in case of an article
    if (volume=='') and (ref_type == 'article'):
        return volume, (ref_nb, 'missing volume of article', volume)

    # return error if the item contains unauthorized punctuation (only '--' allowed)
    elif invalidVolume==True:
        return volume, (ref_nb, 'invalid volume', volume)

    # in all other cases, return no error
    else:
        return volume, None

#===============================================================================
def cleanBibCiteKey(key, listAuthors, title, year):
#===============================================================================
    
    # compare the original key to the list of authors
    common_sub = list(lcs(key.lower(), listAuthors.lower()))
    
    # create a clean key with the year
    startTitle  = title.split(' ')[0].strip('{{').lower()[:5].strip('-')
    clean_key_D = str(common_sub[0]) + '%s'%str(year)[2:4] + startTitle 
    clean_key_M = str(common_sub[0]) + ':%s'%year
    
    return clean_key_D

#===============================================================================
def lcs(S,T):
#===============================================================================
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set

#===============================================================================
def cleanName(name, ref_nb, ref_type):
#===============================================================================

    # define individual names by splitting them via 'and' separator
    #authors = name.lower().split(' and ')
    substrings = re.split(r'(?u)(?![\,\.,])\W+',name)
    substrings = [sub.lower() for sub in substrings]
    for i,sub in enumerate(substrings):
        if (len(sub) > 1 and sub != 'and' and '.' not in sub):
            sub = sub[0].upper() + sub[1:]
        elif (len(sub) > 1 and sub != 'and' and '.' in sub):
            sub = sub.upper()
            if not sub.endswith('.') and not sub.endswith(','): sub = sub + '.'

        elif (len(sub) == 1 and sub != 'and'):
            sub = sub.upper() + '.'
        substrings[i] = sub

    author_list = substrings[0]
    for i,string in enumerate(substrings[1:]):
        if string.endswith('.') and substrings[i-1].endswith('.'):
            author_list += string
        else:
            author_list += ' ' + string


#    # attach the {}'s and the comma, so we don't have to worry later on
#    name = '{' + name + '},'

    # check for invalid format:
    invalidName = False
    # author_list is invalid if there is a missing parenthesis in the final string
    for par1, par2 in zip('({[',')}]'):
        tt1 = author_list.split(par1)
        tt2 = author_list.split(par2)
        if len(tt1) != len(tt2): invalidName = True


    # return error if the item is invalid
    if invalidName==True:
        return author_list, (ref_nb, 'invalid author list', author_list)

    # in all other cases, return no error
    else:
        return author_list, None


#===============================================================================
def cleanTitle(title, ref_nb, ref_type):
#===============================================================================

    # split the title into its words, and check if they all with with capitals
    title_words = title.split(' ')

    for word in title_words:
        if word[0] == word[0].upper():
            all_first_cap = True
        else:
            all_first_cap = False
            break

    # convert the title to lower cases if we detect all words start with capitals
    if all_first_cap == True or title == title.lower():
        title = title.lower()

    # make the first letter Capital and add {{}} to force bibtex to read "as is"
    title = title[0].upper() + title[1:]
    title = '{{' + title + '}},'

    # check for invalid format:
    invalidTitle = False
    # title is invalid if there is a missing parenthesis in the final string
    for par1, par2 in zip('({[',')}]'):
        tt1 = title.split(par1)
        tt2 = title.split(par2)
        if len(tt1) != len(tt2): invalidTitle = True


    # return error if the item is invalid
    if invalidTitle==True:
        return title, (ref_nb, 'invalid title', title)

    # in all other cases, return no error
    else:
        return title, None


#===============================================================================
#value in key 'booktitle' has the same structure needs than value in key 'title'
#===============================================================================



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
