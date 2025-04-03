clc
clear all
close all
%syms f(x);
x=0;
sum=0;
b=input('enter upper limit =');
a=input('enter lower limit =');
n=input('enter number of intervals =');
h=(b-a)/n;
f=input('enter function');
i=1;
while(x<=b)
    F(i)=f(x);
    x=x+h;
   i=i+1;
end
for j=1:i-1
    if j==1||j==i-1
        h/2*(F(j));
        sum=sum+(h/2*(F(j)));
    else
        h*F(j);
        sum=sum+h*F(j);
    end
end
disp('definite integral value=');
disp(sum);