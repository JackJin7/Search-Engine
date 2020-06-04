from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def search(request):
    key = request.POST.get('key', '')
    print(key)
    # TODO 根据key找论文list

    info = {
        'data': [
            {
                'title': 'Graph Convolution Neural Network',
                'author': 'ThomasN.Kipf, Max Welling',
                'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
            },
            {
                'title': 'Graph Attention',
                'author': 'ThomasN.Kipf, Max Welling',
                'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
            },
            {
                'title': 'Graph Embedding',
                'author': 'ThomasN.Kipf, Max Welling',
                'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
            }
        ]
    }
    if key == '1':
        info['data'] = [{
                'title': 'Graph Convolution Neural Network',
                'author': 'ThomasN.Kipf, Max Welling',
                'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
        }]
    elif key == '2':
        info['data'] = [{
            'title': 'Graph Attention',
            'author': 'ThomasN.Kipf, Max Welling',
            'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
        }]
    elif key == '3':
        info['data'] = [{
            'title': 'Graph Embedding',
            'author': 'ThomasN.Kipf, Max Welling',
            'abstract': 'This for abstract. Can be soooooooooooooooooooooooooooooooooooooo long. We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efﬁcient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized ﬁrst-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a signiﬁcant margin.',
        }]

    return render(request, 'content.html', info)
