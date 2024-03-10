import subprocess
import requests

cmd = 'pip'+' install'+' gspread'
subprocess.run([cmd], shell=True)

cmd = 'pip'+' install'+' datetime'
subprocess.run([cmd], shell=True)

cmd = 'pip'+' install'+' time'
subprocess.run([cmd], shell=True)

url  = 'https://raw.githubusercontent.com/AveTavern/yandex-ispmgr/main/yandex-ispmgr'
response = requests.get(url)
with open ('/var/www/yandex.py', 'w+') as file:
  file.write(response.text)
  file.close()
print("Создан файл yandex.py в директории /var/www/")
    
cmd = '/usr/local/mgr5/sbin/mgrctl -m ispmgr scheduler.edit active=on clicked_button=ok command=/var/www/yandex.py description=yandex_metrics sok=ok'
subprocess.run([cmd], shell=True)
print("Создана задача в cron")
