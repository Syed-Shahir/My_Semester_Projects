clc
clear all
close all
%syms f(x)
f=input('enter function = ');
i=0;
err=1;
e=input('enter the accuracy =');
disp('enter interval x1');
x1=input('=');
disp('enter interval x2');
x2=input('=');
check=f(x1)*f(x2);
if check<0
    fprintf(' I# |    x1    |    x2    |    xn    |   error  |'); 
    while err>e
        i=i+1;
     j=x1*f(x2);
     k=x2*f(x1);
    mid=(j-k)/(f(x2)-f(x1));
    x3=f(mid);
    if f(x1)*x3<0
        x2=mid;
    elseif f(x2)*x3<0
        x1=mid;
    end
    err=abs(x3);
    error(i)=err;
        fprintf('\n %d  | %f | %f | %f | %f |',i,x1,x2,mid,error(i));
    end
else
    disp('intervals are incorrect');
end
plot(error),xlabel('iterations');
ylabel('Error'),title('regula falsi method');
grid on;
fprintf('\nend of program');