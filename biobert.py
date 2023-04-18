from bert_similarities import get_bert_based_similarity
from transformers import AutoTokenizer, AutoModel

sentence_pairs = {
        'similar': ['AAA', 
                    'Abdominal Aortic Aneurysm'],
        'disimilar': ['Nicotine or alcohol dependence', 
                    'patient has no smoking history']}

def getSimiliarity(sentence_pairs):
    bio_bert_model = AutoModel.from_pretrained('dmis-lab/biobert-v1.1')
    bio_bert_tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-v1.1')
    return (get_bert_based_similarity(sentence_pairs, bio_bert_model, bio_bert_tokenizer))


if __name__ == "__main__":
    print(getSimiliarity(sentence_pairs))