import numpy as np
import sent2vec

from numpy import dot
from numpy.linalg import norm


def get_biosentvec_similarity(sentence_pairs):
    """
    computes the embeddings of each sentence and its similarity with its corresponding pair

    Args:
    sentence_pairs(dict): dictionary of lists with the similarity type as key and a list of two sentences as value

    Returns:
    similarities(dict): dictionary with similarity type as key and the similarity measure as value
    """
    similarities = dict()
    for sim_type, sent_pair in sentence_pairs.items():
        inputs_1 = sent_pair[0]
        inputs_2 = sent_pair[1]
        sent_1_embed = model.embed_sentence(inputs_1)
        sent_2_embed = model.embed_sentence(inputs_2)
        similarities[sim_type] = dot(np.squeeze(sent_1_embed), np.squeeze(sent_2_embed)) / (norm(sent_1_embed) * norm(sent_2_embed))
    return similarities


if __name__ == "__main__":
    sentence_pairs = {
        'similar': 
            ['nicotine', 
            'smoking'],
        'disimilar': 
            ['Nicotine or alcohol dependence', 
            'no history of nicotine use']
    }

    model = sent2vec.Sent2vecModel()
    model.load_model('./models/BioSentVec_PubMed_MIMICIII-bigram_d700.bin')
    print(get_biosentvec_similarity(sentence_pairs))