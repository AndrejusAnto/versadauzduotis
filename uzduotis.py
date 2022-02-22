import csv
import calendar
from datetime import date

lines = []
lines_numb = 0
email_numb = 0
all_emails = {}
filename = 'C:\\Users\\Admin\\Desktop\\versada\\birthdays.csv'
# filename = "C:\\Users\\Admin\\Desktop\\versada\\birthdays2.csv"
with open(filename, newline='') as csvfile:
    if csvfile:
        lines = [l for idx, l in enumerate(csv.reader(csvfile)) if idx != 0]
        lines_numb = len(lines)
        if(lines_numb != 0):
            for line in lines:
                if (line[0] == '') or (line[1] == '') or (line[2] == ''):
                    print("Name, email or date is missing, please check ;)")
                else:
                    bday = line[2].split("-")
                    dayok = calendar.monthrange(int(bday[0]),int(bday[1]))[1]
                    if (int(bday[2]) <= dayok) and (int(bday[1]) > 0) and (int(bday[1]) < 13): 
                        email_numb +=1
                        all_emails.update({line[1]:[line[0], [int(bday[0]), int(bday[1]), int(bday[2])]]})
                    
        else:
            print("File is empty")
    else:
        print("Can't open file")

def send_email(email, name, bname, bday, delta):
    if (bday[1] < 10) or (bday[2] < 10):
        birthday = f"{bday[0]}-0{bday[1]}-0{bday[2]}"
    else:
        birthday = f"{bday[0]}-{bday[1]}-{bday[2]}"
    print(f"Sedning email to {email}")
    print(f"Subject: Birthday Reminder: {bname}'s birthday on {birthday}")
    print("Body:")
    print(f"Hi {name}")
    print(f"This is a reminder that {bname} will be celebrating their birthday on {birthday}.")
    print(f"There are {delta} days left to get a present!")

send_no = []
send_yes = []
if lines_numb == email_numb:
    for k, v in all_emails.items():
        dateinfo = v[1]
        today = date.today()
        year = date.today().year
        dbday = date(year, *dateinfo[1:])
        delta = dbday - today
        delta = delta.days
        if delta == 7:
            send_no.append([*v, delta])
        else:
            send_yes.append([k, *v[:-1]])

if send_no and send_yes:    
    for y in send_yes:
        for n in send_no:
            send_email(y[0], y[1], n[0], n[1], n[2])