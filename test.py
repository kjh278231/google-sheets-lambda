import gspread
import datetime

def check_duplicated_data(all_Data,name,number):
    for line in all_Data:
        if line[1] == name and line[2] == number :
            return False
    return True

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "wired-torus-351301-ad2ef6a9e623.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1SZRkaAGJQM7BWFw3Vxj_LetIBimhAhpgPhMjqmq17Uw/edit#gid=0"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("제출 명단")
ins_person_id = "주인계정"
name = "김지훈"
number = "01062598538"

all_Data = worksheet.get_all_values()
if(check_duplicated_data(all_Data,name,number)):
    last_row = len(all_Data) + 1
    currentTime = datetime.datetime.now()
    range = 'A'+ str(last_row) + ':D' + str(last_row)
    worksheet.update(range,[["2014-01-13",name,number,ins_person_id]])
else:
    print('Fail...')
