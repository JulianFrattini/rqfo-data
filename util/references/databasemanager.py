import pandas as pd

mandatory_reference_attributes = ['author', 'title']

dbpath = 'util/references/references.csv'
df = pd.read_csv(dbpath, sep=',').set_index('id')

def get_next_id():
    taken = list(df.index)
    return max(taken)+1

def add_reference(reference):
    global df

    # ensure that all mandatory reference attributes are contained
    for att in mandatory_reference_attributes:
        if att not in reference.keys() or not reference[att]:
            return False

    # ensure that this entry has not already been added
    if get_reference_id(reference):
        return False

    # add a new row to the dataframe containing the new reference
    ref = pd.DataFrame.from_records([{
        'id': get_next_id(),
        'author': reference['author'],
        'title': reference['title'],
        'refstring': reference['refstring']
        }], index='id')

    df = df.append(ref)
    df.to_csv(dbpath, sep=',')
    return True

def get_reference_id(reference):
    # find the entry with a matching author and title
    indices = df.index[(df['author']==reference['author']) & (df['title'] == reference['title'])]

    if len(indices) == 0:
        return None
    elif len(indices) == 1:
        return indices[0]
    else:
        # error: more than one entry in the database have the same author and title
        return None

if __name__ == "__main__":
    add_reference({
        "author": "Alessio Ferrari",
        "title": "Detecting requirements defects with NLP patterns: an industrial experience in the railway domain",
        "refstring": "Ferrari, A., Gori, G., Rosadini, B., Trotta, I., Bacherini, S., Fantechi, A., & Gnesi, S. (2018). Detecting requirements defects with NLP patterns: an industrial experience in the railway domain. Empirical Software Engineering, 23(6), 3684-3733."
    })
    get_reference_id({"author": "Alessio Ferrari",
        "title": "Detecting requirements defects with NLP patterns: an industrial experience in the railway domain"})