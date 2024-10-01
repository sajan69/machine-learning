import requests
import xlwt
from xlwt import Workbook
import smtplib
import os.path
# import basename  # This line is incorrect and should be removed
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

BASE_URL = "https://remoteok.com/api/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0"
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.5"
}

def get_jobs_postings():
    res = requests.get(BASE_URL, headers=REQUEST_HEADERS)
    return res.json()

def output_jobs_postings_to_xls(data):
    wb=Workbook()
    job_sheet=wb.add_sheet('Jobs')
    
    headers = data[0].keys()
    for i in range(0, len(headers)):
        #TypeError: 'dict_keys' object is not subscriptable
        job_sheet.write(0, i, list(headers)[i])
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for j in range(0, len(values)):
            job_sheet.write(i+1, j, values[j])

    wb.save('remoteok_jobs.xls')

def send_email(send_from, send_to,subject,text,files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(send_from, 'qpur gyui tgrz plhb')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


    

if __name__ == '__main__':
    json= get_jobs_postings()[1:]
    output_jobs_postings_to_xls(json)
    send_email('sajanac46@gmail.com', ['sajanac83@gmail.com'], 'Remote Jobs', 'Please find the attached file', files=['remoteok_jobs.xls'],)
