# import gspread
# import re
# import datetime

# def check_duplicated_data(all_Data,name,number):
#     for line in all_Data:
#         if line[1] == name and line[2] == number :
#             return False
#     return True

# # json 파일이 위치한 경로를 값으로 줘야 합니다.
# json_file_path = "optical-bond-347104-39356a6af60c.json"
# gc = gspread.service_account(json_file_path)
# spreadsheet_url = "https://docs.google.com/spreadsheets/d/1InUZrKBUz6lnY9xqOSxms660txnx1nCawbaUeitV8kA/edit#gid=1805506674"
# doc = gc.open_by_url(spreadsheet_url)

# worksheet = doc.worksheet("테스트총계")
# ins_person_id = "주인계정"
# name = "테스트"
# number = "01000000000"

# all_Data = worksheet.get_all_values()
# print(all_Data)

# if(check_duplicated_data(all_Data,name,number)):
#     last_row = len(all_Data) + 1
#     currentTime = datetime.datetime.now()
#     range = 'A'+ str(last_row) + ':D' + str(last_row)
#     worksheet.update(range,[["2014-01-13",name,number,ins_person_id]])
# else:
#     print('Fail...')

# # def validatePhoneNumber(phoneNumber):
# #     newPhoneNumber = str.replace(phoneNumber,"-","")
# #     fianlPhoneNumber = str.replace(newPhoneNumber,".","")
# #     patter_first = r"010([0-9]{8})"
# #     if(re.findall(patter_first,fianlPhoneNumber)!= [] or len(fianlPhoneNumber)>=9):
# #         return True,fianlPhoneNumber;
# #     return False,"";

# # result,number = validatePhoneNumber("010.1234.5678")
# # print(result)
# # print(number)