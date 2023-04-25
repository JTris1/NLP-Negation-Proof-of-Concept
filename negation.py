# TODO: figure out how to make the negation detection useful for our case.
# We want negation to be able to check if the term we are processing is negative. If so, we want to skip it.
# We should use 'neg_model2' because it incorporates the negative terms absent, not, etc.

# TODO: Consider what terms would be useful for the db, if any. If we are checking just single words or concepts, do we need custom preceding and following negations?
# Custom negations seem to be useful for a patient's chart. But if we are checking pre-formatted data in a database it may not be needed.


import spacy
import scispacy
from spacy import displacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from spacy.strings import StringStore
from negspacy.negation import Negex
from negspacy.termsets import termset

nlp0 = spacy.load("en_core_sci_sm")
nlp1 = spacy.load("en_ner_bc5cdr_md")

# clinical_note = "Patient resting in bed. Patient given azithromycin without any difficulty. Patient has audible wheezing, states chest tightness. No evidence of hypertension. Patient denies nausea at this time. zofran declined. Patient is also having intermittent sweating associated with pneumonia. Patient refused pain but tylenol still given. Neither substance abuse nor alcohol use however cocaine once used in the last year. Alcoholism unlikely. Patient has headache and fever. Patient is not diabetic. No signs of diarrhea. Lab reports confirm lymphocytopenia. Cardaic rhythm is Sinus bradycardia. Patient also has a history of cardiac injury. No kidney injury reported. No abnormal rashes or ulcers. Patient might not have liver disease. Confirmed absence of hemoptysis. Although patient has severe pneumonia and fever, test reports are negative for COVID-19 infection. COVID-19 viral infection absent."
## clinical_note = "RECOMMENDATIONS The USPSTF recommends 1-time screening for abdominal aortic aneurysm with ultrasonography in men aged 65 to 75 years who have ever smoked. (B recommendation) The USPSTF recommends that clinicians selectively offer screening for abdominal aortic aneurysm with ultrasonography in men aged 65 to 75 years who have never smoked rather than routinely screening all men in this group."

# lemmatizing the notes to capture all forms of negation(e.g., deny: denies, denying)
def lemmatize(note, nlp):
    doc = nlp(note)
    lemNote = [wd.lemma_ for wd in doc]
    return " ".join(lemNote)

## lem_clinical_note = lemmatize(clinical_note, nlp0)

# print(lem_clinical_note)

# Creating a doc object using BC5CDR model
# doc = nlp1(lem_clinical_note);
## doc = nlp1(lem_clinical_note)


# modify options for displacy NER visualization
def get_entity_options():
    entities = ["DISEASE", "CHEMICAL", "NEG_ENTITY"]
    colors = {'DISEASE': 'linear-gradient(180deg, #66ffcc, #abf763)', 'CHEMICAL': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', "NEG_ENTITY":'linear-gradient(90deg, #ffff66, #ff6600)'}
    options = {"ents": entities, "colors": colors}
    return options

## options = get_entity_options()


#adding a new pipeline component to identify negation
### NOTE ###
# This works, but assigns things like 'nausea, viral infection, etc' to DISEASE, not NEG_ENTITY
# See neg_model2 for the fix to this
# def neg_model(nlp_model):
#     nlp = spacy.load(nlp_model, disable=['parser'])
#     nlp.add_pipe('sentencizer')
#     nlp.add_pipe("negex")
#     return nlp

# Add pipeline component 
def neg_model2(nlp_model):
    # Add preceding and following negation terms
    # These get added to the termset 'en_clinical' which is the default for negex
    ts = termset('en_clinical')
    ts.add_patterns({
        "preceding_negations": ['deny', 'refuse', 'neither', 'nor'],
        "following_negations": ['absent', 'deny', 'decline'],
    })

    nlp = spacy.load(nlp_model, disable=['parser'])
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('negex')
    print(nlp.get_pipe_meta('negex'))

    return nlp


# Negspacy sets a new attribute e._.negex to True if a negative concept is encountered

def negation_handling(nlp_model, note, neg_model):
    results = []
    nlp = neg_model(nlp_model)
    note = note.split(".") #sentence tokenization based on delimeter

    print(note)

    note = [n.strip() for n in note] #remove extra spaces at the beg. and end of sentence

    print(note)

    for t in note:
        print()
        print(t)

        doc = nlp(t)
        # print('### t in note loop: \ndoc: ', str(doc))

        for e in doc.ents:
            rs = str(e._.negex)
            if rs == "True":
                results.append(e.text)
    return results

# list of negative concepts from clinical note identified by negspacy
# results0 = negation_handling('en_ner_bc5cdr_md', lem_clinical_note, neg_model)

# updated list of all the negative concepts from clinical note identified by negspacy
## results1 = negation_handling('en_ner_bc5cdr_md', lem_clinical_note, neg_model2)


# identify span objects of matched negative phrases from clinical note
def match(nlp, terms, label):
    patterns = [nlp.make_doc(text) for text in terms]
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add(label, None, *patterns)
    return matcher

# replace labels for identified negative entities
def overwrite_ent_label(matcher, doc):
    matches = matcher(doc)
    seen_tokens = set()
    new_entities = []
    entities = doc.ents
    for match_id, start, end in matches:
        if start not in seen_tokens and end - 1 not in seen_tokens:
            new_entities.append(Span(doc, start, end, label=match_id))
            entities = [e for e in entities if not (e.start < end and e.end > start)]
            seen_tokens.update(range(start, end))
    doc.ents = tuple(entities) + tuple(new_entities)
    return doc

# matcher = match(nlp1, results0, "NEG_ENTITY")

# Updated negations
## matcher = match(nlp1, results1, "NEG_ENTITY")

# doc0: new doc object with added NEG_ENTITY label
## doc0 = overwrite_ent_label(matcher, doc)

# doc1: new doc object with added custom concepts for "NEG_ENTITY" label
## doc1 = overwrite_ent_label(matcher, doc) 

# visualizing identified Named Entities in clinical input text
# displacy.serve(doc1, style='ent', options=options)



# Execute everything
def execNegation(text):
    lem_text = lemmatize(text, nlp1)
    doc = nlp1(lem_text)

    results = negation_handling('en_ner_bc5cdr_md', lem_text, neg_model2)

    matcher = match(nlp1, results, "NEG_ENTITY")
    doc_w_negs = overwrite_ent_label(matcher, doc)

    return doc_w_negs


execNegation('RECOMMENDATIONS The USPSTF recommends 1-time screening for abdominal aortic aneurysm with ultrasonography in men aged 65 to 75 years who have ever smoked. (B recommendation) The USPSTF recommends that clinicians selectively offer screening for abdominal aortic aneurysm with ultrasonography in men aged 65 to 75 years who have never smoked rather than routinely screening all men in this group.')