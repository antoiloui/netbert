import numpy as np
import pandas as pd
import json
import spacy, en_core_web_sm
from tqdm import tqdm
tqdm.pandas()


def sent_segmentation(doc_text):
    """
    Given a string, segment it by sentences.
    """
    nlp = en_core_web_sm.load()
    doc = nlp(doc_text)
    sentences = list(doc.sents)
    return [sent.text for sent in sentences]


def sent_cleaning(list_sent):
    """
    """
    # If line begins with a number, remove the number   
    list_sent = [sent.split(maxsplit=1)[1] if (sent.split(maxsplit=1)[0].isdigit() and len(sent.split(maxsplit=1)) > 1) else sent for sent in list_sent]
    
    # If line begins with a special char, remove that char
    spec_char = set(',?;.:/=+%`¨^*$€-_())°!§\'\"&@#~®†ºπ‡¬≈©◊~∞µ…÷≠<>')
    list_sent = [sent.split(maxsplit=1)[1] if (len(sent.split(maxsplit=1)) > 1 and sent[0] in spec_char) else sent for sent in list_sent]
    

    # Keep only sentences that have less that 15 special characters
    list_sent = [sent for sent in list_sent if max([sent.count(c) for c in spec_char]) < 15]

    # Keep only sentences with more than 2 words
    list_sent = [sent for sent in list_sent if len(sent.split()) > 2]
    return list_sent


def sent_convert(list_sent):
    """
    Given a list of string sentences, return one unique string where
    sentences are separated by newlines.
    """
    return "\n".join(list_sent)   



if __name__ == "__main__":
    # Load data and create dataframe
    rows = []
    for id_file in range(1, 14):
        file_path = "./../Data/Original_data/" + str(id_file) + ".json"

        with open(file_path) as f:
            print("Loading file {}...".format(id_file))
            data = json.load(f)  # data is a list of dict of the form: {'text':['...'], 'uri':['...']}

            print("Extracting text from {} documents in file...".format(len(data), id_file))
            for i, doc in enumerate(data):
                text = doc.get('text') # Get the text of the current doc
                if text is not None:
                    row_dict = {'Text': text[0]}
                    rows.append(row_dict)
    
    print("Creating dataframe...")
    df = pd.DataFrame(rows)
    
    # Clean corpus
    df.Text = df.Text.replace('\s+', ' ', regex=True)  # Remove duplicate spaces
    df.Text = df.Text.str.encode('ascii', 'ignore').str.decode('utf-8')   # Encode in ascii to remove weird characters such as \uf0a7
    df.Text = df.Text.str.lower()  # Lower case all strings (I have noticed a better segmentation by doing that)
    
    # Apply all functions
    print("Segmenting sentences...")
    df['Text'] = df['Text'].progress_apply(sent_segmentation)
    print("Cleaning sentences...")
    df['Text'] = df['Text'].progress_apply(sent_cleaning)
    print("Concatenating all sentences...")
    df['Text'] = df['Text'].progress_apply(sent_convert)
    
    # Concatenate sentences and save as txt file
    final_text = "\n\n".join(df["Text"])
    with open("../Data/output.txt", "w+") as f:
        f.write(final_text)
    print("DONE !")