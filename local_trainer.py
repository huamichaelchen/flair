from flair.datasets import CONLL_03
from flair.data import Corpus
from flair.embeddings import POSEmbeddings, StackedEmbeddings, WordEmbeddings, FlairEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

embedding_types = [
    [WordEmbeddings('glove_spacy100_v2/pos_embeddings_v2_100d'),],
    [WordEmbeddings('glove_spacy25_v2/pos_embeddings_v2_25d'),]
    ]

for idx, embedding_type in enumerate(embedding_types):
    for idx2 in range(3):
        corpus: Corpus = CONLL_03()

        tag_type = 'ner'

        tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

        embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_type)

        tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                                embeddings=embeddings,
                                                tag_dictionary=tag_dictionary,
                                                tag_type=tag_type,
                                                use_crf=True)

        trainer: ModelTrainer = ModelTrainer(tagger, corpus)

        trainer.train(f'resources/taggers/ner-tagger-with-pos-embeddings-v2-{idx}-run{idx2}',
                      learning_rate=0.1,
                      mini_batch_size=32,
                      max_epochs=150,
                      embeddings_storage_mode='gpu')