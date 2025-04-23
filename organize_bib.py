import bibtexparser
import re

def smart_title(text):
    exceptions = {'a', 'an', 'and', 'at', 'but', 'by', 'for', 'in', 'nor', 
                  'of', 'on', 'or', 'so', 'the', 'to', 'up', 'with', 'yet'}
    
    words = text.split()
    result = []

    for i, word in enumerate(words):
        word_clean = word.lower()
        if i == 0 or word_clean not in exceptions:
            # Capitalize only the first letter, keep rest as-is
            if len(word) > 1:
                result.append(word[0].upper() + word[1:])
            else:
                result.append(word.upper())
        else:
            result.append(word_clean)
    
    return ' '.join(result)


def modify_bib_entry(entry):
    """
    Modify a given BibTeX entry (dictionary format). 
    Example: Modify 'title' field by formatting formulas properly.
    """
    if 'title' in entry:
        entry['title'] = entry['title'].replace('$', r'\(').replace('$', r'\)')
    new_entry = {}


    if entry['ENTRYTYPE'] == 'inproceedings':
        if 'booktitle' in entry:
            new_entry['journal'] = entry['booktitle']
        elif 'journal' in entry:
            new_entry['journal'] = entry['journal']
        else:
            print("No booktitle for")
            print(entry)
    elif entry['ENTRYTYPE'] == 'inproceedings':
        new_entry['journal'] = entry['journal']
    else:
        new_entry = entry

    new_entry['ID'] = entry['ID']
    new_entry['ENTRYTYPE'] = 'article'
    title = entry['title']
    new_entry['title'] = smart_title(title)
    if new_entry['title'][0] != '{':
        new_entry['title'] = '{' + new_entry['title'] + '}'
        new_entry['author'] = entry['author']

    publisher = None
    if 'publisher' in entry:
        publisher = entry['publisher']
    elif 'organization' in entry:
        publisher = entry['organization']
    list_short = ['ICRA', 
                  'IROS', 
                  'ICCV', 
                  'ECCV', 
                  'CVPR']
    list_long = ['international conference on robotics and automation',
                 'international conference on intelligent robots and systems',
                 'international conference on computer vision',
                 'european conference on computer vision',
                 'computer vision and pattern recognition']
    list_full = ['IEEE International Conference on Robotics and Automation (ICRA)',
                 'IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)',
                 'IEEE International Conference on Computer Vision (ICCV)',
                 'IEEE European Conference on Computer Vision (ECCV)',
                 'IEEE Conference on Computer Vision and Pattern Recognition (CVPR)']
    list_publisher = ['IEEE', 
                      'IEEE', 
                      'IEEE', 
                      'IEEE', 
                      'IEEE']
    if 'journal' in new_entry.keys():
        for i, short_name in enumerate(list_short):
            long_name = list_long[i]
            if short_name in new_entry['journal'] or long_name.lower() in new_entry['journal'] :
                publisher == list_publisher[i]
                new_entry['journal'] = list_full[i]
        if 'arxiv' in new_entry['journal'].lower():
            print(new_entry['title'], "is an arxiv paper.")
        if publisher is not None:
            if 'Conference' in new_entry['journal']:
                new_entry['organization'] = publisher
            else:
                new_entry['organization'] = publisher
    else:
        print(new_entry['title'], " has no journal.")
        

    if 'pages' in entry:
        new_entry['pages'] = entry['pages']

    if 'year' in entry:
        new_entry['year'] = entry['year']
    else:
        pattern = r"\b(1[0-9]{3}|20[0-9]{2})\b"
        if 'journal' in new_entry.keys():
            match = re.search(pattern, new_entry['journal'])
            if match:
                new_entry['year'] = match.group()
    if 'volume' in entry:
        new_entry['volume'] = entry['volume']
    # if 'journal' in new_entry.keys():
        # new_entry['journal'] = '{' + new_entry['journal'] + '}'

    return new_entry

def process_bib_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    entry_dict = {}
    # Modify each entry
    for entry in bib_database.entries:
        new_entry = modify_bib_entry(entry)
        entry_dict[new_entry['ID']] = new_entry
    bib_database.entries = list(entry_dict.values())

    # Write the cleaned-up BibTeX file
    with open(output_file, 'w', encoding='utf-8') as bib_file:
        bibtexparser.dump(bib_database, bib_file)

# Example usage
process_bib_file('myrefs.bib', 'myrefs2.bib')

