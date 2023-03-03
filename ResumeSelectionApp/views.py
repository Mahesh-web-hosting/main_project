from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as mplt
from pyresparser import ResumeParser
from django.shortcuts import redirect
import random
import smtplib

global uname, email_id, otp, email, password, contact, name, address, utype

def CreateResume(request):
    if request.method == 'GET':
       return redirect("https://makecvforfree.com/app/")

def CompanyLogin(request):
    if request.method == 'GET':
       return render(request, 'CompanyLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def Aboutus(request):
    if request.method == 'GET':
       return render(request, 'Aboutus.html', {})

def OTPValidation(request):
    if request.method == 'POST':
        global otp, email, password, contact, name, address, utype
        usr_otp = request.POST.get('t1', False)
        status = "OTP validation Failed"
        if int(usr_otp) == otp:
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'resumeselection',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(email_id,password,contact_no,name,address,usertype) VALUES('"+email+"','"+password+"','"+contact+"','"+name+"','"+address+"','"+utype+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Signup Process Completed & OTP Validation Successful'
        context= {'data':status}
        return render(request, 'Signup.html', context)        

def sendMail(to_email, message):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        emailAddress = 'cse19c@gmail.com'
        emailPassword = 'printfscanf'
        connection.login(emailAddress, emailPassword)
        connection.sendmail(from_addr = "cse19c@gmail.com", to_addrs = to_email, msg = message)

def SignupAction(request):
    if request.method == 'POST':
        global otp, email, password, contact, name, address, utype
        email = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        name = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        utype = request.POST.get('t6', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'sqluser', password = 'password', database = 'resumeselection',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select email_id from signup where email_id = '"+email+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == email:
                    status = 'Given Username already exists'
                    break
        if status == 'none':
            otp = random.randint(1000,9999)            
            sendMail(email, "OTP for Account Verification "+str(otp))
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'sqluser', password = 'password', database = 'resumeselection',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(email_id,password,contact_no,name,address,usertype) VALUES('"+email+"','"+password+"','"+contact+"','"+name+"','"+address+"','"+utype+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Signup Process Completed & OTP Validation Successful'
        context= {'data':status}
        return render(request, 'Signup.html', context)
        

def UserLoginAction(request):
    if request.method == 'POST':
        global uname, email_id
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'sqluser', password = 'password', database = 'resumeselection',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password and row[5] == 'User':
                    uname = row[3]
                    email_id = row[0]
                    option = 1
                    break
        if option == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def CompanyLoginAction(request):
    if request.method == 'POST':
        global uname, email_id
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'sqluser', password = 'password', database = 'resumeselection',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup")
            rows = cur.fetchall()
            for row in rows:
                print(str(row)+" "+username+" "+password)
                if row[0] == username and row[1] == password and row[5] == 'Company':
                    uname = row[3]
                    email_id = row[0]
                    option = 1
                    break
        if option == 1:
            context= {'data':'welcome '+username}
            return render(request, 'CompanyScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'CompanyLogin.html', context)          

def ResumeSelection(request):
    if request.method == 'GET':
       return render(request, 'ResumeSelection.html', {})

def AnalyseResume(request):
    if request.method == 'GET':
       return render(request, 'AnalyseResume.html', {})    

def getScore(require_skills, skills):
    #require_skills = ['c', 'java', 'cpp', 'javascript']
    score = 0
    for i in range(len(skills)):
        skills[i] = skills[i].lower().strip()
        if skills[i] == 'c++':
            skills[i] = 'cpp'
    found_skills = [x for x in skills if x in require_skills]
    if len(found_skills) > 0:
        if len(found_skills) >= len(require_skills):
            score = 100
        else:
            score = len(found_skills) / len(require_skills)
            score = score * 100
    return score       

def ResumeSelectionAction(request):
    if request.method == 'POST':
        global uname
        require_skills = request.POST.get('t1', False)
        require_skills = require_skills.split(",")
        for i in range(len(require_skills)):
            require_skills[i] = require_skills[i].lower().strip()
            if require_skills[i] == 'c++':
                require_skills[i] = 'cpp'
        percentage = float(request.POST.get('t2', False))
        for afile in request.FILES.getlist('t3'):
            if os.path.exists("ResumeSelectionApp/static/resumes/"+afile.name):
                os.remove("ResumeSelectionApp/static/resumes/"+afile.name)
            fs = FileSystemStorage()
            fs.save("ResumeSelectionApp/static/resumes/"+afile.name, afile)
            print(afile.name)
        output = '<table border=1><tr>'
        output+='<td><font size="" color="black">Applicant Name</td>'
        output+='<td><font size="" color="black">Email id</td>'
        output+='<td><font size="" color="black">Phone number</td>'
        output+='<td><font size="" color="black">Require Skills</td>'
        output+='<td><font size="" color="black">Found Skills</td>'
        output+='<td><font size="" color="black">Found %</td></tr>'
        for root, dirs, directory in os.walk('ResumeSelectionApp/static/resumes'):
            for j in range(len(directory)):
                data = ResumeParser(root+"/"+directory[j]).get_extracted_data()
                skills = data['skills']
                name=data['name']
                mail=data['email']
                ph_no=data['mobile_number']
                score = getScore(require_skills, skills)
                print(str(score)+" "+str(require_skills)+" "+str(skills))
                if score >= percentage:
                    output+='<tr>'
                    output+='<td><font size="" color="black">'+str(name)+'</td>'
                    output+='<td><font size="" color="black">'+str(mail)+'</td>'
                    output+='<td><font size="" color="black">'+str(ph_no)+'</td>'
                    output+='<td><font size="" color="black">'+str(require_skills)+'</td>'
                    output+='<td><font size="" color="black">'+str(skills)+'</td>'
                    output+='<td><font size="" color="black">'+str(score)+'</td></tr>'
        output += "</table><br/><br/><br/><br/><br/><br/>"            
        context= {'data':output}
        return render(request, 'CompanyScreen.html',context)
        
def AnalyseResumeAction(request):
    if request.method == 'POST':
        global uname
        given_name = request.POST.get('t1', False)
        given_mail = request.POST.get('t2', False)
        given_ph_no = request.POST.get('t3', False)
        require_skills = request.POST.get('t4', False)
        require_skills = require_skills.split(",")
        for i in range(len(require_skills)):
            require_skills[i] = require_skills[i].lower().strip()
            if require_skills[i] == 'c++':
                require_skills[i] = 'cpp'
        myfile = request.FILES['t5']
        fname = request.FILES['t5'].name
        fs = FileSystemStorage()
        if os.path.exists("ResumeSelectionApp/static/resumes/"+fname):
            os.remove("ResumeSelectionApp/static/resumes/"+fname)
        filename = fs.save('ResumeSelectionApp/static/resumes/'+fname, myfile)
        data = ResumeParser('ResumeSelectionApp/static/resumes/'+fname).get_extracted_data()
        skills = data['skills']
        name=data['name']
        mail=data['email']
        ph_no=data['mobile_number']
        score = round(getScore(require_skills, skills))
        skill_score=round((score*40)//100)
        final_score=0
        if(str.upper(name)==str.upper(given_name)):
            final_score+=20
            nf="Found"
        else:
            nf="Not Found"
        if(str(mail)==str(given_mail)):
            final_score+=20
            ef="Found"
        else:
            ef="Not Found"
        if(ph_no==given_ph_no):
            final_score+=20
            pf="Found"
        else:
            pf="Not Found"
        final_score+=skill_score
        #context= {'data':"Name :"+nf+"Email_id :"+ef+" Phone number :"+pf+" Skill percentage :"+str(score)+"Finally your Resume Score is : "+str(final_score)+"To get better score use our resume creator"}
        output = '<table border=1><tr>'
        output+='<td><font size="" color="black">Applicant Name</td>'
        output+='<td><font size="" color="black">Email id</td>'
        output+='<td><font size="" color="black">Phone number</td>'
        output+='<td><font size="" color="black">Skill score</td>'
        output+='<td><font size="" color="black">Total score</td>'
        output+='<tr>'
        output+='<td><font size="" color="black">'+nf+'</td>'
        output+='<td><font size="" color="black">'+ef+'</td>'
        output+='<td><font size="" color="black">'+pf+'</td>'
        output+='<td><font size="" color="black">'+str(score)+'</td>'
        output+='<td><font size="" color="black">'+str(final_score)+'</td></tr>'
        output+='<tr rowspan="4"><font size="" color="black">'+'To get better score use our resume creator'+'</tr>'
        output += "</table><br/><br/><br/><br/><br/><br/>" 
        context= {'data':output}
        return render(request, 'UserScreen.html',context)
















        

