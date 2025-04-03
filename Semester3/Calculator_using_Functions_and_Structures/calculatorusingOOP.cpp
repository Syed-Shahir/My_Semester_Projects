#include<iostream>
using namespace std;
struct calculator
{
double num1;
double num2;
char op;
}s;
void getinput()
{
    cout<<"enter first number = ";
    cin>>s.num1;
    cout<<"enter second number = ";
    cin>>s.num2;
    cout<<"enter the opetration (+,-,/,*):";
    cin>>s.op;
}
double performoperation()
{
switch (s.op)
{
case '+':
    return(s.num1+s.num2);
    break;
    case '-':
    return(s.num1-s.num2);
    break;
    case '*':
    return(s.num1*s.num2);
    break;
    case '/':
    return(s.num1/s.num2);
default:
cout<<"invalid character.....try again!!!!";
return(0);
    break;
}
}
int main()
{
    char ch;
    do
    {
        getinput();
        double ans=performoperation();
        cout<<"your answer is = "<<ans<<endl;
        cout<<"do you want to perform another calculation (y/n) ?";
        cin>>ch;
    } while (ch!='n'&&ch!='N');
}