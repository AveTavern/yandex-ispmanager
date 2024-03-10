import requests
from datetime import datetime, timedelta 
import time

# Настройки времени
delta_from = 1
delta_to = 1
current_date = datetime.now()
current_date = str(current_date)
#print("Now is "+current_date)
current_date = datetime.now() - timedelta(days=delta_from)
date_from = current_date.date()
date_from_str = str(date_from)
date_from_req = ''+date_from_str+''
#print("Date from "+date_from_req)
current_date2 = datetime.now() - timedelta(days=delta_to)
date_to = current_date2.date()
date_to_str = str(date_to)
date_to_req = ''+date_to_str+''
#print("Date to "+date_to_req)

# Импорт модуля работы с google sheets
import gspread
gs = gspread.service_account(filename='URL to service account file')  
sh = gs.open_by_key('open key')

# Импорт кред для доступа к Яндекс Метрики
API_token = 'OAuth AUTH'
counter_id = 'ID'
api_metrika_url = 'https://api-metrika.yandex.net/stat/v1/data/bytime'

# Формирование запроса в Яндекс Метрику
params = {
   'date1': date_from_req, 
   'date2': date_to_req, 
   'group' : 'day',
   'dimensions' : 'ym:s:lastsignTrafficSource',
   'ids' : counter_id,
   'metrics': 'ym:s:visits', 
    }
res = requests.get(api_metrika_url, params = params, headers={'Authorization': API_token})
#print(res.text)
#print("")

# Разбираем полученный запрос по составляющим для внедрения в таблицу.
json_res = res.json()  # Превращение ответа в Python native object.
data = json_res["data"] # Оставляем в ответе только данные, убирая информацию о запросе.
#print(data)
#print("")

# Добавляем в техническую таблицу источники трафика
a = 2 #строчка
b = 1 #столбик
for metrics in data: 
    dimensions = metrics["dimensions"]
    for id in dimensions:
        name = id["name"]
        #print(name)
        worksheet = sh.worksheet("tech")
        worksheet = worksheet.update_cell(a, b, name)
        a += 1
        
# Добавляем в техническую таблицу значение трафика
a = 2
for dimensions in data:
    metrics = dimensions["metrics"]
    for id in metrics:
        #print(id)
        b = current_date.day+1
        for key in id:
            #print(key)
            worksheet = sh.worksheet("tech")
            worksheet = worksheet.update_cell(a, b, key)
            b += 1
            #print("middle", b)
        a += 1
        #print("last", a)
        #print("last", b)
        
# Сравнение источников трафика между технической и актуальной таблицей        
worksheet = sh.worksheet("current")
gs_val_current = worksheet.col_values(1)
gs_val_current.remove("Current month")
i2 = 0
a = 2
for word in gs_val_current:
    worksheet = sh.worksheet("tech")
    gs_val_tech = worksheet.col_values(1)
    i = 0
    for word in gs_val_tech:
        #print("current / tech", gs_val_tech[i], "/", gs_val_current[i2] )
       # print("i", i, "i2", i2)
        if  gs_val_tech[i] == gs_val_current[i2]:
            a = i+1
            gs_val_transfer = worksheet.cell(a, 2).value
            worksheet = sh.worksheet("current")
            b = current_date.day
           # print(a, b, gs_val_transfer)
            a = i2+2
            worksheet = worksheet.update_cell(a, b, gs_val_transfer)
        i += 1
    i2 += 1
