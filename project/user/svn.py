# solution for npm package check only
from email.mime.application import MIMEApplication
from fileinput import filename
import os, subprocess,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def svn(repo_ip,email):
    os.chdir('C:')
    #create a new dir if it not exists
    dir_path="C:/svn-tests"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
    #create an arr to include all prjects 
    projects=['schoolbus','hmcr','hets']
    output=''

    #checkout the target project
    for project in projects:
        #go to target dir to checkout svn projects
        os.chdir(dir_path)
        os.system (('svn checkout https://' + repo_ip + '/svn/{}').format(project))
       
        #go to the target project client dir to test npm package
        newDir = 'C:/svn-tests/{}/client'.format(project)
        os.chdir(newDir)

        #save the results as string
        results = subprocess.getoutput("npm audit report")
        output+='{}: '.format(project) + results + '\n\n\n'
        
        #create a txt file to save the output
    try:
        with open('report.txt','w') as f:
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
    filename='report.txt'
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
        smtpObj = smtplib.SMTP('<email protocol>')

        smtpObj.sendmail(sender,receivers,message.as_string())        
        print ("Successfully sent email")
        
    except smtplib.SMTPException:
        print ("Error: unable to send email") 

    #terminating the session
    smtpObj.quit()
       
    