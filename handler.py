import json
import gspread
import datetime

def check_duplicated_data(all_Data,name,number):
    for line in all_Data:
        if line[1] == name and line[2] == number :
            return False
    return True

def hello(event, context):
    try:
        param = json.loads(event["body"])["action"]["params"]
        name = param["name"]
        number = param["number"]

        # json 파일이 위치한 경로를 값으로 줘야 합니다.
        json_file_path = "wired-torus-351301-ad2ef6a9e623.json"
        gc = gspread.service_account(json_file_path)
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1SZRkaAGJQM7BWFw3Vxj_LetIBimhAhpgPhMjqmq17Uw/edit#gid=0"
        doc = gc.open_by_url(spreadsheet_url)

        worksheet = doc.worksheet("제출 명단")
        ins_person_id = "주인계정"

        all_Data = worksheet.get_all_values()
        if(check_duplicated_data(all_Data,name,number)):
            last_row = len(all_Data) + 1
            currentTime = datetime.datetime.now().date
            range = 'A'+ str(last_row) + ':D' + str(last_row)
            worksheet.update(range,[["2014-01-13",name,number,ins_person_id]])
            return {
                "version":"2.0",
                "template":
                    {"outputs":[{"simpleText":{"text":"hello I'm "+name +": "+number}}]}
            }
        else:
            return {
                "version":"2.0",
                "template":
                    {"outputs":[{"simpleText":{"text":"이미 등록된 정보입니다. 다시 확인해주세요."}}]}
            }
    except Exception as inst:
        print(inst)
        return {
        "version":"2.0",
        "template":
            {"outputs":[{"simpleText":{"text":"오류가 발생했습니다."}}]}
        }       

