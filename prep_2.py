#! /usr/bin/python
from math import log
import random
import copy

voc = {}

#if you want to build a index based on string, count it will cost more because you will have different initialization
def buildvoc(filename):
	global voc;
	count = {}
	f = open(filename)
	for lines in f:
		k = lines.strip().split(" ");
		for i in range(len(k)):
			if k[i] not in count:
				count[k[i]] = 1;
			else:
				count[k[i]] += 1;

	voc = dict(zip(count.keys(),range(10000)))
	f.close();




def init(filename):
	unigram = {}
	bigram = {}
	trigram = {}
	unigram_count = {}
	bigram_count = {}
	trigram_count = {}
	f = open(filename)
	for lines in f:
		k = lines.strip().split(" ");
		for i in range(len(k)):
			if voc[k[i]] not in unigram_count:
				unigram_count[voc[k[i]]] = 1;
			else:
				unigram_count[voc[k[i]]] += 1;

			if i < len(k)-1:
				if (voc[k[i]],voc[k[i+1]]) not in bigram_count:
					bigram_count[voc[k[i]],voc[k[i+1]]] = 1;
				else:
					bigram_count[voc[k[i]],voc[k[i+1]]] += 1;

			if i < len(k)-2:
				if (voc[k[i]],voc[k[i+1]],voc[k[i+2]]) not in trigram_count:
					trigram_count[voc[k[i]],voc[k[i+1]],voc[k[i+2]]] = 1;
				else:
					trigram_count[voc[k[i]],voc[k[i+1]],voc[k[i+2]]] += 1;			
	# so voc contains exactly 10000 words


	f.close();
	for w1, w2, w3 in trigram_count:
		trigram[w1, w2, w3] = float(trigram_count[w1, w2, w3]) / bigram_count[w1, w2];

	for w1, w2 in bigram_count:
		bigram[w1, w2] = float(bigram_count[w1, w2]) / unigram_count[w1];

	for w1 in unigram_count:
		unigram[w1] = float(unigram_count[w1]) / sum(unigram_count.values());


	return unigram, bigram, trigram, unigram_count, bigram_count, trigram_count
	#print '*'*30
	#raw_input('Enter your input:')
	#print (sorted(unigram.items(), key = lambda x: x[1], reverse = True)[0:100])
	#raw_input('Enter your input:')
	#print (sorted(bigram.items(), key = lambda x: x[1], reverse = True)[0:100])
	#raw_input('Enter your input:')
	#print (sorted(trigram.items(), key = lambda x: x[1], reverse = True)[0:100])
	#raw_input('Enter your input:')
	#print '*'*30
def cp_unigram(w1, unigram):
	return unigram[w1];


def cp_bigram(w1, w2, bigram):
	if (w1, w2) in bigram:
		return bigram[w1, w2];
	else:
		return 0;


def cp_trigram(w1, w2, w3, trigram):
	if (w1, w2, w3) in trigram:
		return trigram[w1, w2, w3];
	else:
		return 0;


def mixture_train(trigram_count_tu, unigram_tr, bigram_tr, trigram_tr):
	l = [random.random(), random.random(), random.random()];
	l = [x/sum(l) for x in l];
	count = [0 for x in range(3)];
	

	while True:
		l_n = [0 for x in range(3)];

		for w1, w2, w3 in trigram_count_tu:
			count[0] = l[0] * cp_unigram(w3, unigram_tr);
			count[1] = l[1] * cp_bigram(w2, w3, bigram_tr);
			count[2] = l[2] * cp_trigram(w1, w2, w3, trigram_tr);
			#print k[i],k[i+1],k[i+2]
			#print count;
			count = [(x/sum(count))*trigram_count_tu[w1,w2,w3] for x in count];
			l_n = map(lambda x,y:x+y, l_n, count);

		l_n = [x/sum(l_n) for x in l_n];
		l = l_n[:];
		print l
		print loglike_mix(l, trigram_count_tu, unigram_tr, bigram_tr, trigram_tr)



def loglike_mix(l, trigram_count, unigram_tr, bigram_tr, trigram_tr):
	llh = 0.0;
	count = sum(trigram_count.values());

	for w1, w2, w3 in trigram_count:
		llh += trigram_count[w1, w2, w3] * log(l[0]*cp_unigram(w3, unigram_tr)+l[1]*cp_bigram(w2,w3, bigram_tr)+l[2]*cp_trigram(w1,w2,w3, trigram_tr))

	return llh / count;

	

def context_train(c):
	print '-------------------'
	p_z_w = [[random.random() for x in xrange(c)] for y in xrange(10000)]
	p_w_z = [[random.random() for x in xrange(10000)] for y in xrange(c)]
	denom_z_w = [sum(p_z_w[y]) for y in xrange(10000)]
	denom_w_z = [sum(p_w_z[y]) for y in xrange(c)]
	p_z_w = [[p_z_w[y][x]/denom_z_w[y] for x in range(c)] for y in range(10000)]
	p_w_z = [[p_w_z[y][x]/denom_w_z[y] for x in range(10000)] for y in range(c)]
	print '-------------------'
	ltrain = -1000.0

	while True:
		print '-------------------'
		p_z_w_n = [[0 for x in xrange(c)] for y in xrange(10000)]
		p_w_z_n = [[0 for x in xrange(10000)] for y in xrange(c)]
		
		for w1, w2 in bigram_count_tr:			
			# E-step
			tempz = [p_z_w[w1][x]*p_w_z[x][w2] for x in xrange(c)];
			tempz = [(x / sum(tempz))*bigram_count_tr[w1,w2] for x in tempz];
			# M-step
			for j in xrange(c):
				p_z_w_n[w1][j] += tempz[j];
			for j in xrange(c):
				p_w_z_n[j][w2] += tempz[j];

		print '-------------------'
		#<END> has no training example to act as w, so the denominator will be zero..
		p_z_w_n[voc['<END>']] = [1 for x in xrange(c)];

		denom_z_w = [sum(p_z_w_n[y]) for y in xrange(10000)]
		denom_w_z = [sum(p_w_z_n[y]) for y in xrange(c)]

		p_z_w_n = [[p_z_w_n[y][x]/denom_z_w[y] for x in xrange(c)] for y in xrange(10000)]
		p_w_z_n = [[p_w_z_n[y][x]/denom_w_z[y] for x in xrange(10000)] for y in xrange(c)]
		p_z_w = copy.deepcopy(p_z_w_n);
		p_w_z = copy.deepcopy(p_w_z_n);
		ltrain2, ltune2 = loglike_context(p_z_w, p_w_z, c, bigram_count_tr), loglike_context(p_z_w, p_w_z, c, bigram_count_tu);
		print ltrain2, ltune2

		#print ltrain2, ltrain, ltrain2 - ltrain
		if ltrain2 - ltrain < 0.01:
			break;
		ltrain = ltrain2;
		
	return ltune2, p_z_w, p_w_z;


def loglike_context(p_z_w, p_w_z, c, bigram_count):
	llh = 0.0;
	count = sum(bigram_count.values());
	for w1, w2 in bigram_count:	
		llh += bigram_count[w1,w2]*log(sum([p_z_w[w1][j]*p_w_z[j][w2]for j in range(c)]))

	return llh / count;

def mixture_train_g(trigram_count_tu, unigram_tr, bigram_tr, p_z_w, p_w_z):
	l = [random.random(), random.random(), random.random()];
	l = [x/sum(l) for x in l];
	count = [0 for x in range(3)];
	

	while True:
		l_n = [0 for x in range(3)];

		for w1, w2, w3 in trigram_count_tu:
			count[0] = l[0] * cp_unigram(w3, unigram_tr);
			count[1] = l[1] * cp_bigram(w2, w3, bigram_tr);
			count[2] = l[2] * sum([p_z_w[w1][j]*p_w_z[j][w2] for j in range(len(p_w_z))])
			#print k[i],k[i+1],k[i+2]
			#print count;
			count = [(x/sum(count))*trigram_count_tu[w1,w2,w3] for x in count];
			l_n = map(lambda x,y:x+y, l_n, count);

		l_n = [x/sum(l_n) for x in l_n];
		l = l_n[:];
		print l
		print loglike_mix_g(l, trigram_count_tu, unigram_tr, bigram_tr, p_z_w, p_w_z)



def loglike_mix_g(l, trigram_count, unigram_tr, bigram_tr,  p_z_w, p_w_z):
	llh = 0.0;
	count = sum(trigram_count.values());

	for w1, w2, w3 in trigram_count:
		llh += trigram_count[w1, w2, w3] * log(l[0]*cp_unigram(w3, unigram_tr)+l[1]*cp_bigram(w2,w3, bigram_tr)+l[2]* sum([p_z_w[w1][j]*p_w_z[j][w2] for j in range(len(p_w_z))]))

	return llh / count;




if __name__ == "__main__":
	buildvoc('train_m.txt');
	unigram_tr, bigram_tr, trigram_tr, unigram_count_tr, bigram_count_tr, trigram_count_tr = init('train_m.txt');
	unigram_tu, bigram_tu, trigram_tu, unigram_count_tu, bigram_count_tu, trigram_count_tu = init('tune_m.txt');

	#mixture_train(trigram_tu, unigram_tr, bigram_tr, trigram_tr);

	#ltune2, p_z_w, p_w_z = context_train(6);
	#mixture_train_g(trigram_tu, unigram_tr, bigram_tr, p_z_w, p_w_z);

	l = [context_train(c)[0] for c in range(1,31)];
	print l;


















