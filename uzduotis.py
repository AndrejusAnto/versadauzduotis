import csv
import calendar
import datetime

lines = []
lines_numb = 0
email_numb = 0
email_list = []
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
                        email_list.append(line[1])
                    
        else:
            print("File is empty")
    else:
        print("Can't open file")

if lines_numb == email_numb:
    print(len(email_list), email_list)