import ConnectMongodb
import re
import pandas as pd
import Segment

# Segment.run()
douyudb = ConnectMongodb.DouYuDB()
Str = douyudb.DailyString
Word = douyudb.Word
filenames = []
words = []
frequencies = []
slice_rule = re.compile('(.*),([\d]{2,6})')
z = {}
for day in Str.find():
    filenames.append('dailystring/allresult%s.txt' % day['_id'])
for file in filenames:
    try:
        with open(file, 'r') as read_file:
            while True:
                data = read_file.readline()
                if not data:
                    break
                    pass
                word = slice_rule.findall(data)[0][0]
                frequency = slice_rule.findall(data)[0][1]
                if word not in words:
                    words.append(word)
                    frequencies.append(int(frequency))
                else:
                    for i in range(len(words)):
                        if words[i] == word:
                            frequencies[i] += int(frequency)
    except FileNotFoundError:
        continue
dict = {}
dict["words"] = words
dict["frequency"] = frequencies

extra_dict = pd.DataFrame(dict).sort_values(by="words", ascending=False)
extra_dict.to_csv('extractdict/extract_dict.txt', header=False, index=0)