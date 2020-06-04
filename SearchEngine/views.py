from django.http import HttpResponse
from django.shortcuts import render
import json


sorted_index = {
    "apple": ["1", "2"],
    "banana": ["3", "4", "5"]
}
paper = {
    "1": {
        "title": "Apple Better Than Banana",
        "author": "Apple's mother",
        "abstract": "This is abstract",
        "text": "too much",
        "word_freq": [5, 0, 2, 8, 0]
    },
    "2": {
        "title": "Banana Better Than Apple",
        "author": "Banana's mother",
        "abstract": "This is abstract",
        "text": "too much",
        "word_freq": [2, 1, 5, 0, 0]
    },
    "3": {
        "title": "3",
        "author": "This is author",
        "abstract": "This is abstract",
        "text": "too much",
        "word_freq": [3, 1, 5, 0, 0]
    },
    "4": {
        "title": "4",
        "author": "This is author",
        "abstract": "This is abstract",
        "text": "too much",
        "word_freq": [4, 1, 5, 0, 0]
    },
    "5": {
        "title": "5",
        "author": "This is author",
        "abstract": "This is abstract",
        "text": "too much",
        "word_freq": [5, 1, 5, 0, 0]
    }
}


def word2id(key):  # str -> list
    return sorted_index[key]


def id2paper(ID):  # str -> dict
    return paper[ID]


def key2onehot(key):  # str -> list
    return [1, 0, 1, 1, 0]


def get_paper_ids_by_index(keys):
    res = []
    for key in keys:
        res.extend(word2id(key))
    return res


def get_onehot(keys):
    res = []
    for key in keys:
        res.append(key2onehot(key))
    return res


def get_sorted_paper(one_hots, ids):
    '''
    :param one_hots: 假设查询单词有k个，则size=kxM
    :param ids: 召回的文章id列表
    :return:
    '''

    for ID in ids:
        doc = id2paper(ID)
        doc_vec = doc['word_freq']

    return ids


def index(request):
    return render(request, 'index.html')


def search(request):
    key = request.POST.get('key', '')

    keys = key.split()  # 空格分词
    print(keys)

    # keys = [a, b, c]
    # [1, 0, 1, 1, 0]
    ids = get_paper_ids_by_index(keys)  # 根据倒排索引召回paper
    print(ids)
    one_hots = get_onehot(keys)  # 拿单词的独热编码
    print(one_hots)
    sorted_ids = get_sorted_paper(one_hots, ids)  # 根据独热编码和召回的paper，对paper排序
    print(sorted_ids)

    res = {
        'data': [id2paper(i) for i in sorted_ids]
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
