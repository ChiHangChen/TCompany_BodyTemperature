import datetime
import time
import numpy as np
import requests 
from bs4 import BeautifulSoup
import schedule

# 工號
EmployeeID = "000000"
# 程式每日觸發時間(每日填表時間)
trigger_time = "08:00"



print("--------------程式執行中--------------")
base_url = 'https://zh.surveymonkey.com/r/EmployeeHealthCheck'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}
params = {
    "ssrc": "head",
    "returnurl": "https://zh.surveymonkey.com/r/HCCompleted",
}
def get_data(EmployeeID, temperature, survey_data, start_time, end_time):
    data = {
        '486014833': '3209788694',
        '486014830': EmployeeID,
        '486014835': '3209788698',
        '486014831': temperature,
        '486015076': '3209796414',
        '486014832': '3209788684',
        'survey_data': survey_data,
        'response_quality_data': {"question_info":{"qid_486014834":{"number":-1,"type":"presentation_text","option_count":None,"has_other":False,"other_selected":None,"relative_position":None,"dimensions":None,"input_method":None,"is_hybrid":False},"qid_486014833":{"number":1,"type":"single_choice_vertical","option_count":1,"has_other":False,"other_selected":None,"relative_position":[[0,0]],"dimensions":[1,1],"input_method":None,"is_hybrid":False},"qid_486014830":{"number":2,"type":"open_ended","option_count":None,"has_other":False,"other_selected":None,"relative_position":None,"dimensions":None,"input_method":"text_typed","is_hybrid":True},"qid_486014835":{"number":3,"type":"single_choice_vertical","option_count":3,"has_other":False,"other_selected":None,"relative_position":[[0,0]],"dimensions":[3,1],"input_method":None,"is_hybrid":False},"qid_486014831":{"number":4,"type":"open_ended","option_count":None,"has_other":False,"other_selected":None,"relative_position":None,"dimensions":None,"input_method":"text_typed","is_hybrid":True},"qid_486014836":{"number":-1,"type":"presentation_text","option_count":None,"has_other":False,"other_selected":None,"relative_position":None,"dimensions":None,"input_method":None,"is_hybrid":False},"qid_486015076":{"number":5,"type":"single_choice_vertical","option_count":2,"has_other":False,"other_selected":None,"relative_position":[[1,0]],"dimensions":[2,1],"input_method":None,"is_hybrid":False},"qid_486014832":{"number":6,"type":"single_choice_vertical","option_count":1,"has_other":False,"other_selected":None,"relative_position":[[0,0]],"dimensions":[1,1],"input_method":None,"is_hybrid":False}},"start_time":start_time,"end_time":end_time,"time_spent":760313,"previous_clicked":False,"has_backtracked":False,"bi_voice":{}},
        'is_previous': False,
        'disable_survey_buttons_on_submit':''
    }
    return data



def main():
    session = requests.session()
    soup = BeautifulSoup(session.get(base_url).content, "html.parser")
    survey_data = soup.find(id="survey_data")['value']
    start_time = round(time.time())
    end_time = start_time+15120
    temperature = round(np.random.uniform(36.3,37.1),1)
    data = get_data(EmployeeID, temperature, survey_data, start_time, end_time)
    response = session.post(base_url, data=data, headers=headers, params=params)
    if response.history:
        print("-----------填表完成-----------")
        print("填表時間 : {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        print("工號 : {}".format(EmployeeID))
        print("體溫 : {}".format(temperature))
    else:
        print("-----------填表失敗-----------")
        print("Please report this issue to https://github.com/ChiHangChen/TCompany_BodyTemperature/issues")

def print_rest_time():
    now_datetime = datetime.datetime.now()
    now_str = now_datetime.strftime("%Y-%m-%d %H:%M")
    today_trigger = now_str[:11]+"{:02d}".format(int(trigger_time.split(":")[0]))
    today_trigger += ":"+trigger_time.split(":")[1]
    today_trigger_datetime = datetime.datetime.strptime(today_trigger,"%Y-%m-%d %H:%M")
    now_datetime = datetime.datetime.now()
    if now_datetime > today_trigger_datetime:
        tom_trigger_datetime = today_trigger_datetime+datetime.timedelta(days=1)
        trigger_delta = (tom_trigger_datetime-now_datetime).seconds
    else:
        trigger_delta = (today_trigger_datetime-now_datetime).seconds
    trigger_delta_hour = trigger_delta/3600
    trigger_delta_minutes = int((trigger_delta_hour-int(trigger_delta_hour))*60)
    print("距離下次填表時間還有 : {} 小時 {} 分鐘".format(int(trigger_delta_hour),trigger_delta_minutes))
    
if __name__=="__main__":
    print_interval = 5 # minute
    schedule.every().day.at(trigger_time).do(main)
    now = datetime.datetime.now()-datetime.timedelta(minutes = 5)
    while True:
        schedule.run_pending()
        if (datetime.datetime.now()-now).seconds/60 >= print_interval:
            print_rest_time()
            now = datetime.datetime.now()
        time.sleep(30)
