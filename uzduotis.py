import csv
import calendar
from datetime import date
import sys
import smtplib, ssl
import os
from sqlitedict import SqliteDict

# email server:
# python -m smtpd -c DebuggingServer -n localhost:1025

# The script should have two commands/options:

# option check: 1.validate the persons birthday data file, print errors (if found)
# python uzduotis.py check C:\Users\Admin\Desktop\versada\birthdays.csv

# option send: 2.check for upcoming birthdays and send emails if there are any. Exit once emails are sent.
# python uzduotis.py send C:\Users\Admin\Desktop\versada\birthdays.csv

nosend = []
sendto = []

# paprastas serveris patikrinti emailų siuntimą per localhost
port = 1025  # For starttls
smtp_server = "localhost"
sender_email = "andrejusantoninovas@gmail.com"

options = sys.argv[1:]
filename = options[1]

db_name = "bdays.sqlite"
db_filename = os.getcwd() + "\\" + db_name

def check_file(fname):
	lines_numb = 0
	email_numb = 0
	db = SqliteDict("bdays.sqlite")
	with open(fname, newline='') as csvfile:
		if csvfile:
			lines = [l for idx, l in enumerate(csv.reader(csvfile)) if idx != 0]
			lines_numb = len(lines)
			if(lines_numb != 0):
				for line in lines:
					if (line[0] == '') or (line[1] == '') or (line[2] == ''):
						db.close()
						return "Name, email or date is missing, please check ;)"
					else:
						bday = line[2].split("-")
						dayok = calendar.monthrange(int(bday[0]),int(bday[1]))[1]
						if ((int(bday[2]) > 0) and (int(bday[2]) <= dayok)) and ((int(bday[1]) > 0) and (int(bday[1]) < 13)): 
							db[line[1]] = [line[0], [int(bday[0]), int(bday[1]), int(bday[2])]]
							email_numb +=1
							if lines_numb == email_numb:
								return db
						else:
							db.close()
							return f"Date is wrong, check {' '.join(line)}"

						
			else:
				db.close()
				return "File is empty"
		else:
			db.close()
			return "Can't open file"

def message_form(name, bname, bday, delta):
	if (bday[1] < 10) or (bday[2] < 10):
		bday = f"{bday[0]}-0{bday[1]}-0{bday[2]}"
	else:
		bday = f"{bday[0]}-{bday[1]}-{bday[2]}"
	sub = f"Subject: Birthday Reminder: {bname}'s birthday on {bday}\n\n"
	body = f"Hi {name}\nThis is a reminder that {bname} will be celebrating their birthday on {bday}."
	end = f"\nThere are {delta} days left to get a present!"
	msg = sub + body + end
	return msg

def find_bdays(db_emails):
	for k, v in db_emails.items():
		dateinfo = v[1]
		today = date.today()
		year = date.today().year
		dbday = date(year, *dateinfo[1:])
		delta = dbday - today
		delta = delta.days
		if delta == 7:
			nosend.append([*v, delta])
		else:
			sendto.append([k, *v[:-1]])

def send_email(sno, syes):
	with smtplib.SMTP(smtp_server, port) as server:
		if sno and syes:
			for y in syes:
				for n in sno:
					message = message_form(y[1], n[0], n[1], n[2])
					server.sendmail(sender_email, y[0], message)
		else:
			print("No one's birthday is comming in a week")

if(options[0] == "check"):
	if os.path.exists(db_name):
		os.remove(db_filename)

	if_file = check_file(filename)
	if type(if_file) != str:
		if_file.commit()
		if_file.close()
		print("Finished, no errors, now you can use 'send' option")
	else:
		os.remove(db_filename)
		print(if_file)

if(options[0] == "send"):
	if os.path.exists(db_name):
		db = SqliteDict(db_name)
		find_bdays(db)
		send_email(nosend, sendto)

		# čia tam, kad matyųsi gimtadininkai (žiūrėti gif'ą)
		for bd in nosend:
			print(bd)
		print("Emails has been sent successfully")
	else:
		print("You have to check the file")
		print('Please use "check" option')