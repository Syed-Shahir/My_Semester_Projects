#include<iostream>
#include<string>
using namespace std;
struct loginsystem
{
    string name;
    string num;
    int type;
    char save;
    int start,exit;
}s[14];
int main()
{
int count1=0,count2=0,count3=0;
int i=0,j;
char log;
string number;
do
{
    system("cls");
    cout<<"enter name :";
    getline(cin,s[i].name);
    cout<<"enter number :";
    getline(cin,s[i].num);
    cout<<"select employee type :"<<endl;
    cout<<"1)press 1 for office staff "<<endl;
    cout<<"2)press 2 for supervisory "<<endl;
    cout<<"3)press 3 for utility "<<endl;
    cin>>s[i].type;
    cin.ignore();
    if(s[i].type==1)
    {
        if(count1==2)
        {
            cout<<"office staff space is full"<<endl;
        }
        else
        count1++;
    }
    else if(s[i].type==2)
    {
                if(count2==2)
        {
            cout<<"supervisor space is full"<<endl;
        }
        else
        count2++;
    }
    else if(s[i].type==3)
    {
                if(count3==2)
        {
            cout<<"utility  space is full"<<endl;
        }
        else
        count3++;
    }
    else
    cout<<"invalid choice "<<endl;
    cout<<"do you want to save or not ? y/n "<<endl;
    cin>>s[i].save;
    cin.ignore();
    if(s[i].save=='y'||s[i].save=='Y')
    {
        i++;
    }
} while (count1!=2 || count2!=2 || count3!=2);
system("cls");
cout<<"*********************"<<endl;
cout<<"***LOGIN PORTAL***"<<endl;
cout<<"enter the employe number :";
cin>>number;
for(int i=0;i<15;i++)
{
if(number==s[i].num)
{
    j=i;
    break;
}
}
system("cls");
 do{
     system("cls");
     cout<<"\nenter A for login\nenter B for logout\ne for exit :"<<endl;
     cin>>log;
 if(log=='a'||log=='A')
 {
 cout<<"you selected log in :"<<endl;
 cout<<"enter the starting time 24 hr:";
 cin>>s[j].start;
 system("cls");
 cout<<"thanks";
 }
 else if(log=='b'||log=='B')
 {
     cout<<"you selected log out :"<<endl;
     cout<<"enter the ending time 24 hr:";
     cin>>s[j].exit;
     cout<<"you rendered "<<(s[j].exit)-(s[j].start)<<":00 hours of service today"<<endl;
     system("cls");
     cout<<"thanks";
 }
 }
 while(log!='e'&&log!='E');
 cout<<"thanks for using "<<endl;
}


