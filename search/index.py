import math
import redis

from tqdm import tqdm
from .timing import timing
from .analysis import analyze


class Index:
    def __init__(self, host='localhost', port=6379, db=0, batch_size=10000):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.batch_size = batch_size
        self.pipeline = self.redis.pipeline()

    def index_document(self, document):
        doc_id = document.ID
        if not self.redis.exists(doc_id):
            document.analyze()
            for token in analyze(document.fulltext):
                self.pipeline.sadd(token, doc_id)
                self.pipeline.incr(token + ':df')
            self.indexed_count += 1
            if self.indexed_count % self.batch_size == 0:
                self.pipeline.execute()

    def document_frequency(self, token):
        return int(self.redis.get(token + ':df') or 0)

    def inverse_document_frequency(self, token):
        df = self.document_frequency(token)
        return math.log10(self.redis.dbsize() / (df + 1))

    def _results(self, analyzed_query):
        return [self.redis.smembers(token) for token in analyzed_query]

    @timing
    def search(self, query, search_type='AND', rank=False):
        if search_type not in ('AND', 'OR'):
            return []

        analyzed_query = analyze(query)
        results = self._results(analyzed_query)

        if search_type == 'AND':
            documents = [doc_id.decode('utf-8') for doc_id in self.redis.sinter(*results)]
        if search_type == 'OR':
            documents = [doc_id.decode('utf-8') for doc_id in self.redis.sunion(*results)]

        if rank:
            return self.rank(analyzed_query, documents)
        return documents

    def rank(self, analyzed_query, documents):
        results = []
        if not documents:
            return results
        for doc_id in documents:
            score = 0.0
            for token in analyzed_query:
                tf = self.redis.scard(token + ':' + doc_id)
                idf = self.inverse_document_frequency(token)
                score += tf * idf
            results.append((doc_id, score))
        return sorted(results, key=lambda doc: doc[1], reverse=True)

    @timing
    def index_documents(self, documents):
        self.indexed_count = 0
        for i, document in tqdm(enumerate(documents), total=len(documents)):
            self.index_document(document)
        self.pipeline.execute()

    def close(self):
        self.redis.close()
