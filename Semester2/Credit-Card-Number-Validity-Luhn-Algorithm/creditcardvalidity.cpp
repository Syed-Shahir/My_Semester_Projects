#include<iostream>
#include <bits/stdc++.h>
using namespace std;
int step1(string numb)//this function will add even numbered*2 if 2*numb>9(two digits) that
    {                //will be added separately
    int k,c,sum=0;
    k=numb.size();
    for(int i=1;i<k;i=i+2)
    {
        numb[i]=numb[i]-48;
        c=numb[i]*2;
        if(c>9)
        {
            c=c%10;
            sum=sum+1+c;
        }
        else
        sum=sum+c;
    }
    return(sum);

}
int oddnumberedsum(string numb)//this function will add all the odd numbered digits
{
    int k,c,sum=0;
    k=numb.size();
    for(int i=0;i<k;i=i+2)
    {
        numb[i]=numb[i]-48;
        sum=sum+numb[i];
    }
    return(sum);
}
int main()
{
    string number;
    int result=0;
    //int st1,st2;//to store return of step 1(function 1)of algo
    cout<<"do not enter any spaces or characters"<<endl;
    cout<<"enter credit card number =";
    getline(cin,number);
    //this built in function is used to reverse string because we
    //will work from right to left
    reverse(number.begin(),number.end());
    //cout<<"you entered this number :"<<number;
    // st1 =step1(number);
    // cout<<st1;
    // st2=oddnumberedsum(number);
    // cout<<st2;
    result=(step1(number))+(oddnumberedsum(number));
    //cout<<result;
    if(result%10==0)
    cout<<"credit card number is valid ";
    else
    cout<<"invalid number try again";
}
