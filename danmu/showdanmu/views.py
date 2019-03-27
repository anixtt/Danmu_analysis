from django.shortcuts import render
import sys
sys.path.append()#DouYuDanMu.py所在的目录
import DouYuDanMu
import threading
import json
# Create your views here.

dm = []
dmcls = DouYuDanMu.getDanMuSocket()
t1 = threading.Thread(target=dmcls.start, args=(9999, ))
t1.start()
t1.join()
def showdanmu(request):
    dm.append()
    return render(request, 'show.html', {'danmu_list': json.dumps()})