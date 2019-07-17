# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import sys
sys.path.append("..")
import Segment
from gensim.models import word2vec
import time
import jieba
import re
import jieba.analyse
import pymongo
import json

dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
douyudb = dbclient["DouYu"]
dm = douyudb['DanMu']
jieba.load_userdict('others/extra_dict.txt')
# def index(request):
#     return render(request, 'index.html', {})

def room(request):
    return render(request, 'room.html', {})

@csrf_exempt
def analyse(request):
    model = word2vec.Word2Vec.load('../others/弹幕.model')
    danmus = request.POST.get("danmus", 0)
    print(danmus)
    w = ''
    d = Segment.Chinese_Word_Segmentation(time.strftime("%Y-%m-%d", time.localtime()), danmus)
    for word in d:
        w += word[0] + ' '
    with open('danmuall.txt', 'w') as f:
        f.write(' '.join(jieba.cut(danmus, cut_all=False)))
    f.close()
    sentences = word2vec.Text8Corpus(r'danmuall.txt')
    # model = word2vec.Word2Vec(sentences, size=10, hs=1, min_count=2, window=5)
    return HttpResponse(w+'!@##$$$%%%^^^&&&***(((*&)^'+model.doesnt_match(w.split()))


@csrf_exempt
def jiebaanalyse(request):
    model = word2vec.Word2Vec.load('../others/弹幕.model')
    danmus = request.POST.get("danmu_jieba", 0)
    print(danmus)
    keywords = jieba.analyse.extract_tags(danmus, topK=20, withWeight=True, allowPOS=())
    word = ''
    # 访问提取结果
    for item in keywords:
        # 分别为关键词和相应的权重
        word += item[0] + ' '
    with open('danmualljieba.txt', 'w') as f:
        f.write(' '.join(jieba.cut(danmus, cut_all=False)))
    f.close()
    sentences = word2vec.Text8Corpus(r'danmualljieba.txt')
    # model = word2vec.Word2Vec(sentences, size=10, hs=1, min_count=2, window=5)
    # sign !@##$$$%%%^^^&&&***(((*&)^
    return HttpResponse(word+'!@##$$$%%%^^^&&&***(((*&)^'+model.doesnt_match(word.split()))

@csrf_exempt
def suspectuser(request):
    user = request.POST.get("userlist")
    nickname = []
    user = user.strip('[')
    user = user.strip(']')
    user = set(user.split(','))
    for u in user:
        u = re.compile('"(.*?)"').findall(u)[0]
        for x in dm.find({"用户ID": u}).skip(dm.find({"用户ID": u}).count() - 1):
            nickname.append(x['昵称'])
    d = zip(user, nickname)
    d = json.dumps(dict(d))
    return HttpResponse(json.dumps({'udata': d}))


@csrf_exempt
def suggestban(request):
    danm = request.POST.get("danmu_jieba")
    print(danm)
    length = 0
    model = word2vec.Word2Vec.load('../others/jy.model')
    for x in jieba.cut(danm):
        try:
            model.most_similar_cosmul(x)
            length += 1
        except:
            continue
    if length >= 2:
        return HttpResponse('no')
    else:
        return HttpResponse('yes')
