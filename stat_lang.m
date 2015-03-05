f_vocab = fopen('vocab.txt')
vocab = {}
i = 1;

for i = 1:500
	s = fgets(f_vocab);
	s = s(1:size(s,2)-1)
	size(s)
	vocab(i,1) = s;	
end

fclose(f_vocab);
uni_count = load('unigram.txt');
uni_count = uni_count / sum(uni_count);

bi_count_sp = load('bigram.txt');
len = size(bi_count_sp,1)
bi_count = zeros(500,500);

for i = 1:len
	bi_count(bi_count_sp(i,1), bi_count_sp(i,2)) = bi_count_sp(i,3);
end

for i = 1:500
	if (sum(bi_count(i, :)) ~= 0)
		bi_count(i, :) = bi_count(i, :) / sum(bi_count(i, :));
	end
end

for i = 1:500
	s = cell2mat(vocab(i,1));
	if s(1) == 'S'
		s
		uni_count(i)
	end
end

idx = cellidx(vocab,"THE\n")
s = bi_count(idx,:)
l = sortrows([-s' (1:500)'],1)

for i = 1:10
	k = l(i,2);
	s = cell2mat(vocab(k,1))
end

a = "The stock market fell a hundred points on Friday";
a = upper(a);
rem = a;
sentences = {};
i = 1;
while (length(rem)~=0)
	[str rem] = strtok(rem);
	sentences(i,1) = str;
	i += 1;
end


U = 1;
B = 1;
for k = 1:i-1
	U = U * uni_count(cellidx(vocab,strcat(sentences(k,1),"\n")));
end


for k = 1:i-1
	if k == 1
	B = B * bi_count(cellidx(vocab,strcat(sentences(k,1),"\n")),cellidx(vocab,"<s>\n"))
	else
	B = B* 	bi_count(cellidx(vocab,strcat(sentences(k,1),"\n")),cellidx(vocab,strcat(sentences(k-1,1),"\n")))
	end
end

B = 1;
for k = 1:i-1
	U = U * uni_count(cellidx(vocab,sentences(k,1)));
end


for k = 1:i-1
	if k == 1
	B = B * bi_count(cellidx(vocab,"<s>"),cellidx(vocab,sentences(1,1)));
	else
	B = B* 	bi_count(cellidx(vocab,sentences(k-1,1)),cellidx(vocab,sentences(k,1)));
	end
end






