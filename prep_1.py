#! /usr/bin/python
voc = {};

f2 = open('tune_m.txt','w')

f = open('train.txt')
for lines in f:
	k = lines.strip().split(" ");
	for word in k:
		if word not in voc:
			voc[word] = 1;
		else:
			voc[word] += 1;

print len(voc)
#raw_input('Enter your input:')

voc = dict(sorted(voc.items(),key= lambda x: x[1], reverse=True)[0:9999])
f.close();

f = open('tuning.txt')
for lines in f:
	k = lines.strip().split(" ");
	for word in k:
		if word not in voc:
			f2.write("<OTHER> ");
		else:
			f2.write(word+" ");
	f2.write("\n");

f.close();
f2.close();


