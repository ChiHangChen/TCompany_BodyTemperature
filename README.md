# TCompany_BodyTemperature
每天都要填寫體溫實在是太麻煩了

## Environment setting (Python 3)

套件要求 (install with `pip install pkgname`): 

 - datetime
 
 - time
 
 - numpy
 
 - requests 
 
 - bs4
 
 - schedule

## How to use

#### Step 1:
更改 `TCompany_BodyTemperature.py` 中的 : 

 1. EmployeeID (工號)
 
 2. trigger_time (程式每日觸發時間)

#### Step 2:
在 Windows cmd 中或 Linux Terminal 執行 `python TCompany_BodyTemperature.py`後放著不要管它，每天時間一到就會自動填表