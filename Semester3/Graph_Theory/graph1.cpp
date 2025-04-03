#include <iostream>
using namespace std;
int main()
{
int n,nn;
cout<<"enter number of nodes =";
cin>>n;
char arr[n];
cout<<"enter data in nodes :"<<endl;
for(int i=0;i<n;i++)
{
	cin>>arr[i];
}
nn=n;
int m[n][nn];
for(int i=0;i<n;i++)
{
	for(int j=0;j<nn;j++)
	{
		cout<<"weight between "<<arr[i]<<" & "<<arr[j]<<"= ";
		cin>>m[i][j];
	}
}
cout<<"\t";
for(int i=0;i<n;i++)
{
	cout<<arr[i]<<"\t";//for clear view purpose
}
cout<<endl;
for(int i=0;i<n;i++)//printing the matrix
{
	cout<<arr[i]<<"\t";
	for(int j=0;j<nn;j++)
	{
		cout<<m[i][j]<<"\t";
	}
	cout<<endl;
}
}

