import bibtexparser
import re

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
        return entry

    new_entry['ID'] = entry['ID']
    new_entry['ENTRYTYPE'] = 'article'
    title = entry['title']
    new_entry['title'] = f"{{{title}}}"
    new_entry['author'] = entry['author']

    publisher = None
    if 'publisher' in entry:
        publisher = entry['publisher']
    elif 'organization' in entry:
        publisher = entry['organization']

    if 'ICRA' in new_entry['journal'] or 'IROS' in new_entry['journal'] :
        publisher == 'IEEE'
    if publisher is not None:
        if 'Conference' in new_entry['journal']:
            new_entry['organization'] = publisher
        else:
            new_entry['organization'] = publisher

    if 'pages' in entry:
        new_entry['pages'] = entry['pages']

    if 'year' in entry:
        new_entry['year'] = entry['year']
    else:
        pattern = r"\b(1[0-9]{3}|20[0-9]{2})\b"
        match = re.search(pattern, new_entry['journal'])
        if match:
            new_entry['year'] = match.group()
    if 'volume' in entry:
        new_entry['volume'] = entry['volume']


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
