clc
clear all
close all
syms f(x)
f=input('enter function = ');
i=0;
itr=input('enter the iterations =');
mid=input('give mid value');
    g1=diff(f);
    if subs(g1,x,mid)~=0
   fprintf(' I# |   Xn-1 |    xn    |   error  |'); 
    for i=1:itr
        g2=subs(f,x,mid);
        g3=subs(g1,x,mid);
    x3=vpa (mid-(g2/g3));
    error(i)=abs(x3-mid);    
    fprintf('\n %d  | %f | %f | %f |',i,x3,mid,error(i));
    mid=x3;
    end
    else
        disp('NR not possible');
    end
plot(error),xlabel('iterations');
ylabel('Error'),title('NR method');
fprintf('\nend of program');