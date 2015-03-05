function EM()
X = load('X.dat');
Y = load('Y.dat');
[len, dim] = size(X);




p = 0.6*ones(1,dim);
[p, Lf] = train(X,Y,p);


[Xt, Yt] = gen_train(X,Y,1000);
num = [100 200 400 800 1600 3200 6400];
L_train = zeros(1,7);
L_test = zeros(1,7);

for i=1:7
	[X1, Y1] = gen_train(X,Y,num(i));
	[p, L_train(i)] = train(X1, Y1, 0.6*ones(1,dim));
	[mid_result, L_test(i)] = cal_L(Xt,Yt,p);
end

figure;
hold on;
plot(num, L_train,'b');
plot(num, L_test,'r');

function [p, Lf] = train(X,Y,p)
[len, dim] = size(X);
L = zeros(1,100);
for iter = 1:100
	T = sum(X,1);
	[mid_result, L(iter)] = cal_L(X,Y,p);
	L(iter)
	rate = sum(((Y./mid_result)*ones(1,dim)).*X,1);
	p = (rate.*p)./T;
	if iter > 1 && L(iter) - L(iter-1) < 1e-6
	break;
end
Lf = L(iter);

end


function [mid_result, L] = cal_L(X,Y,p)
[len, dim] = size(X);
mid_result = zeros(len,1);
L = 0;

mid_result = 1 - prod(repmat(ones(1,dim) - p, len, 1).^(X),2);

L = sum((Y==1).*(log(mid_result)) + ((Y==0).*log(1 - mid_result)));

L = L / len;
end


function [X1, Y1] = gen_train(X,Y,num)
	[len,dim] = size(X);
	X1 = zeros(num,dim);
	Y1 = zeros(num,1);

	for i = 1:num
		row = ceil(rand*len);		
		X1(i,:) = X(row,:);
		Y1(i) = Y(row);
	end

end
%	temp = 1;	
%	for i = 1:dim
%		if X(t,i) == 1
%			temp = temp * (1 - p(i));
%		end
%	end
%	mid_result = 1 - temp;
%	if Y(t) == 1
%		temp = 1 - temp;
%	end
%	L = L + log(temp);
