import glob, os
import csv

results = []
with open('config/queue.txt', newline='\n') as inputfile:
    result = csv.reader(inputfile)
    for row in result:
        results.append(row[0])



for file in os.listdir("E:\TweetPort-1\TweetPort\downloaded2"):
    filename = file.replace(".csv","")
    if filename in results:
        #print(filename)
        results.remove(filename)

for x in results:
    print(x)
