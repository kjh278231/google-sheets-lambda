import json
import gspread
import datetime
import re

def check_duplicated_data(all_Data,name,number):
    for line in all_Data:
        if line[1] == name and line[2] == number :
            return False
        if len(line[2]) >= 8 and len(number) >= 8:
            if line[2][-8:] == number[-8:]:
                return False
    return True

def validationNumber(event,context):
    try:
        print(event)
        number = json.loads(event["body"])['value']['origin']
        print(context)
        number = filteringNumber(number)
        if len(str(number)) < 8:
            return {
                "status": "FAIL",
                "value": "-",
                "message": "형식을 맞춰 다시 입력해주세요.\n"
            }
        return {
            "status": "SUCCESS",
            "value": str(number),
            "message": "감사합니다."
        }
    except Exception as inst:
        return {
            "status": "FAIL",
            "value": "-",
            "message": "오류가 발생했습니다.."
        }

def filteringNumber(number):
    number = str.replace(number,"-","")
    number = str.replace(number,".","")
    number = re.sub(r'[^0-9\+]', '', number)
    print(number)
    return number

def hello(event, context):
    try:
        param = json.loads(event["body"])["action"]["params"]
        print(json.loads(event["body"]))
        name = param["name"]
        number = filteringNumber(param['number'])
        ins_person_id = json.loads(event["body"])["bot"]["name"]

        # json 파일이 위치한 경로를 값으로 줘야 합니다.
        json_file_path = "optical-bond-347104-39356a6af60c.json"
        gc = gspread.service_account(json_file_path)
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1InUZrKBUz6lnY9xqOSxms660txnx1nCawbaUeitV8kA/edit#gid=1805506674"
        doc = gc.open_by_url(spreadsheet_url)

        worksheet = doc.worksheet("WI총계(현물+선물)")

        all_Data = worksheet.get_all_values()
        last_row = len(all_Data) + 1
        range = 'A'+ str(last_row) + ':D' + str(last_row)
        date_now = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
        worksheet.update(range,[[date_now,name,number,ins_person_id]])
        return {
            "version":"2.0",
            "template":
                {"outputs":[{"simpleText":{"text":"확인했습니다. 순차적으로 무료 입장 도와 드리도록 하겠습니다. \n\n많은 분들의 입장을 도와드리고 있다 보니, 시간이 다소 지연되더라도 양해 부탁 드립니다. ^^"}}]}
        }
    except Exception as inst:
        print(inst)
        return {
        "version":"2.0",
        "template":
            {"outputs":[{"simpleText":{"text":"오류가 발생했습니다."}}]}
        }       