import numpy as np

from numpy import dot
from numpy.linalg import norm
from transformers import AutoTokenizer, AutoModel


def get_bert_based_similarity(sentence_pairs, model, tokenizer):
    """
    Computes the embeddings of each sentence and its similarity with its corresponding pair
    Args:
        sentence_pairs(dict): dictionary of lists with the similarity type as key and a list of two sentences as value
        model: the language model
        tokenizer: the tokenizer to consider for the computation
    
    Returns:
        similarities(dict): dictionary with similarity type as key and the similarity measure as value
    """

    similarity = np.float32()
    for sent_pair in sentence_pairs.items():
        print(sent_pair)
        print(sent_pair[1])
        inputs_1 = tokenizer(sent_pair[1][0], return_tensors='pt')
        inputs_2 = tokenizer(sent_pair[1][1], return_tensors='pt')
        sent_1_embed = np.mean(model(**inputs_1).last_hidden_state[0].detach().numpy(), axis=0)
        sent_2_embed = np.mean(model(**inputs_2).last_hidden_state[0].detach().numpy(), axis=0)
        similarity = dot(sent_1_embed, sent_2_embed) / (norm(sent_1_embed) * norm(sent_2_embed))
    return similarity