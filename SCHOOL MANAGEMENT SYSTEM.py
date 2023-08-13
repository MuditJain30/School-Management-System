#CS PROJECT PREPARED BY MUDIT JAIN AND NAMIT MEHROTRA(XII-B)-SCHOOL MANAGEMENT SYSTEM--------------------------------------------------

#TO HIDE PASSWORD FROM USER
import getpass
password=getpass.getpass(prompt='enter mysql password')

import random 
import datetime

#TO ESTABLISH CONNECTION BETWEEN MYSQL AND PYTHON
import mysql.connector as co 
mycon=co.connect(host="localhost", user="root", passwd=password,charset='utf8')
mycur=mycon.cursor()

#createdatabase-----------------------------------------------------------------------------------------------------------------------
def createdatabase():
    try:
        query='create database school_management'
        mycur.execute(query)
    except:
        print("")
    query2='use school_management'
    mycur.execute(query2)
createdatabase()

#createtables-------------------------------------------------------------------------------------------------------------------------
def createtablestudent():
    try:
        query='create table student(AdNo varchar(20) primary key,StudentName varchar(50),Class varchar(10),\
        RollNo int(10),DOB varchar(15),Email varchar(50),FatherName varchar(50),\
        MotherName varchar(50),Address varchar(50),MobileNumber bigint not null,\
        Dues int(10) default 0,ClassTeacher varchar(50),DateOfAdmission varchar(15))'
        mycur.execute(query)
    except:
        print("")

def createtablefees():
    try:
        query='create table studentfee(adno varchar(20) primary key,name varchar(50),amount int(10),mode varchar(10),\
        dateofpayment varchar(15))'
        mycur.execute(query)
    except:
        print("")

def createtableteacher():
    try:
        query='CREATE TABLE teacher(ID int(10) primary key,Name varchar(120) ,Email varchar(120),\
        MobileNumber bigint(10),Qualifications varchar(120),\
        Address varchar(200),TeacherSub varchar(120),\
        JoiningDate varchar(15),Department varchar(20),ClassAllotted varchar(10))'
        mycur.execute(query)
    except:
        print('')
        
createtablestudent()
createtablefees()
createtableteacher()

#code for auto increment of every months fees in student table-------------------------------------------------------------------------
def count():
    d=datetime.datetime.today()
    x=str(d.month)
    filename='count_data'+x
    try:
        with open(filename) as fin:
            i=fin.readline()
            k=fin.readline()
            j=int(i)
            l=int(k)
    except IOError:
        j=0
        l=d.month
    j+=1
    with open(filename,'w') as fout:
        fout.write(str(j))
        fout.write(str(l))
    #this checks that fees don't get add multiple times
    while j==1:
        query=("select * from student")
        mycur.execute(query)
        data=mycur.fetchall()
        for i in data:
            Class=i[2]
            AdNo=i[0]
            x=Class.split()
            #this will add fees of respective class to the dues column in student table
            if x[0]=='1' or x[0]=='2' or x[0]=='3' or x[0]=='4' or x[0]=='5':
                q="update student set Dues=Dues+5000 where AdNo='%s'"%(AdNo)
                mycur.execute(q)
                mycon.commit()
            elif x[0]=='6' or x[0]=='7' or x[0]=='8':
                q="update student set Dues=Dues+5500 where AdNo='%s'"%(AdNo)
                mycur.execute(q)
                mycon.commit()
            elif x[0]=='9' or x[0]=='10' or x[0]=='11' or x[0]=='12':
                q="update student set Dues=Dues+6000 where AdNo='%s'"%(AdNo)
                mycur.execute(q)
                mycon.commit()
            else:
                print('something is wrong,check again')
count()
#fee menu-----------------------------------------------------------------------------------------------------------
def FEE_MENU():
    print("\t\t.............................................")	
    print("\t\t*****Welcome to School Management System*****")  
    print("\t\t.............................................")	
    print("\n\t\t*****Fee Menu*****")
    print('1.FEE DEPOSIT')
    print('2.RETURN TO MAIN MENU')
    tday=datetime.date.today()
    print("TODAY'S DATE: ",tday)
    x=int(input('ENTER THE CHOICE:'))
    if x==1:
        fee_deposit()
    elif x==2:
        MAIN_MENU()
    else:
        print('ERROR:INVALID CHOICE TRY AGAIN')
        FEE_MENU()

def fee_deposit():
    AdNo=input('enter admission no.:')
    s=datetime.datetime.now()
    y=s.strftime("%Y")
    m=s.strftime("%m")
    a=s.strftime("%d")
    d=y+'-'+m+'-'+a
    query=("select * from student where AdNo='%s'"%(AdNo))
    mycur.execute(query)
    data=mycur.fetchone()
    name=data[1]
    Class=data[2]
    x=Class.split()
    #to display the particulars of the student
    print('ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:',data[3],
          '\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:',data[7],
          '\n','ADDRESS:',data[8],'\n','MOBILE NUMBER:',data[9])
    if x[0]=='1' or x[0]=='2' or x[0]=='3' or x[0]=='4' or x[0]=='5':
        print('THE FEE FOR CLASS',data[2],'IS:\nTUITION FEE=RS.4000\nDEVELOPMENT CHARGES=RS.500\nOTHER\
              CHARGES=RS.500\nTOTAL FEE=RS5000')
        print('YOUR PREVIOUS DUES ARE:',data[10]-5000)
        print('YOUR CURRENT DUES ARE:',data[10])
        ans=input('DO YOU WANT TO PAY FEES<y/n>:')
        if ans=='y':
            ok=input('DO YOU WANT TO PAY ALL THE DUES:<y/n>')
            if ok=='y':
                amount=data[10]
                mode=input('ENTER MODE OF PAYMENT:<cash,online,cheque,card>')
                q=("insert into studentfee(adno,name,amount,mode,dateofpayment) values('{}','{}',{},'{}','{}')\
                   ").format(AdNo,name,amount,mode,d)
                mycur.execute(q)
                mycon.commit()
                print('FEES FOR',data[1],'SUBMITTED SUCCESSFULLY')
                q1="update student set Dues=0 where AdNo='%s'"%(AdNo)
                mycur.execute(q1)
                mycon.commit()
                #code to create the fees slip as a text file which can be printed for manual records
                filename=data[0],'.txt'
                a=listtostring(filename)
                file=open(a,'w')
                w=('*****DAV Public School*****','\n','FEE SLIP FOR MONTH:',m,'\n',\
                'ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:'\
                ,data[3],'\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:'\
                ,data[7],'\n','ADDRESS',data[8],'\n','MOBILE NUMBER:',data[9],'\n','THE FEE FOR CLASS',data[2],\
                'IS:\nTUITION FEE=RS.4000\nDEVELOPMENT CHARGES=RS.500\nOTHER CHARGES=RS.500\nTOTAL FEE=RS5000\
                \nLATE FEE=______\nYOUR PREVIOUS DUES ARE:',data[10]-5000,'\n','YOUR CURRENT DUES ARE:',data[10])
                str1=''.join(map(str,w))
                file.write(str1)
                file.close()
            elif ok==n:
                amount=int(input('ENTER THE AMOUNT YOU WANT TO DEPOSIT'))
                mode=input('ENTER MODE OF PAYMENT:<cash,cheque,online,card>')
                q=("insert into studentfee(adno,name,amount,mode,dateofpayment) values('{}','{}',{},'{}','{}')\
                ").format(AdNo,name,amount,mode,d)
                mycur.execute(q)
                mycon.commit()
                remaining=data[10]-amount
                q1="update student set Dues=%s where AdNo='%s'"%(remaining,AdNo)
                mycur.execute(q1)
                mycon.commit()
                print('FEES FOR',data[1],'SUBMITTED SUCCESSFULLY')
                #code to create the fees slip as a text file which can be printed for manual records
                filename=data[0],'.txt'
                a=listtostring(filename)
                file=open(a,'w')
                w=('*****DAV Public School*****','\n','FEE SLIP FOR MONTH:',m,'\n',\
                'ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:'\
                ,data[3],'\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:'\
                ,data[7],'\n','ADDRESS',data[8],'\n','MOBILE NUMBER:',data[9],'\n','THE FEE FOR CLASS',data[2],\
                'IS:\nTUITION FEE=RS.4000\nDEVELOPMENT CHARGES=RS.500\nOTHER CHARGES=RS.500\nTOTAL FEE=RS5000\
                \nLATE FEE=______\nYOUR PREVIOUS DUES ARE:',data[10]-5000,'\n','YOUR CURRENT DUES ARE:',data[10])
                str1=''.join(map(str,w))
                file.write(str1)
                file.close()
            else:
                print('wrong input')
        elif ans=='n':
            MAIN_MENU()
        else:
            print('wrong input')
    elif x[0]=='6' or x[0]=='7' or x[0]=='8':
        print('THE FEE FOR CLASS',data[2],'IS:\nTUITION FEE=RS.4500\nDEVELOPMENT CHARGES=RS.500\nOTHER\
              CHARGES=RS.500\nTOTAL FEE=RS5500')
        print('YOUR PREVIOUS DUES ARE:',data[10]-5500)
        print('YOUR CURRENT DUES ARE:',data[10])
        ans=input('DO YOU WANT TO PAY FEES<y/n>:')
        if ans=='y':
            ok=input('DO YOU WANT TO PAY ALL THE DUES:<y/n>')
            if ok=='y':
                amount=data[10]
                mode=input('ENTER MODE OF PAYMENT:<cash,online,cheque,card>')
                q=("insert into studentfee(adno,name,amount,mode,dateofpayment) values('{}','{}',{},'{}','{}'\
                   )").format(AdNo,name,amount,mode,d)
                mycur.execute(q)
                mycon.commit()
                print('FEES FOR',data[1],'SUBMITTED SUCCESSFULLY')
                q1="update student set Dues=0 where AdNo='%s'"%(AdNo)
                mycur.execute(q1)
                mycon.commit()
                #code to create the fees slip as a text file which can be printed for manual records
                filename=data[0],'.txt'
                a=listtostring(filename)
                file=open(a,'w')
                w=('*****DAV Public School*****','\n','FEE SLIP FOR MONTH:',m,'\n',\
                'ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:'\
                ,data[3],'\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:'\
                ,data[7],'\n','ADDRESS:',data[8],'\n','MOBILE NUMBER:',data[9],'\n','THE FEE FOR CLASS',data[2],\
                'IS:\nTUITION FEE=RS.4500\nDEVELOPMENT CHARGES=RS.500\nOTHER CHARGES=RS.500\nTOTAL FEE=RS5500\
                \nLATE FEE=______\nYOUR PREVIOUS DUES ARE:',data[10]-5500,'\n','YOUR CURRENT DUES ARE:',data[10])
                str1=''.join(map(str,w))
                file.write(str1)
                file.close()
            elif ok=='n':
                amount=int(input('ENTER THE AMOUNT YOU WANT TO DEPOSIT'))
                mode=input('ENTER MODE OF PAYMENT:<cash,cheque,online,card>')
                q=("insert into studentfee(adno,name,amount,mode,dateofpayment) values('{}','{}',{},'{}','{}')\
                   ").format(AdNo,name,amount,mode,d)
                mycur.execute(q)
                mycon.commit()
                remaining=data[10]-amount
                q1="update student set Dues=%s where AdNo='%s'"%(remaining,AdNo)
                mycur.execute(q1)
                mycon.commit()
                print('FEES FOR',data[1],'SUBMITTED SUCCESSFULLY')
                #code to create the fees slip as a text file which can be printed for manual records
                filename=data[0],'.txt'
                a=listtostring(filename)
                file=open(a,'w')
                w=('*****DAV Public School*****','\n','FEE SLIP FOR MONTH:',m,'\n',\
                'ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:'\
                ,data[3],'\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:',\
                data[7],'\n','ADDRESS:',data[8],'\n','MOBILE NUMBER:',data[9],'\n','THE FEE FOR CLASS',data[2],\
                'IS:\nTUITION FEE=RS.4500\nDEVELOPMENT CHARGES=RS.500\nOTHER CHARGES=RS.500\nTOTAL FEE=RS5500\
                \nLATE FEE=______\nYOUR PREVIOUS DUES ARE:',data[10]-5500,'\n','YOUR CURRENT DUES ARE:',data[10])
                str1=''.join(map(str,w))
                file.write(str1)
                file.close()
            else:      
                print('wrong input')
        elif ans=='n':
            MAIN_MENU()
        else:
            print('wrong input')
    elif x[0]=='9' or x[0]=='10' or x[0]=='11' or x[0]=='12':
        print('THE FEE FOR CLASS',data[2],'IS:\nTUITION FEE=RS.5000\nDEVELOPMENT CHARGES=RS.500\n\
              OTHER CHARGES=RS.500\nTOTAL FEE=RS6000')
        print('YOUR PREVIOUS DUES ARE:',data[10]-6000)
        print('YOUR CURRENT DUES ARE:',data[10])
        ans=input('DO YOU WANT TO PAY FEES<y/n>:')
        if ans=='y':
            ok=input('DO YOU WANT TO PAY ALL THE DUES:<y/n>')
            if ok=='y':
                amount=data[10]
                mode=input('ENTER MODE OF PAYMENT:<cash,online,cheque,card>')
                q=("insert into studentfee(adno,name,amount,mode,dateofpayment) values('{}','{}',{},'{}','{}')\
                ").format(AdNo,name,amount,mode,d)
                mycur.execute(q)
                mycon.commit()
                print('FEES FOR',data[1],'SUBMITTED SUCCESSFULLY')
                q1="update student set Dues=0 where AdNo='%s'"%(AdNo)
                mycur.execute(q1)
                mycon.commit()
                #code to create the fees slip as a text file which can be printed for manual records
                filename=data[0],'.txt'
                a=listtostring(filename)
                print(a)
                file=open(a,'w')
                w=('*****DAV Public School*****','\n','FEE SLIP FOR MONTH:',m,'\n',\
                'ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:'\
                ,data[3],'\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:',\
                 data[7],'\n','ADDRESS:',data[8],'\n','MOBILE NUMBER:',data[9],'\n','THE FEE FOR CLASS',data[2],\
                'IS:\nTUITION FEE=RS.5000\nDEVELOPMENT CHARGES=RS.500\nOTHER CHARGES=RS.500\nTOTAL FEE=RS6000\
                \nLATE FEE=______\nYOUR PREVIOUS DUES ARE:',data[10]-6000,'\n','YOUR CURRENT DUES ARE:',data[10])
                str1=''.join(map(str,w))
                file.write(str1)
                file.close()
            elif ok=='n':
                amount=int(input('ENTER THE AMOUNT YOU WANT TO DEPOSIT'))
                mode=input('ENTER MODE OF PAYMENT:<cash,cheque,online,card>')
                q=("insert into studentfee(adno,name,amount,mode,dateofpayment) values('{}','{}',{},'{}','{}')\
                ").format(AdNo,name,amount,mode,d)
                mycur.execute(q)
                mycon.commit()
                remaining=data[10]-amount
                q1="update student set Dues=%s where AdNo='%s'"%(remaining,AdNo)
                mycur.execute(q1)
                mycon.commit()
                print('FEES FOR',data[1],'SUBMITTED SUCCESSFULLY')
                #code to create the fees slip as a text file which can be printed for manual records
                filename=data[0],'.txt'
                a=listtostring(filename)
                file=open(a,'w')
                w=('*****DAV Public School*****','\n','FEE SLIP FOR MONTH:',m,'\n',\
                'ADMISSION NUMBER:',data[0],'\n','NAME:',data[1],'\n','CLASS:',data[2],'\n','ROLL NO:'\
                ,data[3],'\n','DOB:',data[4],'\n','EMAIL:',data[5],'\n','FATHER NAME:',data[6],'\n','MOTHER NAME:',\
                data[7],'\n','ADDRESS:',data[8],'\n','MOBILE NUMBER:',data[9],'\n','THE FEE FOR CLASS',data[2],\
                'IS:\nTUITION FEE=RS.5000\nDEVELOPMENT CHARGES=RS.500\nOTHER CHARGES=RS.500\nTOTAL FEE=RS6000\
                \nLATE FEE=______\nYOUR PREVIOUS DUES ARE:',data[10]-6000,'\n','YOUR CURRENT DUES ARE:',data[10])
                str1=''.join(map(str,w))
                file.write(str1)
                file.close()
            else:
                print('wrong input')
        elif ans=='n':
            MAIN_MENU()
        else:
            print('wrong input')
    else:
        print('wrong input')

#to convert a list or tupple to a string
def listtostring(s):
    str1=''
    for ele in s:
        str1+=ele
        return str1

#-------------------------------------------------------------------------------------------------------------------------------------
#STUDENT MENU-------------------------------------------------------------------------------------------------------------------------
def STUDENT_MENU():
    while True:
        print("\t\t.............................................")	
        print("\t\t*****Welcome to School Management System*****")  
        print("\t\t.............................................")	
        print("\n\t\t*****STUDENT MENU*****")
        print("1: ADD DETAILS OF NEW STUDENT")
        print("2: SHOW DETAILS OF ALL STUDENTS")
        print("3: SEARCH DETAILS OF STUDENT")
        print("4: DELETION OF RECORDS OF STUDENT")
        print("5: UPDATE DETAILS OF STUDENT")
        print("6: RETURN")
        print("\t\t--------------------------------------------")	
        tday=datetime.date.today()
        print("TODAY'S DATE: ",tday)
        choice=int (input ("Enter your choice"))
        if choice==1:
            add_student_details()
        elif choice==2:
            show_student_details()
        elif choice==3:
            search_student_details()
        elif choice==4: 
            delete_student_details()
        elif choice==5: 
            edit_student_details()
        elif choice==6:
            return
        else:
            print("Error: Invalid Choice try again.....")
            _MENU()

def add_student_details():
    AdNo=random.getrandbits(16)   #to create students unique admission number
    print('STUDENT ADMISSION NUMBER=',AdNo)
    StudentName=input('Enter student name:')
    Class=input('Enter student class:')
    RollNo=int(input('Enter student roll number:'))
    DOB=input('Enter student DOB:<YYYY-MM-DD>')
    Email=input('Enter student email:')
    FatherName=input('Enter student father name:')
    MotherName=input('Enter student mother name:')
    Address=input('Enter student address:')
    MobileNumber=input('Enter students mobile number:')
    if len(MobileNumber)!=10:    #to check that a valid mobile number is entered or not
        print('Enter valid mobile number!')
        MobileNumber=input('Enter students mobile number:')
    q="select Name from teacher where ClassAllotted='%s'"%(Class)
    mycur.execute(q)
    ClassTeacher=mycur.fetchone()
    a=listtostring(ClassTeacher)
    print('Class Teacher is:',a)   #to find the class teacher using students class
    DOA=input('Enter DATE OF ADMISSION:<YYYY-MM-DD>')
    query="insert into student(AdNo,StudentName,Class,RollNo,DOB,Email,FatherName,MotherName,Address,MobileNumber,ClassTeacher,DateOfAdmission) values('{}','{}','{}',{},'{}','{}','{}','{}','{}',{},'{}','{}')".format(AdNo,StudentName,Class,RollNo,DOB,Email,FatherName,MotherName,Address,MobileNumber,a,DOA)
    mycur.execute(query)
    mycon.commit()
    print('Record has been saved in student table')

def show_student_details():
    mycur.execute("select * from student")
    data=mycur.fetchall() 
    for row in data:
        print(row)

def search_student_details():
    print('1.SEARCH USING ADMISSION NUMBER')
    print('2.SEARCH USING NAME')
    print('3.SEARCH USING CLASS')
    print('4.SEARCH USING MOBILE NUMBER')
    print('5.RETURN')
    ch=int(input('Enter choice:'))
    if ch==1:
        ac=input('Enter Student Admission Number:')
        st="select * from student where AdNo='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print(data)
    elif ch==2:
        ac=input('Enter Student Name:')
        st="select * from student where StudentName='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print(data)
    elif ch==3:
        ac=input('Enter Student Class:')
        st="select * from student where Class='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print(data)
    elif ch==4:
        ac=input('Enter Student Moblie Number:')
        st="select * from student where MobileNumber='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print(data)
    elif ch==5:
        return
    else:
        print("Error: Invalid Choice try again.....")
        search_teacher_details()

def delete_student_details():
    ac=input('Enter Student Admission No:')
    st="delete from student where AdNo='%s'"%(ac)
    mycur.execute(st)   
    mycon.commit()
    print ('Data deleted successfully') 

def edit_student_details():
    print("1: Edit Student Name") 
    print("2: Edit Class") 
    print("3: Edit Roll No.")
    print("4: Edit DOB") 
    print("5: Edit Email") 
    print("6: Edit Father Name")
    print("7: Edit Mother Name") 
    print("8: Edit Address") 
    print("9: Edit Mobile No.")
    print("10: Return")
    print("\t\t--------------------------------------------")
    choice=int(input("Enter your choice"))
    if choice==1:
        ac=input('Enter Admission no:')
        nm=input('Enter correct name:')
        st="update student set StudentName='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==2:
        ac=input('Enter Admission no:')
        nm=input('Enter correct class:')
        st1="update student set Class='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st1)
        mycon.commit()
        x="select Name from teacher where ClassAllotted='%s'"%(nm)   #to edit the name of class teacher as well
        mycur.execute(x)
        ClassTeacher=mycur.fetchone()
        a=listtostring(ClassTeacher)
        print('New Class Teacher is:',a)
        st2="update student set ClassTeacher='%s' where AdNo='%s'"%(a,ac)
        mycur.execute(st2)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==3:
        ac=input('Enter Admission no:')
        nm=input('Enter correct RollNo:')
        st="update student set RollNo=%s where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==4:
        ac=input('Enter Admission no:')
        nm=input('Enter correct DOB:<YYYY-MM-DD>')
        st="update student set DOB='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==5:
        ac=input('Enter Admission no:')
        nm=input('Enter correct Email:')
        st="update student set Email='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==6:
        ac=input('Enter Admission no:')
        nm=input('Enter correct Father Name:')
        st="update student set FatherName='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==7:
        ac=input('Enter Admission no:')
        nm=input('Enter correct Mother Name:')
        st="update student set MotherName='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==8:
        ac=input('Enter Admission no:')
        nm=input('Enter correct Address:')
        st="update student set Address='%s' where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==9:
        ac=input('Enter Admission no:')
        nm=input('Enter correct MobileNo.:')
        st="update student set MobileNumber=%s where AdNo='%s'"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==10:
        return
    else:
        print("Error: Invalid Choice try again.....")
        edit_admin_details()

#teachersmenu-------------------------------------------------------------------------------------------------------------------------
def TEACHER_MENU():
    while True:
        print("\t\t.............................................")	
        print("\t\t*****Welcome to School Management System*****")  
        print("\t\t.............................................")	
        print("\n\t\t*****Teacher Menu*****")
        print("1.ADD NEW TEACHER'S RECORD")
        print('2.SHOW ALL TEACHER DETAILS')
        print('3.SEARCH TEACHER RECORD')
        print('4.DELETE TEACHER RECORD')
        print('5.EDIT TEACHER RECORD')
        print('6.RETURN')
        print('-------------------------------------------------')
        tday=datetime.date.today()
        print("TODAY'S DATE: ",tday)
        c=int(input('enter your choice:'))
        if c==1:
            add_teacher_details()
        elif c==2:
            show_teacher_details()
        elif c==3:
            search_teacher_details()
        elif c==4:
            delete_teacher_details()
        elif c==5:
            edit_teacher_details()
        elif c==6:
            MAIN_MENU()
        else:
            print('ERROR:INVALID CHOICE TRY AGAIN')
            TEACHERS_MENU()

def add_teacher_details():
    ID=random.getrandbits(16)     #to generate teachers unique id
    print('TEACHER ID=',ID)    
    Name=input('Enter name of teacher:')
    Email=input('Enter teachers email:')
    MobileNumber=input('Enter teachers mobile number:')    #to check if the mobile number is valid or not
    if len(MobileNumber)!=10:
        print('Enter valid mobile number!')
        MobileNumber=input('Enter teachers mobile number:')
    Qualifications=input('Enter teachers qualifications:')
    Address=input('Enter teachers address:')
    TeacherSub=input("Enter teacher's subject:")
    JoiningDate=input("Enter teacher's joining date:<YYYY-MM-DD>")
    Department=input('Enter teachers department:<primary/middle/senior/senior secondary>')
    ClassAllotted=input("Enter Class Allotted to the teacher:<default none>")
    query="insert into teacher(ID,Name,Email,MobileNumber,Qualifications,Address,TeacherSub,JoiningDate,Department\
    ,ClassAllotted) values({},'{}','{}',{},'{}','{}','{}','{}','{}','{}')".format\
    (ID,Name,Email,MobileNumber,Qualifications,Address,TeacherSub,JoiningDate,Department,ClassAllotted)
    mycur.execute(query)
    mycon.commit()
    print('Record has been saved in teacher table')

def show_teacher_details():
    mycur.execute("select * from teacher")
    data=mycur.fetchall() 
    for row in data:
        print(row)

def search_teacher_details():
    print('1.SEARCH USING ID')
    print('2.SEARCH USING NAME')
    print('3.SEARCH USING TEACHER SUBJECT')
    print('4.SEARCH USING CLASS ALLOTTED')
    print("5: Return")
    ch=int(input('Enter choice:'))
    if ch==1:
        ac=int(input('Enter ID:'))
        st="select * from teacher where ID=%s"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print (data)
    elif ch==2:
        ac=input("Enter teacher's name:")
        st="select * from teacher where Name='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print (data)
    elif ch==3:
        ac=input('Enter teacher subject:')
        st="select * from teacher where Teachersub='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print (data)
    elif ch==4:
        ac=input("Enter teacher's Alloted Class:")
        st="select * from teacher where ClassAllotted='%s'"%(ac)
        mycur.execute(st)
        data=mycur.fetchall()
        print (data)
    elif ch==5:
        return
    else:
        print("Error: Invalid Choice try again.....")
        search_teacher_details()

def delete_teacher_details():
    ac=int(input('Enter teacher ID:'))
    st="delete from teacher where ID=%s"%(ac)
    mycur.execute(st)   
    mycon.commit()
    print ('Data deleted successfully')

def edit_teacher_details():
    print("1: Edit Name:") 
    print("2: Edit Email:") 
    print("3: Edit Mobile Number:")
    print("4: Edit Qualifications:")
    print("5: Edit Address:")
    print("6: Edit Teacher Subject:")
    print("7: Edit DateofJoining:")
    print("8: Return")
    print("\t\t--------------------------------------------")
    choice=int(input("Enter your choice"))
    if choice==1:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct name:')
        st="update teacher set Name='%s' where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==2:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct email:')
        st="update teacher set Email='%s' where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==3:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct mobile number:')
        st="update teacher set MobileNumber=%s where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==4:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct qualifications:')
        st="update teacher set Qualifications='%s' where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==5:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct address:')
        st="update teacher set address='%s' where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==6:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct teacher subject:')
        st="update teacher set TeacherSub='%s' where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==7:
        ac=int(input('Enter teacher ID:'))
        nm=input('Enter correct dateofjoining:<YYYY-MM-DD>')
        st="update teacher set JoiningDate='%s' where ID=%s"%(nm,ac)
        mycur.execute(st)
        mycon.commit()
        print ('Data updated successfully')
    elif choice==8:
        return
    else:
        print("Error: Invalid Choice try again.....")
        edit_teacher_details()

#--------------------------------------------------------------------------------------------------------------------------------------
#ADMIN MENU----------------------------------------------------------------------------------------------------------------------------
def ADMIN_MENU():
    while True:
        print("\t\t.............................................")
        print("\t\t*****Welcome to School Management System*****")
        print("\t\t.............................................")
        print("\n\t\t*****ADMIN MENU*****")
        print("1: TOTAL NEW ADMISSIONS THIS MONTH")
        print("2: TOTAL NEW ADMISSIONS THIS YEAR")
        print("3: TOTAL FEES COLLECTED THIS MONTH")
        print("4: TOTAL FEES COLLECTED THIS YEAR")
        print("5: LIST OF ALL FEE DEFAULTERS")
        print("6: EXIT")
        print("\t\t.............................................")
        choice=int(input("Enter your choice"))
        if choice==1:
            admissionthismonth()
        elif choice==2:
            admissionthisyear()
        elif choice==3:
            feescollectedthismonth()
        elif choice==4:
            feescollectedthisyear()
        elif choice==5:
            Q='select AdNo,StudentName,Class,MobileNumber,Dues from student where Dues>15000'
            #if dues>15000,student is considered as fee defaulter
            mycur.execute(Q)
            data=mycur.fetchall()
            if data==[]:
                print('NO FEE DEFAULTER')
            else:
                print(data)
        elif choice==6:
            MAIN_MENU()
        else:
            print("Error: Invalid Choice try again.....")	
            ADMIN_MENU()

def admissionthismonth():    #to count number of new admissions this month
    count=0
    d=datetime.datetime.today()
    y=d.strftime("%Y")
    m=d.strftime("%m")
    q='select DateOfAdmission from student'
    mycur.execute(q)
    data=mycur.fetchall()
    for i in data:
        a=listtostring(i)
        if int(a[0:4])==y:
            if int(a[5:7])==m:
                count+=1
    print('TOTAL NEW ADMISSIONS TAKEN THIS MONTH ARE:',count)

def admissionthisyear():    #to count number of new admissions this year
    count=0
    d=datetime.datetime.today()
    y=d.strftime("%Y")
    q='select DateOfAdmission from student'
    mycur.execute(q)
    data=mycur.fetchall()
    for i in data:
        a=listtostring(i)
        if int(a[0:4])==y:
            count+=1
    print('TOTAL NEW ADMISSIONS TAKEN THIS YEAR ARE:',count)
    
def feescollectedthismonth():   #to calculate total fees collected this month
    d=datetime.datetime.today()
    y=d.strftime("%Y")
    m=d.strftime("%m")
    x=y+'-'+m
    print(x)
    q="select SUM(amount) from studentfee where dateofpayment LIKE '{}%'".format(x)
    mycur.execute(q)
    data=mycur.fetchone()
    print('TOTAL FEES COLLECTED THIS MONTH IS:',data)
    
def feescollectedthisyear():    #to calculate total fees collected this year
    d=datetime.datetime.today()
    y=d.strftime("%Y")
    q="select SUM(amount) from studentfee where dateofpayment LIKE '{}%'".format(y)
    mycur.execute(q)
    data=mycur.fetchone()
    print('TOTAL FEES COLLECTED THIS YEAR IS:',data)
    
#---------------------------------------------------------------------------------------------------------------------
#MAIN MENU------------------------------------------------------------------------------------------------------------
def MAIN_MENU():
    while True:
        print("\t\t.............................................")
        print("\t\t*****Welcome to School Management System*****")
        print("\t\t.............................................")
        print("\n\t\t*****DAV Public School*****")
        print("1: STUDENT DETAILS")
        print("2: FEE DETAILS")
        print("3: TEACHER DETAILS")
        print("4: ONLY ADMIN RECORDS")
        print("5: EXIT")
        print("\t\t.............................................")
        tday=datetime.date.today()
        print("TODAY'S DATE: ",tday)
        choice=int(input("Enter your choice"))
        if choice==1:
            STUDENT_MENU()
        elif choice==2:
            FEE_MENU()
        elif choice==3:
            TEACHER_MENU()
        elif choice==4:
            print('YOU NEED PASSWORD TO OPEN THIS MENU') #only an admin have access to this menu
            passwd=getpass.getpass(prompt='ENTER PASSWORD:')    #to hide password from the user
            if passwd=='ABC':
                ADMIN_MENU()
        elif choice==5:
            break
        else:
            print("Error: Invalid Choice try again.....")	
            MAIN_MENU()

MAIN_MENU()
#--------------------------------------------------------------------------------------------------------------------------------------
