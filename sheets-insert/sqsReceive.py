import datetime
import json
import dateutil.tz
import gspread

def receiveMessageHandler(event, context):
    try:
        print(event)
        # json 파일이 위치한 경로를 값으로 줘야 합니다.
        json_file_path = "optical-bond-347104-39356a6af60c.json"
        gc = gspread.service_account(json_file_path)
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1InUZrKBUz6lnY9xqOSxms660txnx1nCawbaUeitV8kA/edit#gid=1805506674"
        doc = gc.open_by_url(spreadsheet_url)
        worksheet = doc.worksheet("테스트")

        for record in event["Records"]:
            body = json.loads(record["body"])
            name = body["name"]
            number = body["number"]
            ins_person_id = body["ins_person_id"]
            last_row = len(worksheet.get_all_values()) + 1
            range = 'A'+ str(last_row) + ':D' + str(last_row)
            korea_now = datetime.datetime.now(dateutil.tz.gettz('Asia/Seoul'))
            date_now = str(korea_now.year) + "-" + str(korea_now.month) + "-" + str(korea_now.day)
            worksheet.update(range,[[date_now,name,number,ins_person_id]])
    except Exception as inst:
        print(inst)
        return {
            "status": "FAIL",
            "value": "-",
            "message": "오류가 발생했습니다.."
        }
    