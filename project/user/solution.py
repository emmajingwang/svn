import os
from email.mime.application import MIMEApplication
from fileinput import filename
import os, subprocess,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def svn(svn_address,username,password,package,email,project,branchNum):
#def svn(svn_address,email,package,project,branchNum):
    os.chdir('C:')
    
    #create a new dir if it not exists
    dir_path="C:/svn-tests2"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    #go to target dir to checkout svn projects
    os.chdir(dir_path)
    
    output=''
    results=''
    foundPackage=''
    #package choice as condition 
    #if using npm package, do npm check. otherwise,do nuget check
    if package =='npm':
        os.system('svn checkout https://' + svn_address+'/svn/'+project)
        #go to the target project client dir to test npm package
        newDir = 'C:/svn-tests2/'+project+'/client'
        os.chdir(newDir)

        #save the results as string
        results = subprocess.getoutput("npm audit report")
         
    else:
        
        if(username=="" or password==""):
            os.system ('svn checkout https://' + svn_address + '/svn/' +project +' --username '+username+' --password '+password)
        else:   
            os.system('svn checkout https://' + svn_address+'/svn/'+project+'/'+project+'-'+branchNum)
        
        path=dir_path+'/'+project
        path2=path+'/packagereferences.csproj'
        
        #call to run the powershell script to create the packagereferences
        os.system('powershell C:/svn/svn/dotnet '+ path +' '+path2)
        
        #check any packages not installed yet
        path3=path+'/'+project+'-'+branchNum+'/src/'+project +'/packages'
        
        foundPackage=subprocess.getoutput('powershell C:/svn/svn/check '+ path2+' '+path3)
       
        os.chdir(path)
        os.system('dotnet restore')
        
        #save results as a string 
        results=subprocess.getoutput("dotnet list package --vulnerable")

    output += project+': \n\n' +foundPackage +'\n\n'+ results + '\n\n\n' 
    #create a txt file to save the output
    try:
        with open('C:/svn-tests2/report.txt','w') as f:
            f.write(output)
    except FileNotFoundError:
        print("Report not exists.")
    f.close

    #send results by email
    sender = 'emma.wang@gov.bc.ca'
    receivers=email

    #create an instance of EmailMessage
    message = MIMEMultipart()

    #store the senders, receivers, subject and body of the email
    message['From'] = sender
    message['To'] = receivers
    message['Subject'] = 'test for SVN'
    body="Hello, please check out the attachement for the report of your projects"

    #attach the body with the message instance
    message.attach(MIMEText(body, 'plain'))

    #open the file to be sent
    filename='C:/svn-tests2/report.txt'
    attachment=open(filename,'rb')

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    #attach to the message
    message.attach(p)

    try:
        #create SMTP session
        smtpObj = smtplib.SMTP('apps.smtp.gov.bc.ca')

        smtpObj.sendmail(sender,receivers,message.as_string())        
        print ("Successfully sent email")
        
    except smtplib.SMTPException:
        print ("Error: unable to send email") 

    #terminating the session
    smtpObj.quit()