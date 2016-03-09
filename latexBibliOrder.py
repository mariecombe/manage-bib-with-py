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

import sys, os, glob, re, string
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
                    key = stuff.split('=')[0].strip(' ').strip('"').strip('{').strip('}').strip('\t').strip(' ')
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
                    if key=='chapter':     clean_entries[6][i] = value
                    if key=='institution': clean_entries[7][i] = value
                    if key=='school':      clean_entries[8][i] = value
                    if key=='journal':     clean_entries[9][i] = value

                    '''
                    if key=='chapter':
                        chapter = cleanChapter(value, i, bib_type)
                        clean_entries[6][i] = chapter[0]
                        if chapter[1]!=None: invalid_refs += [chapter[1]] # When an invalid error is detected in chapter

                    if key=='institution':
                        institution = cleanInstitution(value, i, bib_type)
                        clean_entries[7][i] = institution[0]
                        if institution[1]!=None: invalid_refs += [institution[1]] # When an invalid error is detected in institution
                        #NB: we want the key to match the insitution, in case of "misc" references

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



    #---------------- WARNING THE USER ABOUT MISTAKES AND GAPS -----------------

    # if entries with errors were detected during the cleaning
    if len(invalid_refs)>0:
        # we print warning messages for the user to take action
        print '\nUser modifications required:'
        for bibitem_nb, error_message, clean_value in invalid_refs:
            cite_key = clean_entries[1][bibitem_nb]
            print 'WARNING! %20s : %s '%(cite_key, error_message) +\
            '(%s)'%clean_value.strip(',').strip('{').strip('}')

    # check for gaps:
    gaps_info = []
    for i,cite_key in enumerate(clean_entries[1]):
        bib_entry = retrieve_entry(clean_entries, i)
        gaps_info += check_gaps(bib_entry)

    # if entries with gaps were detected
    if len(gaps_info)>0:
        # we print warning messages for the user to take action
        print '\nGap-filling required:'
        for cite_key, gap_message in gaps_info:
            print 'GAPS!    %20s : %s '%(cite_key, gap_message)

    #------------------- FINISHING TO CLEAN THE CITE KEYS ----------------------

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


    # let's assign a letter to the keys when same author has published few times in
    # the same year
    duplicate_positions = dict()
    for i,key in enumerate(clean_entries[1]):

        # initialize some variables
        listEqualRef = []
        alphabet = string.ascii_lowercase
        pos_duplicates = []

        # we loop over all possible cite_keys from all files
        for position,k in enumerate(clean_entries[1]):

            # if we find other references with the same author and year as our 
            # entry, we add it to a list
            if k == key: 
                title = clean_entries[4][position].lower()
                listEqualRef += [[k, position, title, False]]

        # we sort the list in alphabetical order using the lower case titles
        listEqualRef = sorted(listEqualRef, key=itemgetter(2))

        # if the reference is a duplicate, we modify its 'duplicate' flag to 'True'
        for r,ref in enumerate(listEqualRef):
            other_titles = [item[2] for x,item in enumerate(listEqualRef) if x!=r]
            if ref[2] in other_titles:
                listEqualRef[r][3] = True
                # if not already done, we append the duplicate position to a list
                if ref[1] not in pos_duplicates:
                    pos_duplicates += [listEqualRef[r][1]]

        # we append a letter to the cite_keys with same author and year if 
        # there is more than one unique publication for that author x year
        unique_titles = set([r[2] for r in listEqualRef])
        if len(unique_titles) > 1:
            counter = -1
            for k,pos,tit,dup in listEqualRef:
                if dup==False: counter += 1 
                clean_entries[1][pos] = k + alphabet[counter]
                #print clean_entries[1][pos], tit

        # we store the duplicate entries position in a dictionary for later use
        duplicate_positions[clean_entries[1][i]] = pos_duplicates
    
    #---------------------------------------------------------------------------

    # we translate the table of entries into a list of entries, in order to
    # 1- merge the duplicate bib entries
    # 2- sort references alphabetically

    # we initialize the final list
    sorted_refs = []

    # we loop over all bib entries:
    for i,cite_key in enumerate(clean_entries[1]):

        # if the reference is not already stored in the final list:
        if cite_key not in [k[1] for k in sorted_refs]:

            # if there are duplicates for that cite_key, we store the merged 
            # information from all duplicates
            if duplicate_positions[cite_key] != []:
                positions = duplicate_positions[cite_key]
                duplicate_entries = [retrieve_entry(clean_entries,p) for p in positions]
                best_entry = merge_entries(duplicate_entries)
                sorted_refs += [best_entry]
                print '\nWARNING: We merged %i duplicate entries for %s'%(len(positions),cite_key)

            # else, we store the information as is
            else:
                sorted_refs += [retrieve_entry(clean_entries, i)]

    # we sort the list of bib entries using the unique cite_keys:
    sorted_refs = sorted(sorted_refs, key=itemgetter(1))
    #print [r[1] for r in sorted_refs]

    #---------------------------------------------------------------------------

    # initialize an output file, which will be stored in the 'output' folder

    #res = open('test.txt','wb')
    #for stuff in bib_items:
    #    res.write(stuff)
    #res.close()


    # write clean bib_items to the master.bib file:
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

    #print key, listAuthors, year
    # compare the original key to the list of authors
    common_sub = list(lcs(key.lower(), listAuthors.lower()))
    cs = str(common_sub[0]).strip('?').strip(',').strip('.').strip(':').strip(';').strip(' ')

    # create a clean key with the year
    startTitle  = title.split(' ')[0].strip('{{').lower()[:5].strip('-')
    clean_key_D = cs + '%s'%str(year).strip('{').strip('}')[2:4]
    clean_key_M = cs + ':%s'%year

    return clean_key_D

#===============================================================================
def assignLetter(key, list_of_keys):
#===============================================================================

    return None

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
def check_gaps(bib_entry):
#===============================================================================
    bib_type = bib_entry[0]
    cite_key = bib_entry[1]

    # we initialize the error message list
    entry_gaps = []

    # for all articles:
    if bib_type == 'article':
        if bib_entry[2] == '': entry_gaps += [(cite_key, 'Missing author of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[9] == '': entry_gaps += [(cite_key, 'Missing journal of %s'%bib_type)]
        #if bib_entry[10] == '': entry_gaps += [(cite_key, 'Missing volume of %s'%bib_type)]
        #if bib_entry[12] == '': entry_gaps += [(cite_key, 'Missing pages of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]

    # for all books:
    elif bib_type == 'book':
        if (bib_entry[2] == '') and (bib_entry[3] == ''): 
            entry_gaps += [(cite_key, 'Missing author OR editor of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]
        #if bib_entry[17] == '': entry_gaps += [(cite_key, 'Missing publisher of %s'%bib_type)]

    # for all booklets:
    elif bib_type == 'booklet':
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]

    # for all book chapters without their own titles:
    elif bib_type == 'inbook':
        if (bib_entry[2] == '') and (bib_entry[3] == ''): 
            entry_gaps += [(cite_key, 'Missing author OR editor of %s'%bib_type)]
        if (bib_entry[6] == '') and (bib_entry[12]==''): 
            entry_gaps += [(cite_key, 'Missing book chapter OR pages of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]
        #if bib_entry[17] == '': entry_gaps += [(cite_key, 'Missing publisher of %s'%bib_type)]

    # for all book chapters with their own title:
    elif bib_type == 'incollection':
        if bib_entry[2] == '': entry_gaps += [(cite_key, 'Missing author of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[5] == '': entry_gaps += [(cite_key, 'Missing book title of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]
        #if bib_entry[17] == '': entry_gaps += [(cite_key, 'Missing publisher of %s'%bib_type)]

    # for all articles of a conference proceedings:
    elif bib_type == 'inproceedings':
        if bib_entry[2] == '': entry_gaps += [(cite_key, 'Missing author of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[5] == '': entry_gaps += [(cite_key, 'Missing book title of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]

    # for all manuals:
    elif bib_type == 'manual':
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]

    # for all MSc or PhD theses:
    elif bib_type == 'mastersthesis' or bib_type == 'phdthesis':
        if bib_entry[2] == '': entry_gaps += [(cite_key, 'Missing author of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[8] == '': entry_gaps += [(cite_key, 'Missing school of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]

    # for other kind of publication (websites, databases, maps, etc):
    elif bib_type == 'misc':
        if bib_entry[13] == '': entry_gaps += [(cite_key, 'Missing note of %s'%bib_type)]

    # for an entire proceedings of a conference:
    elif bib_type == 'proceedings':
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]

    # for all technical reports from educational, commercial or 
    # standardization institution:
    elif bib_type == 'techreport':
        if bib_entry[2] == '': entry_gaps += [(cite_key, 'Missing author of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[7] == '': entry_gaps += [(cite_key, 'Missing institution of %s'%bib_type)]
        if bib_entry[16] == '': entry_gaps += [(cite_key, 'Missing year of %s'%bib_type)]

    # for all unpublished articles/books/theses, etc:
    elif bib_type == 'unpublished':
        if bib_entry[2] == '': entry_gaps += [(cite_key, 'Missing author of %s'%bib_type)]
        if bib_entry[4] == '': entry_gaps += [(cite_key, 'Missing title of %s'%bib_type)]
        if bib_entry[13] == '': entry_gaps += [(cite_key, 'Missing note of %s'%bib_type)]

    # for wrong types:
    else:
        entry_gaps += [(cite_key, 'Wrong reference type: %s'%bib_type)]

    return entry_gaps

#===============================================================================
def merge_entries(list_of_entries):
#===============================================================================
    new_ref_type     = ''
    new_cite_key     = ''
    new_author       = ''
    new_editor       = ''
    new_title        = ''
    new_booktitle    = ''
    new_chapter      = ''
    new_institution  = ''
    new_school       = ''
    new_journal      = ''
    new_volume       = ''
    new_number       = ''
    new_pages        = ''
    new_note         = ''
    new_url          = ''
    new_doi          = ''
    new_year         = ''

    for entry in list_of_entries:
        if len(new_ref_type   ) < len(entry[0] ): new_ref_type    = entry[0]
        if len(new_cite_key   ) < len(entry[1] ): new_cite_key    = entry[1]
        if len(new_author     ) < len(entry[2] ): new_author      = entry[2]
        if len(new_editor     ) < len(entry[3] ): new_editor      = entry[3]
        if len(new_title      ) < len(entry[4] ): new_title       = entry[4]
        if len(new_booktitle  ) < len(entry[5] ): new_booktitle   = entry[5]
        if len(new_chapter    ) < len(entry[6] ): new_chapter     = entry[6]
        if len(new_institution) < len(entry[7] ): new_institution = entry[7]
        if len(new_school     ) < len(entry[8] ): new_school      = entry[8]
        if len(new_journal    ) < len(entry[9] ): new_journal     = entry[9]
        if len(new_volume     ) < len(entry[10]): new_volume      = entry[10]
        if len(new_number     ) < len(entry[11]): new_number      = entry[11]
        if len(new_pages      ) < len(entry[12]): new_pages       = entry[12]
        if len(new_note       ) < len(entry[13]): new_note        = entry[13]
        if len(new_url        ) < len(entry[14]): new_url         = entry[14]
        if len(new_doi        ) < len(entry[15]): new_doi         = entry[15]
        if len(new_year       ) < len(entry[16]): new_year        = entry[16]

    return (new_ref_type,
            new_cite_key,
            new_author,
            new_editor,
            new_title,
            new_booktitle,
            new_chapter,
            new_institution,
            new_school,
            new_journal,
            new_volume,
            new_number,
            new_pages,
            new_note,
            new_url,
            new_doi,
            new_year       
            )              
                           
#===============================================================================
def retrieve_entry(clean_entries, pos):
#===============================================================================
    return (clean_entries[0][pos],    # ref_type
            clean_entries[1][pos],    # cite_key
            clean_entries[2][pos],    # author
            clean_entries[3][pos],    # editor
            clean_entries[4][pos],    # title
            clean_entries[5][pos],    # booktitle
            clean_entries[6][pos],    # chapter
            clean_entries[7][pos],    # institution
            clean_entries[8][pos],    # school
            clean_entries[9][pos],    # journal
            clean_entries[10][pos],   # volume
            clean_entries[11][pos],   # number
            clean_entries[12][pos],   # pages
            clean_entries[13][pos],   # note
            clean_entries[14][pos],   # url
            clean_entries[15][pos],   # doi
            clean_entries[16][pos]    # year
            )

#===============================================================================
if __name__=='__main__':
    main()
#===============================================================================

"""
I don't know how difficult would this be, but... what about warning if it finds
entries that have largely coincidental strings, i.e., duplicates but that have
mistakes on them, that a super thorough examination (one to one) won't detect.

"""
