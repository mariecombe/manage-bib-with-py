#!/usr/bin/env python

"""
This program reads one or more bib file, separates its bibtex entries
and reorders its items in a designated order.

Processing include:
    -- reordering
    -- reassignation of key_name
    -- inclusion of double curly braquets in title
    -- removal of eprint, abstract, ... if any
    -- save file as latexBibliOrder.bib
    -- promp errors when invalid format (manual modifications needed)
    -- keep url for excelBibData.py
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

    ## Gets fullpath to current working directory
    ## Defines useful folder names
    cwd           = os.getcwd()
    input_folder  = os.path.join(cwd, 'bib_input_files/')
    output_folder = os.path.join(cwd, 'bib_output_file/')

    ## Lists the input .bib files to read in the input folder (two steps)
    # Defines the pattern you are looking for:
    pattern       = os.path.join(input_folder, '*.bib')
    # Creates a list of all files that fullfil this pattern
    inFileList    = glob.glob(pattern)
    #print inFileList

    # A - Warns the user
    # B - Exits the script
    if len(inFileList)==0:
        print 'there are no .bib files in folder %s' %cwd
        sys.exit()


    ### Cleans the input files

    # Initializes empty string to store clean bib_items from all files
    files_as_one_string = ''

    # ------------------------ Loops over .bib files ------------------------
    # For each input file
    for filename in inFileList:

        # Reads file content as one string and closes file
        f = open(filename, 'r') # r for read-only
        files_as_one_string += f.read()
        f.close()
    # ------------------- Exits the loop on bib files --------------------

    # Splits the contents into bib_item
    bib_separator = '@'
    bib_items     = files_as_one_string.split(bib_separator)

    # Removes the first item, which is an empty string
    del bib_items[0]

    # ----------------- Loops over unclean bib entries ----------------------

    # Initializes matrix to store the (cleaned) results
    # Ner of columns = number of bib entries
    # Ner of rows = number of ref items per bib entry
    nbcols  = len(bib_items)
    nbrows  = 17

    # Sets data type of the array to 'arbitrary object' (so the array stores strings and not floats)
    clean_entries = np.array([['']*nbcols]*nbrows, dtype=object)

    # Initiates a list of invalid bib references
    invalid_refs = list()

    # For each bib_item of complete list
    for i in range(nbcols):

        # Splits the bib_item into its ref_item (cite_key, title, ...)
        if '\r\n' in files_as_one_string:
            ref_item_separator = '\r\n'
        else:
            ref_item_separator = '\n'

        list_ref_items     = bib_items[i].split(ref_item_separator)

        # Loops the rows from the end to the start:
        for j,stuff in enumerate(list_ref_items):

            ## After detailed description of what's going on, we reach the part were things get interesting,
            ## and surprise surprise, no description!
            if j==0:
                bib_type     = stuff.split('{')[0]
                bib_cite_key = stuff.split('{')[1]
                clean_entries[0][i]   = bib_type
                clean_entries[1][i]   = bib_cite_key

            else:
                if len(stuff.split('='))==2: # if the line that is read contains useful info
                                             # i.e. if it is not a single curly bracket or empty line

                    # Separates key from value, and cleans edges by removing
                    # empty spaces, quotation marks, and curly brackets
                    key = stuff.split('=')[0].strip(' ').strip('"').strip('{').strip('}').strip(' ')
                    value  = stuff.split('=')[1].strip(',').strip(' ').strip('"').strip('{').strip('}').strip(' ')

                    if key=='author':
                        author = cleanName(value, i, bib_type)
                        clean_entries[2][i] = author[0]
                        if author[1]!=None: invalid_refs += [author[1]] # When an invalid error is detected in author

                    if key=='editor':
                        editor = cleanName(value, i, bib_type)
                        clean_entries[3][i] = editor[0]
                        if editor[1]!=None: invalid_refs += [editor[1]] # When an invalid error is detected in editor

                    if key=='title':
                        title  = cleanTitle(value, i, bib_type)
                        clean_entries[4][i] = title[0]
                        if title[1]!=None: invalid_refs += [title[1]] # When an invalid error is detected in title

                    if key=='booktitle':
                        btitle = cleanTitle(value, i, bib_type)
                        clean_entries[5][i] = btitle[0]
                        if btitle[1]!=None: invalid_refs += [btitle[1]] # When an invalid error is detected in booktitle
              '''
                    if key=='chapter':
                        chapter = cleanChapter(value, i, bib_type)
                        clean_entries[6][i] = chapter[0]
                        if chapter[1]!=None: invalid_refs += [chapter[1]] # When an invalid error is detected in chapter

                    if key=='institution':
                        institution = cleanInstitution(value, i, bib_type)
                        clean_entries[7][i] = institution[0]
                        if institution[1]!=None: invalid_refs += [institution[1]] # When an invalid error is detected in institution

                    if key=='school':
                        school = cleanSchool(value, i, bib_type)
                        clean_entries[8][i] = school[0]
                        if school[1]!=None: invalid_refs += [school[1]] # When an invalid error is detected in school

                    if key=='journal':
                        journal = cleanJournal(value, i, bib_type)
                        clean_entries[9][i] = journal[0]
                        if journal[1]!=None: invalid_refs += [journal[1]] # When an invalid error is detected in journal
              '''
                    if key=='volume':
                        volume = cleanVolume(value, i, bib_type)
                        clean_entries[10][i] = volume[0]
                        if volume[1]!=None: invalid_refs += [volume[1]] # When an invalid error is detected in volume

                    if key=='number':
                        number = cleanNumber(value, i, bib_type)
                        clean_entries[11][i] = number[0]
                        if number[1]!=None: invalid_refs += [number[1]] # When an invalid error is detected in number

                    if key=='pages':
                        pages = cleanPages(value, i, bib_type)
                        clean_entries[12][i] = pages[0]
                        if pages[1]!=None: invalid_refs += [pages[1]] # When an invalid error is detected in pages

                    if key=='note':
                        note = cleanNote(value, i, bib_type)
                        clean_entries[13][i] = note[0]
                        if note[1]!=None: invalid_refs += [note[1]] # When an invalid error is detected in note

                    if key=='url':
                        url = cleanURL(value, i, bib_type)
                        clean_entries[14][i] = url[0]
                        if url[1]!=None: invalid_refs += [url[1]] # When an invalid error is detected in URL

                    if key=='doi':
                        doi = cleanDOI(value, i, bib_type)
                        clean_entries[15][i] = doi[0]
                        if doi[1]!=None: invalid_refs += [doi[1]] # When an invalid error is detected in doi

                    if key=='year':
                        year = cleanYear(value, i, bib_type)
                        clean_entries[16][i] = year[0]
                        if year[1]!=None: invalid_refs += [year[1]] # When an invalid error is detected in year


    #print clean_entries[6]


    # after reading all the information for all bib items, and having
    # stored it in the table we clean the bib cite key items
    for i in range(nbcols):
        try:
            clean_entries[1][i] = cleanBibCiteKey(clean_entries[1][i],
                                                  clean_entries[2][i],
                                                  clean_entries[4][i],
                                                  clean_entries[16][i])
        except IndexError: # except "when the computer cannot find an author", then do:
            try:
                clean_entries[1][i] = cleanBibCiteKey(clean_entries[1][i],
                                                      clean_entries[3][i],
                                                      clean_entries[4][i],
                                                      clean_entries[16][i])
            except IndexError: # except "when the computer cannot find an editor", then do:
                clean_entries[1][i] = cleanBibCiteKey(clean_entries[1][i],
                                                      clean_entries[7][i],
                                                      clean_entries[4][i],
                                                      clean_entries[16][i])


    # if entries with errors were detected during the cleaning
    if len(invalid_refs)>0:
        # we print warning messages for the user to take action
        print 'User modifications needed:'
        for bibitem_nb, error_message, clean_value in invalid_refs:
            cite_key = clean_entries[1][bibitem_nb]
            print 'WARNING! %20s : %s '%(cite_key, error_message) +\
            '(%s)'%clean_value.strip(',').strip('{').strip('}')

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
def cleanYear(year, ref_nb, ref_type):
#===============================================================================

    # 1- cleaning:
    # ------------
    # we append one set of curly brackets around the year if non empty
    if year!='':
        year = '{' + year + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidYear = False # initialize to False

    # year is invalid if there are non-digits characters, or year length is
    # longer than 4 characters
    import string
    authorized_chars = string.digits
    for char in year.strip('{').strip('}'):
        if char not in authorized_chars: invalidYear = True
    if len(year.strip('{').strip('}'))>4: invalidYear = True

    # 3- return clean item, and error message if needed
    # -------------------------------------------------
    # return error if year is missing for 'article' bib type
    if (year == '') and (ref_type=='article'):
        return year, (ref_nb, "missing year of article", year)

    # return error if invalid year
    elif invalidYear == True:
        return year, (ref_nb, "invalid year", year)

    # in all other cases, return no error
    else:
        return year, None

#===============================================================================
def cleanDOI(doi, ref_nb, ref_type):
#===============================================================================

    # 1- cleaning:
    # ------------
    # we remove the http start where relevant
    doi = doi.replace('http://dx.doi.org/','')
    # we append one set of curly brackets around the doi if non empty
    if doi!='':
        doi = '{' + doi + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidDOI = False # initialize to False

    # DOI is invalid if there is a non-closed parenthesis in the final string
    for par1, par2 in zip('({[',')}]'):
        tt1 = doi.split(par1)
        tt2 = doi.split(par2)
        if len(tt1) != len(tt2): invalidDOI = True

    # 3- return clean item, and error message if needed
    # -------------------------------------------------
    # return error if doi is missing for 'article' bib type
    if (doi == '') and (ref_type=='article'):
        return doi, (ref_nb, "missing doi of article", doi)

    # return error if invalid doi
    elif invalidDOI == True:
        return doi, (ref_nb, "invalid doi", doi)

    # in all other cases, return no error
    else:
        return doi, None

#===============================================================================
def cleanURL(url, ref_nb, ref_type):
#===============================================================================

    # 1- cleaning:
    # ------------
    # we only want the URL to be used for websites ('misc' type), so we empty the
    # string for all other types
    if not ref_type.startswith('misc'):
        url = ''
    # we append one set of curly brackets around the URL if non empty
    if url!='':
        url = '{' + url + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidURL = False # initialize to False

    # URL should start with an 'http://' string
    if ref_type.startswith('misc') and not url.startswith('{http://'):
        invalidURL = True
    # URL is invalid if there is a parenthesis in the middle of the final string
    for char in '({[)}]':
        if char in url.strip('{').strip('}'):
            invalidURL = True


    # 3- return clean item, and error message if needed
    # -------------------------------------------------
    # return error if url is missing for 'misc' bib type
    if (url == '') and (ref_type.startswith('misc')):
        return url, (ref_nb, "missing URL for website", url)

    # return error if invalid url
    elif invalidURL == True:
        return url, (ref_nb, "invalid URL", url)

    # in all other cases, return no error
    else:
        return url, None

#===============================================================================
def cleanNote(note, ref_nb, ref_type):
#===============================================================================

    # 1- cleaning:
    # ------------
    # we only want the note used for websites ('misc type'), so we empty the
    # string for all other types
    if not ref_type.startswith('misc'):
        note = ''
    # we append one set of curly brackets around the note if non-empty
    if note!='':
        note = '{' + note + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidNote = False # initialize to False

    # note should start with a 'Last accessed on' string
    if ref_type.startswith('misc') and not note.startswith('{Last accessed on'):
        invalidNote = True


    # 2- return clean item, and error message if needed
    # -------------------------------------------------
    # return error if note is missing for 'misc' bib type
    if (note == '') and (ref_type.startswith('misc')):
        return note, (ref_nb, "missing 'Last accessed on (mon) (day), (year)'"+\
               " statement for website", note)

    # return error if invalid note
    elif invalidNote == True:
        return note, (ref_nb, "invalid 'Last accessed on (mon) (day), (year)'"+\
               " statement for website", note)

    # in all other cases, return no error
    else:
        return note, None

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
            pages = pp[0]+'--'+pp[1]
    # add a set of curly bracket around the page number(s)
    pages = '{' + pages + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidPages = False # initialize to False

    # if we have more than one page number
    if '--' in pages:
        pp = pages.split('--')
        # but if a page boundary is missing: invalid format error
        if len(pp)==2 and (pp[0]=='{' or pp[1]=='}'): invalidPages = True

        # or if we have more than one '--': invalid format error
        elif len(pp)!=2: invalidPages = True

    # we allow only '--' and digits (no puntuation, no letters, no special encoding)
    import string
    authorized_chars = string.digits + '-'
    # we check for authorized characters on the string representation (i.e. repr(string))
    # to be able to check for encoded letters and characters (they start with '\'
    # in the string representation, but not in the string itself)
    for char in repr(pages).strip("'").strip('{').strip('}'):
        if char not in authorized_chars: invalidPages = True; break

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
    # add a set of curly bracket around the issue number
    number = '{' + number + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidNumber = False # initialize to False

    # in case of double '--', check if bound by two numbers always
    if '--' in number:
        bounds = number.split('--')
        if bounds[0]=='' or bounds[1]=='': invalidNumber = True

    # final search for unauthorized characters in the number string:
    # we allow only '--' punctuation characters
    import string
    unauthorized_chars = string.punctuation
    unauthorized_chars = unauthorized_chars.replace('-','') # remove '-' from list of unauthorized characters
    for char in repr(number).strip("'").strip('{').strip('}'): # to ba able to detect encoding of strange characters
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
    # ? symbol appears to occur instead of -
    volume = volume.replace('?','--')
    # replace single '-' by double '--'
    if '--' not in volume and '-' in volume:
        volume = volume.replace('-','--')
    # add a set of curly bracket around the volume number
    volume = '{' + volume + '}'

    # 2- check for invalid format:
    # ---------------------------
    invalidVolume = False # initialize to False

    # in case of double '--', check if bound by two numbers always
    if '--' in volume:
        bounds = volume.split('--')
        if bounds[0]=='{' or bounds[1]=='}': invalidVolume = True

    # we allow only '--' punctuation characters
    import string
    unauthorized_chars = string.punctuation
    unauthorized_chars = unauthorized_chars.replace('-','')
    # we search for unauthorized characters in the 'volume' string
    for char in repr(volume).strip("'").strip('{').strip('}'):
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
I don't know how difficult would this be, but... what about warning if it finds
entries that have largely coincidental strings, i.e., duplicates but that have
mistakes on them, that a super thorough examination (one to one) won't detect.

"""
