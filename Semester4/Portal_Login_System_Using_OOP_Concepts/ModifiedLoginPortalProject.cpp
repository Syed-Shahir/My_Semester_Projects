#include <iostream>
#include <string>
#include <cstdlib>
#include<conio.h>
using namespace std;
//class is acting like a container to hold different data
//private access specifier is used because the information has to be 
//kept away from normal access
class Employee 
{
private:
//private attributes
    string name;
    string empNo;
    int empType;
    int logInTime;
    int logOutTime;
public:
    Employee()
    {
        name = "xxx";
        empNo = "xxx";
        empType = 0;
        logInTime = 0;
        logOutTime =0;
    }
    //this can be called a friendly function because it is used to 
    //assign values to the entities stores in private
    void SetEmployee(string a,string b,int c)
    {
        name = a;
        empNo = b;
        empType = c;
       
    }
    //this function is used to print result according to 
    //am and pm time spaces
    //this function will be in use for the login time
    //this is  also friendly function 
    void logIn(int time,string amOrpm)
    {
        if (amOrpm == "am") {
            logInTime = time;
        }
        else 
            logInTime = time+12;
    }
    //this function also works the same as previous but its for logout time
    //this is also a friendly function
    void logOut(int time, string amOrpm)
    {
        
        if (amOrpm == "am") {
            logOutTime = time;
        }
        else
            logOutTime = time + 12;
     
    }
    //now this function will calculate the working hours
    //rendered hours
    double getHoursOfWork()
    {
        int hrs = 0;     
            hrs = logOutTime - logInTime;
        return hrs;
    }
//this will return the employe number as a string
    string getEmpNo()
    {
        return empNo;
    }
    //already stored values in setemployee function
    //on the basis of which the type will be decided
    void PrintEmployees()
    {
        cout << "Name : " << name << endl;
        cout << "Emloyee Number : " << empNo << endl;
        if (empType == 1)
        {
            cout << "Designation : OFFICER " << endl;
        }
        else if (empType == 2)
        {
            cout << "Designation : SUPERVISOR " << endl;
        }
        else if (empType == 3)
        {
            cout << "Designation : utility " << endl;
        }

    }
};
//this another class is declared for the purpose of registration
//of the employee
class EmployeeRegistration
{
    //private access specifier used to keep data from access directly in main
private:
//this employee pointer is used to store the address of first class employee
//this employee pointer is used to create the class array as we dont know the size 
//the size may vary every time so thats why we will work with dynamic memory allocation
//private attributes
    Employee* employees;
    int EmpTypes1;
    int EmpTypes2;
    int EmpTypes3;
    int numRegisteredEmp;
    int maxEmp;
public:
//accessing the private members
    EmployeeRegistration(int _maxEmp)
    {
        EmpTypes1 = 0;
        EmpTypes2 = 0;
        EmpTypes3 = 0;

        numRegisteredEmp = 0;
        maxEmp = _maxEmp;
        //this is dynamically allocated array of class
        employees = new Employee[maxEmp];

    }
//this function will be used to store data of employees
//as the size of maximum employes would have been already specified
    void registerEmployee()
    {
       
        int j = 0;
        for (int i = 0; i < maxEmp; i++)
        {
            string name, empNo;
            int empType;
            //these are data for registration
            cout << "Name: ";
            cin >> name;
            cout << "Employee No: ";
            cin >> empNo;
            cout << "Employee Type:" << endl;
            cout << "[1] Office Staff" << endl;
            cout << "[2] Supervisory" << endl;
            cout << "[3] Utility" << endl;
            cout << "Choose Type: ";
            cin >> empType;
        //this condition is applied for every employe type because there is restriction
        //in the given task that only 5 employees can be registered of every 3 type
            if (empType == 1)
            {
                if (EmpTypes1 > 5) 
                {
                    cout << "you should never enter more officers vancy is filled" << endl;
                    cout << "choose again Employee Type:" << endl;
                    cout << "[1] Office Staff" << endl;
                    cout << "[2] Supervisory" << endl;
                    cout << "[3] Utility" << endl;
                    cout << "Choose Type: ";
                    cin >> empType;
                }
                //emptype counters are used to keep the track of employee count
                EmpTypes1++;
            }
            else if (empType == 2)
            {
                if (EmpTypes2 > 5)
                {
                    cout << "you should never enter more officers vancy is filled" << endl;
                    cout << "choose again Employee Type:" << endl;
                    cout << "[1] Office Staff" << endl;
                    cout << "[2] Supervisory" << endl;
                    cout << "[3] Utility" << endl;
                    cout << "Choose Type: ";
                    cin >> empType;
                }
                EmpTypes2++;
            }
            else if (empType == 3)
            {
                if (EmpTypes3 > 5)
                {
                    cout << "you should never enter more officers vancy is filled" << endl;
                    cout << "choose again Employee Type:" << endl;
                    cout << "[1] Office Staff" << endl;
                    cout << "[2] Supervisory" << endl;
                    cout << "[3] Utility" << endl;
                    cout << "Choose Type: ";
                    cin >> empType;
                }
                EmpTypes3++;
            }
          //this will be a useful key because if somehow data is incorrect 
          //user can unsave data
          //class index will move to next if save option is selected otherwise no increment
            char save;
            cout << "enter save[Y/N]: ";
            cin >> save;
            if (save == 'y' || save == 'Y')
            {
                employees[j].SetEmployee(name, empNo, empType);
                j++;
                numRegisteredEmp++;
            }
            else
            {
                maxEmp++;
            }
            //system cls command is used to clear screen after very iteration
            system("cls");
        }
        
    }
    //in this function only employe number is recieved as parameter
    //because all the data will processed on the basis of unique id numbers
    void LogInSystem(string empNum)
    {
        bool found = false;
        char select;
        int saveindex = 0;
        int inTime = 0;
        int outTime = 0;
        int workHrs = 0;
        string amPm;
        //this loop will go through each employee data if any match is found 
        //further operations will be performed
        for (int i = 0; i < maxEmp; i++)
        {
            if (employees[i].getEmpNo() == empNum)
            {
                found = true;
                saveindex = i;
                break;
            }
        }
        //the screen will be cleared
        system("cls");
        //if the employee has been found the portal will be opened 
        //three options will be given for log in, log out and end
        if (found == true)
        {
        jump1:
            cout << "\n Employee Number: " << empNum << endl << endl;;
            cout << "select only this options " << endl;
            cout << "\n [A] - Log-in ";
            cout << "\n [B] - Log out ";
            cout << "\n [E] - for Exit ";
            cout << "enter choice :" << endl;
            cin >> select;
        //these if-else are used for different scenarios of log in,log out and exit options
            if (select == 'A' || select == 'a')
            {
                cout << endl << "..................LOG IN PAGE..................." << endl;
                cout << "morning for enter 'am' and noon for enter'pm' : ";
                cin >> amPm;
                cout << "enter Login time: ";
                cin >> inTime;
        //here the employee class array has been called 
        //in class array the log in function is called where the time and am/pm is passes as arguments
                employees[saveindex].logIn(inTime,amPm);
                system("cls");
            //goto is used because after log in maybe employe wants to select log out option
                goto jump1;
            }
            //this is the log out page 
            else if (select == 'b' || select == 'B')
            {
                cout << endl << "..................LOG OUT PAGE..................." << endl;
                cout << "morning for enter 'am' and noon for enter'pm' : ";
                cin >> amPm;
                cout << "enter LogOut time: ";
                cin >> outTime;
                //class employee array is called again here its used to calculate the total render time
                employees[saveindex].logOut(outTime,amPm);
                workHrs = employees[saveindex].getHoursOfWork();
                cout << "You rendered " << workHrs << "hours of service today." << endl << endl << endl;
            }
         //this option will be used for exiting the portal
            else if (select == 'e' || select == 'E')
            {
            system("cls");
            return;
            }
          
         }
       //if the unique id number is incorrect so no operations performed
        else 
        {
            cout << "the employee with" << empNum << "does not have any employee record" << endl;
        }
    }
    //this print function can be used to print the data of employee as employee type
    void Print()
    {
        for (int i = 0; i < maxEmp; i++)
        {
            employees[i].PrintEmployees();
            cout << endl;
            cout << endl;
        }
        cout << endl;
        cout << endl;
    }
  
};
//here the main function has begin
int main()
{
//for decoration of portal layout
    cout << "*************************\n\n\n";
    cout << "              Welcome to Employee Registration System                 \n\n";
    cout << "*******        MENU        ***********\n\n";
    int size = 0;
    cout << "enter total number of employee you want register" << endl;
    cin >> size;
    //this is the second class defined above where the size is passed as an argument to
    //decide what will be the size of first class array
    //obj is object defined
    EmployeeRegistration obj(size);
jump:
    cout << "1.Register" << endl;
    cout << "2.Log-in" << endl;
    cout << "3 print" << endl;
    cout << "4 exit" << endl;
    int choice = 0;
    cout << "\nEnter your choice :";
    //now different functions have been made in above classes to perform specific task
    //so these if else will let user decide what function has to be called and from which class
    cin >> choice;

    if (choice == 1)
    {
       
        obj.registerEmployee();
        obj.Print();
    }
    else if (choice == 2)
    {
        string empnum;
        cout << "enter the empNo for login system" << endl;
        cin >> empnum;
        obj.LogInSystem(empnum);
    }
    if (choice == 3)
    {
        obj.Print();
    }
    else if (choice == 4)
    {
        cout << "exit........" << endl << endl;
        return 0;
    }
 //this goto will be used because the portal will remain on and lets user enter input to decide
 //what they want to do login,print,registration and exit
 //if the goto was not used it would have exited program after end
        goto jump;
  

}