from django.http import HttpResponse
from django.shortcuts import render
import json
import numpy as np
from time import time
from nltk.stem.porter import PorterStemmer


stemmer= PorterStemmer()


rev_index = {
    # "apple": ["1", "2"],
    # "banana": ["3", "4", "5"]
}
docs = {
    # "1": {
    #     "title": "Apple Better Than Banana",
    #     "author": "Apple's mother",
    #     "abstract": "This is abstract",
    #     "text": "too much",
    #     "word_freq": [5, 0, 2, 8, 0]
    # },
    # "2": {
    #     "title": "Banana Better Than Apple",
    #     "author": "Banana's mother",
    #     "abstract": "This is abstract",
    #     "text": "too much",
    #     "word_freq": [2, 1, 5, 0, 0]
    # },
    # "3": {
    #     "title": "3",
    #     "author": "This is author",
    #     "abstract": "This is abstract",
    #     "text": "too much",
    #     "word_freq": [3, 1, 5, 0, 0]
    # },
    # "4": {
    #     "title": "4",
    #     "author": "This is author",
    #     "abstract": "This is abstract",
    #     "text": "too much",
    #     "word_freq": [4, 1, 5, 0, 0]
    # },
    # "5": {
    #     "title": "5",
    #     "author": "This is author",
    #     "abstract": "This is abstract",
    #     "text": "too much",
    #     "word_freq": [5, 1, 5, 0, 0]
    # }
}


vocab = {}  # {单词：{在vec中的索引值， 总文档freq_all， onehot总文档freq_onehot}}


def init_data(a=0.4, k1=1.2, b=0.75):  # 初始化函数，参数为bm25的参数
    global rev_index
    global vocab
    f_doc = open("docs/paper_index_feq.json", "r", encoding="utf-8")
    f_doc = json.load(f_doc)
    f_index = open("docs/reversed_dict.json", "r", encoding="utf-8")
    rev_index = json.load(f_index)
    f_vocab = open("docs/word_index.json", "r", encoding="utf-8")
    vocab = json.load(f_vocab)

    freq_all = []
    len_all = 0
    for doc_id, value in f_doc.items():  # 先存一遍重要信息
        docs[doc_id] = {}
        docs[doc_id]["title"] = value["title"]
        docs[doc_id]["len"] = 1000
        docs[doc_id]["word_freq"] = np.array(value["freq_v"])
        freq_all.append(value["freq_v"])
        len_all += docs[doc_id]["len"]

    freq_all = np.array(freq_all)  # 获得单词的文档频率
    freq_all_onehot = freq_all
    mask = freq_all_onehot > 0
    freq_all_onehot[mask] = 1
    freq_all_onehot_sum = np.sum(freq_all_onehot, axis=0)

    idf = np.log(len(docs)) - np.log(freq_all_onehot_sum)  # 计算每个单词的idf值
    bm25_idf = np.log(len(docs) - freq_all_onehot_sum + 0.5) - np.log(freq_all_onehot_sum + 0.5)  # 计算每个单词的idf值
    avg_len = len_all / len(docs)  # 平均长度
    for doc_id in docs.keys():  # 计算每篇文章的tf-idf / bm25_w
        docs[doc_id]["tf"] = a + (1 - a) * docs[doc_id]["word_freq"] / max(docs[doc_id]["word_freq"])  # 计算文章的tf值
        docs[doc_id]["tf_idf"] = docs[doc_id]["tf"] * idf  # 计算文章的tf_idf

        k = k1 * (1 - b) + b * docs[doc_id]["len"] / avg_len
        docs[doc_id]["bm25_w"] = bm25_idf * (k1 + 1) * docs[doc_id]["word_freq"] / (k + docs[doc_id]["word_freq"])

        docs[doc_id]["doc_sum"] = sum(docs[doc_id]["tf_idf"] ** 2)


def get_freq_vec(keys):  # 获取查询的词频向量
    vec = np.zeros(len(vocab))
    for w in keys:
        if w in vocab:
            vec[vocab[w]] = keys.count(w)
    return vec


def word2docid(key):  # 单词倒序索引至文章
    if key in rev_index:
        return rev_index[key]
    else:
        print("{} not found in vocab".format(key))
        return []


def id2doc(_id):  # 获取文章内容
    return docs[_id]


def get_doc_ids_by_index(keys):  # 获取查询的倒序索引文章
    res = []
    for key in keys:
        res.extend(word2docid(key))
    return list(set(res))


def dist_cosine(query, doc, query_sum, doc_sum):  # 计算query和doc之间的cosine距离
    dot_product = np.dot(query, doc)
    return dot_product / (query_sum * doc_sum)**0.5


def get_sorted_doc(query_vec, doc_ids, method="cosine", k2=500):  # 获取排序后的相关文章
    sorted_ids = {}

    if method == "cosine":
        query_sum = sum(query_vec ** 2)
        for doc_id in doc_ids:
            sorted_ids[doc_id] = dist_cosine(query_vec, docs[doc_id]["tf_idf"], query_sum, docs[doc_id]["doc_sum"])
    elif method == "bm25":
        query_w = (k2 + 1) * query_vec / (k2 + query_vec)
        for doc_id in doc_ids:
            start = time()
            t = np.nonzero(query_vec)
            sorted_ids[doc_id] = float((query_vec[t] * docs[doc_id]["bm25_w"][t]).sum())
            # print("bm25 time:", time() - start)

    sorted_ids = sorted(sorted_ids.items(), key=lambda k: k[1], reverse=False)
    return [i[0] for i in sorted_ids]


def index(request):
    return render(request, 'index.html')


def search(request):
    key = request.POST.get('key', '')

    keys = key.split()  # 空格分词
    print(keys)

    # keys = [a, b, c]
    # [1, 0, 1, 1, 0]
    ids = get_doc_ids_by_index(keys)  # 根据倒排索引召回paper
    print(ids)
    query_freq = get_freq_vec(keys)  # 拿query单词的词频
    print(query_freq)
    sorted_ids = get_sorted_doc(query_freq, ids)  # 根据词频向量和召回的doc，对doc排序
    print(sorted_ids)

    res = {
        'data': [id2doc(i) for i in sorted_ids]
    }

    # info = {
    #     'data': [
    #         {
    #             'title': 'Graph Convolution Neural Network',
    #             'author': 'ThomasN.Kipf, Max Welling',
    #             'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
    #         },
    #         {
    #             'title': 'Graph Attention',
    #             'author': 'ThomasN.Kipf, Max Welling',
    #             'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
    #         },
    #         {
    #             'title': 'Graph Embedding',
    #             'author': 'ThomasN.Kipf, Max Welling',
    #             'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
    #         }
    #     ]
    # }
    # if key == '1':
    #     info['data'] = [{
    #             'title': 'Graph Convolution Neural Network',
    #             'author': 'ThomasN.Kipf, Max Welling',
    #             'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
    #     }]
    # elif key == '2':
    #     info['data'] = [{
    #         'title': 'Graph Attention',
    #         'author': 'ThomasN.Kipf, Max Welling',
    #         'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
    #     }]
    # elif key == '3':
    #     info['data'] = [{
    #         'title': 'Graph Embedding',
    #         'author': 'ThomasN.Kipf, Max Welling',
    #         'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
    #     }]

    return render(request, 'content.html', res)


start = time()
init_data()
end = time()
print("initial time:", end-start)
while True:
    keys = input().split()
    start = time()
    keys = [stemmer.stem(w) for w in keys]
    print("searching:", keys)
    ids = get_doc_ids_by_index(keys)  # 根据倒排索引召回paper
    print(ids)

    query_freq = get_freq_vec(keys)  # 拿query单词的词频
    sorted_ids = get_sorted_doc(query_freq, ids, method="bm25")  # 根据词频向量和召回的doc，对doc排序
    print(sorted_ids)
    print("found results:", len(ids))
    print("search time:", time()-start)
