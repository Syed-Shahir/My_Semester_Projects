#include<iostream>
#include<ctime>
using namespace std;
void board(char *ch)
{
	cout<<ch[0]<<" |"<<ch[1]<<" |"<<ch[2]<<" "<<endl;
	cout<<"__|"<<"__|"<<"__"<<endl;
	cout<<ch[3]<<" |"<<ch[4]<<" |"<<ch[5]<<" "<<endl;
	cout<<"__|"<<"__|"<<"__"<<endl;
	cout<<ch[6]<<" |"<<ch[7]<<" |"<<ch[8]<<" "<<endl;
	cout<<"  |"<<"  |"<<endl;
    cout<<"\n\n";
}	
void playerturn(char *ch,char value)
{
int k;
do
{
cout<<"enter position to put X :";
cin>>k;
k--;
if(ch[k]==' ')
{
    ch[k]=value;
    break;
}
}
 while (k<0||k>8);
}
void player2turn(char *ch,char value)
{
   int k;
do
{
cout<<"enter position to put Y:";
cin>>k;
k--;
if(ch[k]==' ')
{
    ch[k]=value;
    break;
}
}
 while (k<0||k>8); 
}
int winnerfun(char *ch)
{
    if(ch[0]=='X'&&ch[1]=='X'&&ch[2]=='X'||ch[3]=='X'&&ch[4]=='X'&&ch[5]=='X'||ch[6]=='X'&&ch[7]=='X'&&ch[8]=='X'||ch[0]=='X'&&ch[3]=='X'&&ch[6]=='X'||ch[1]=='X'&&ch[4]=='X'&&ch[7]=='X'||ch[2]=='X'&&ch[5]=='X'&&ch[8]=='X'||ch[0]=='X'&&ch[4]=='X'&&ch[8]=='X'||ch[2]=='X'&&ch[4]=='X'&&ch[6]=='X')
    {
    return(1);
    }else if(ch[0]=='Y'&&ch[1]=='Y'&&ch[2]=='Y'||ch[3]=='Y'&&ch[4]=='Y'&&ch[5]=='Y'||ch[6]=='Y'&&ch[7]=='Y'&&ch[8]=='Y'||ch[0]=='Y'&&ch[3]=='Y'&&ch[6]=='Y'||ch[1]=='Y'&&ch[4]=='Y'&&ch[7]=='Y'||ch[2]=='Y'&&ch[5]=='Y'&&ch[8]=='Y'||ch[0]=='Y'&&ch[4]=='Y'&&ch[8]=='Y'||ch[2]=='Y'&&ch[4]=='Y'&&ch[6]=='Y')
    {
        return(2);
    }
}
int tiecheck(char *ch)
{
    int count=0;
    for (int i = 0; i < 9; i++)
    {
        if (ch[i]==' ')
        {
            return(1);
            break;
        }
    }
    return(0);
    
}
int main()
{
	char ch[9]={' ',' ',' ',' ',' ',' ',' ',' ',' '};
    char pl='X';
    char cm='Y';
    bool running=true;
	board(ch);
    int n=9;
    int check,check1;
    while (n!=0)
    {
        playerturn(ch,pl);
        board(ch);
       check=winnerfun(ch);
       check1=tiecheck(ch);
if (check==1)
{
    cout<<"congratulations!!! player 1 won "<<endl;
    break;
}
else if(check1==0)
{
    cout<<"the game has drawn :"<<endl;
    break;
}
//cout<<"check 1 :"<<check1<<endl;
        player2turn(ch,cm);
        board(ch);
        check=winnerfun(ch);
 if (check==2)
{
    cout<<"congratulations!!! player 2 won"<<endl;
    break;
}
else if(check1==0)
{
    cout<<"the game has drawn :"<<endl;
    break;
}
//cout<<"check 2 :"<<check1<<endl;

    }
}