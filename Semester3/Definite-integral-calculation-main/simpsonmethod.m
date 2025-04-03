 clc
 clear all
 close all
%syms x
a =input('enter lower limit =');
b =input('enter upper limit =');
n=input('enter number of intervals =');
f =input('enter function =');
h = (b - a)/n;
X = f(a)+f(b);
Odd = 0;
Even = 0;
for i = 1:2:n-1
    xi=a+(i*h);
    Odd=Odd+f(xi);
end
for i = 2:2:n-2
    xi=a+(i*h);
    Even=Even+f(xi);
end
I = (h/3)*(X+4*Odd+2*Even);
  
disp('approximate value = ');
disp(I);