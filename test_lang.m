a = "The agency officials sold securities";
a = upper(a)
rem = a;
sentences = {};
len = 1;
while (length(rem)~=0)
	[str rem] = strtok(rem);
	sentences(len,1) = str;
	len += 1;
end
len
M = zeros(1,101);
i = 1;
for i = 1:101
	M(i) = 0;
	lambda = 0.01*(i-1)
	for k = 1:len-1
	if k == 1
	M(i) = M(i) + log(lambda*uni_count(cellidx(vocab,sentences(k,1))) + (1 - lambda) * bi_count(cellidx(vocab, "<s>"), cellidx(vocab, sentences(k,1))))/log(2);
	else
	M(i) = M(i) + log(lambda*uni_count(cellidx(vocab,sentences(k,1))) + (1 - lambda) * bi_count(cellidx(vocab,sentences(k-1,1)), cellidx(vocab, sentences(k,1))))/log(2);
	end
	end
end

plot(0:0.01:1,M);
