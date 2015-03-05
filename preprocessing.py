#! /usr/bin/python

import pickle

vocab = []
dictionary = {}
invert_voc = {}
uni = {}
uni_denom = 0;
big = {}
big_denom = {}
tri = {}
tri_denom = {}
num = 100000;


def init(filename):
	global vocab,dictionary,invert_voc,uni,uni_denom,big,big_denom,tri,tri_denom

	invert_voc ={};
	f1 = open(filename)
	print f1

	for line in f1:
		k = line.strip().split(" ");
		for w in k:
			if w not in invert_voc:
				invert_voc[w] = 1;
			else:
				invert_voc[w] += 1;
	# train a unigram model


	

	print len(invert_voc)
	dictionary = dict(sorted(invert_voc.items(), key = lambda x: x[1], reverse = True)[0:num]);
	print len(dictionary)
	return;
	uni = dict(zip(range(0,len(dictionary)),dictionary.values()));
	#print dictionary
	invert_voc = dict(zip(dictionary.keys(),range(0,len(dictionary))));

	print len(invert_voc)
	print ('<OTHER>' in invert_voc)
	f1.close();



	f1.close();
	f1 = open(filename);

	
	for line in f1:
		k = line.strip().split(" ");
		for i in range(0,len(k)-1):
			if (invert_voc[k[i]], invert_voc[k[i+1]]) not in big:
				big[(invert_voc[k[i]], invert_voc[k[i+1]])] = 1;
			else:
				big[(invert_voc[k[i]], invert_voc[k[i+1]])] += 1;

			if i < len(k)-2:
				if (invert_voc[k[i]], invert_voc[k[i+1]], invert_voc[k[i+2]]) not in tri:
					tri[(invert_voc[k[i]], invert_voc[k[i+1]], invert_voc[k[i+2]])] = 1;
				else:
					tri[(invert_voc[k[i]], invert_voc[k[i+1]], invert_voc[k[i+2]])] += 1;

	f1.close();

	#print '*'*30
	#raw_input('Enter your input:')
	#print (sorted(uni.items(), key = lambda x: x[1], reverse = True)[0:100])
	#raw_input('Enter your input:')
	#print (sorted(big.items(), key = lambda x: x[1], reverse = True)[0:100])
	#raw_input('Enter your input:')
	#print (sorted(tri.items(), key = lambda x: x[1], reverse = True)[0:100])
	#raw_input('Enter your input:')
	#print '*'*30

	#print uni
	#print big
	#print tri


	uni_denom = sum(uni.values())

	for i,j,k in tri:
		tri[i,j,k] = float(tri[i,j,k]) / big[i,j]
	for i,j in big:
		big[i,j] = float(big[i,j]) / uni[i]
	for i in uni:
		uni[i] = float(uni[i]) / uni_denom

	
	
	f = open('invert_voc.txt','w');
	pickle.dump(invert_voc,f);
	f.close();


	f = open('unigram.txt','w');
	pickle.dump(uni, f)
	f.close();

	f = open('bigram.txt','w');
	pickle.dump(big, f);
	f.close();

	f = open('trigram.txt','w');
	pickle.dump(tri, f);
	f.close();
def get_uni(i):
	if i in uni:
		return uni[i];
	else:
		return 0.0;

def get_big(i,j):
	if (i,j) in big:
		return big[i,j];
	else:
		return 0.0;

def get_tri(i,j,k):
	if (i,j,k) in tri:
		return tri[i,j,k];
	else:
		return 0.0;

def tune(filename):
	
	l = [random.random(), random.random(), random.random()];
	l1, l2, l3 =  [x/sum(l) for x in l];
	print '*'*30
	#print invert_voc
	#print uni
	#print big
	#print tri

	while True:
		count1 = count2 = count3 = 0;
		f2 = open(filename);
		for line in f2:
			k = line.strip().split(" ");
			for i in range(0,len(k)-2):
				if k[i] in invert_voc and k[i+1] in invert_voc and k[i+2] in invert_voc:
					resp1 = l1 * get_uni(invert_voc[k[i+2]]);
					resp2 = l2 * get_big(invert_voc[k[i+1]],invert_voc[k[i+2]]);
					resp3 = l3 * get_tri(invert_voc[k[i]],invert_voc[k[i+1]],invert_voc[k[i+2]]);
					Z = resp1 + resp2 + resp3;
					count1, count2, count3 = map(lambda x,y:x+y, [count1, count2, count3], [resp1/Z, resp2/Z, resp3/Z]);
		Z = count1 + count2 + count3;
		l1, l2, l3 = map(lambda x: x/Z, [count1, count2, count3]);
		print l1, l2, l3		
					
def train_context(filename, c):
	p_z_w = [[random.random() for x in range(c)] for y in range(num)]
	p_w_z = [[random.random() for x in range(num)] for y in range(c)]
	p_z_w = [[p_z_w[y][x]/sum(p_z_w[y]) for x in range(c)] for y in range(num)]
	p_w_z = [[p_w_z[y][x]/sum(p_w_z[y]) for x in range(num)] for y in range(c)]

	print p_z_w
	#only keeping the structure, without modifying the numbers.
	# z_w means z, conditioned on w, and the first dimension is about w
	#p_z_w_new = [[0 for x in range(c)] for y in range(10000)]
	#p_w_z_new = [[0 for x in range(10000)] for y in range(c)]



	#w_count = [0 for x in range(10000)];
	#z_count = [0 for x in range(c)];

	while True:
		f = open(filename);
		for line in f:
			k = line.strip().split(" ");
			for i in range(0,len(k)-1):
				if k[i] in invert_voc and k[i+1] in invert_voc:
					w1, w2 = invert_voc[k[i]], invert_voc[k[i+1]];
					#w_count[w1] += 1;				
					# E-step: calculating the posterior prob of hidden var z
					temp_z_count = [p_z_w[w1][x]*p_w_z[x][w2] for x in range(c)]
					Z = sum(temp_z_count);
					temp_z_count = map(lambda x: x/Z, temp_z_count);

					#z_count = map(lambda x,y:x+y, z_count, temp_z_count);
					# M-step: calculating the numerator	
					#update p_z_w
					p_z_w[w1] = map(lambda x,y:x+y, p_z_w[w1], temp_z_count);
					#update p_w_z
					for j in range(0,c):				
						p_w_z[j][w2] += temp_z_count[j]
		#finally normalize:
		p_z_w = [[p_z_w[y][x]/sum(p_z_w[y]) for x in range(c)] for y in range(num)]
		p_w_z = [[p_w_z[y][x]/sum(p_w_z[y]) for x in range(num)] for y in range(c)]
		f.close();
		print log_likelihood(filename, p_z_w, p_w_z, c);


def log_likelihood(filename, p_z_w, p_w_z, c):
	f = open(filename);
	llh = 0.0;
	for line in f:
		k = line.strip().split(" ");
		for i in range(0,len(k)-1):
			if k[i] in invert_voc and k[i+1] in invert_voc:
				w1, w2 = invert_voc[k[i]], invert_voc[k[i+1]];
				temp = sum([p_z_w[w1][x]*p_w_z[x][w2] for x in xrange(c)]);
				llh += log(temp,2);
				
	f.close();
	return llh;


if __name__ == "__main__":
	init('train_m.txt');
	#tune('tuning.txt');
	#train_context('train.txt',6);
	#outputdict();

