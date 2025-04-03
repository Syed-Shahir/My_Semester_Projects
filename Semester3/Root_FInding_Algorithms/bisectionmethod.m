clc
clear all
close all
%syms f(x)
f=input('enter function = ');
i=0;
ind=1;
err=1;
e=input('enter accuracy =');
disp('enter interval x1');
x1=input('=');
disp('enter interval x2');
x2=input('=');
check=f(x1)*f(x2);
if check<0
    fprintf(' I# |    x1    |    x2    |    xn    |   error  |'); 
    while err>e
        i=i+1;
    mid(i)=(x1+x2)/2;
    x3=f(mid(i));
    if f(x1)*f(mid(i))<0
        x2=mid(i);
    else 
        x1=mid(i);
    end
       error(i)=abs(x1-x2);
       err=error(i);
    
    fprintf('\n %d  | %f | %f | %f | %f |',i,x1,x2,mid(i),error(i));
    end
else
    disp('intervals are incorrect');
end
plot(error),xlabel('iterations');
ylabel('Error'),title('bisection method');
grid on;
fprintf('\nprogram end');