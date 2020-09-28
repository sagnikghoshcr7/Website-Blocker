import os, time, ctypes, sys
from datetime import datetime as dt

host = r'etc\hosts' if os.name == 'posix' else r'C:\Windows\System32\drivers\etc\hosts' 

redirect = "127.0.0.1"
website_list = []

try:
    with open(os.path.dirname(os.path.realpath(__file__))+'\sitelist.txt','r') as f:
        f.seek(0)
        website_list = f.readlines()

except:
    print("Please make a sitelist.txt file which containes websites list 'one site / line'\n\n")
website_list=list(map(lambda x:x.strip('\n'), website_list))
precision = 5
timer = [
        00,00, #from hour, minutes 
        00,00 #to hour, minutes
        ]

def get_time():
    print("Enter time duration. Eg. '13 25 15 30' for from 1:25 PM to 3:30 PM")
    for i in range(4):
        x=input().strip()
        if x == '\n' or x == '':
            continue
        else:
            timer[i] = int(x)
        


def run_blocker():
    print("Blocker Starting...")
    
    print('''
        Details:
            Time: {}:{} to {}:{}
            Websites: {}
            redirect: {}
            precision: {}
        '''.format(
        timer[0], timer[1], 
        timer[2], timer[3], 
        website_list,
        redirect,
        precision
        )
    )
    print("After closing the program re-run the program without entring time will unblock websites")
    while True:
        d = dt.now()
        if dt(d.year, d.month, d.day,timer[0],timer[1]) < d < dt(d.year, d.month, d.day, timer[2], timer[3]):
            with open(host, 'r+') as f:
                content = f.read()
                for site in website_list:
                    if site not in content:
                        f.write(redirect+" "+site+"\n")
        else:
            with open(host, 'r+') as f:
                f.seek(0)  # go to first pointer
                content = f.readlines()

                f.seek(0)  # go from EOL to first pointer
                f.truncate() # delete all file
                
                for site in website_list:
                    try:
                        content.remove(redirect+" "+site+"\n")
                    except:
                        pass
                f.writelines(content)
        time.sleep(precision)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    get_time()
    run_blocker()
else:
    print('run it as administrator')