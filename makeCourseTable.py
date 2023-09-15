#复制‘’‘中的内容到终端
'''
pip3 install bs4
pip3 install icalendar
pip3 install datetime
pip3 install selenium
python3 /Users/pc/Desktop/makeCourseTable.py
'''
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import *
from selenium.webdriver.common.by import By
import selenium.webdriver as wbd
from pathlib import Path
filePath="/Users/pc/Desktop/"#日历和课程文件存放的路径,注意结尾有/
termN = "大三上t.nosync"#文件夹名称
dtime = [["第0节"],[time(8,0,0),time(8,45,0)],[time(8,50,0),time(9,35,0)],[time(10,0,0),time(10,45,0)],[time(10,50,0),time(11,35,0)],[time(13,30,0),time(14,15,0)],[time(14,20,0),time(15,5,0)],[time(15,30,0),time(16,15,0)],[time(16,20,0),time(17,5,0)],["第9节"],[time(19,0,0),time(19,45,0)],[time(19,50,0),time(20,35,0)],["第12节"]]
weekdays = {"星期一":1,"星期二":2,"星期三":3,"星期四":4,"星期五":5,"星期六":6,"星期天":7}

filename="courseTable"
startD = datetime(2023,9,11)
url = "https://1.tongji.edu.cn/"
OPTIONS = wbd.ChromeOptions()
OPTIONS.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')
browser = wbd.Chrome(options=OPTIONS)
browser.get(url)
input("操作完毕后扣1\n")
table = browser.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/section/main/div/div[2]/div[2]/div[1]/div/div[3]/table")
table = table.get_attribute("outerHTML")
browser.close()
soup = BeautifulSoup(table,"lxml")
texts = soup.text.split("\n")
step1 = []
for i in texts:
    if i!="":
        step1.append(i.strip())
step2 = []
for i in step1:
    if i!="":
        if i[-4:]=="排课信息":
            tmp=[i[:len(i)-10],i[len(i)-10:]]
            step2+=tmp
        else:
            step2.append(i)
step3 = []
for i in step2:
    if i!="":
        step3.append(i)
step4 = []
for i in step3:
    if i[:3]=="[星期":
        step4.append(i)
    elif i[0]=="[":
        step4.append(i)

class course:
    def __init__(self,weekday,dailyTime,weeks,name,teacher,location,ord):
        self.weekday=weekday
        self.dailyTime=dailyTime
        self.weeks=weeks
        self.name=name
        self.teacher=teacher
        self.location=location
        self.ord=ord
    def p(self):
        print(self.weekday,self.dailyTime,self.weeks,self.name,self.teacher,self.location)

step5 = []
for i in range(len(step4)):
    if i%2==0:
        weekday = step4[i][1:4]
    else:
        k = 0
        while step4[i][k]!="]":k+=1
        dailyTime = list(map(int,step4[i][1:k-1].split("-")))
        k+=2
        st=k
        while step4[i][k]!="]":k+=1
        ed=k+1
        if step4[i][st:ed]=="[1, 3, 5, 7, 9, 11, 13, 15]":weeks = "单"
        elif step4[i][st:ed]=="[1-17]":weeks = "全"
        else:weeks = "双"
        tmp = step4[i][k+1:].split()
        c = course(weekday,dailyTime,weeks,tmp[0][:len(tmp[0])-8],tmp[1][:len(tmp[1])-7],tmp[2],weekdays[weekday]*100+dailyTime[0])
        step5.append(c)
step5.sort(key=lambda x:x.ord)

Path(filePath+termN).mkdir(parents=True, exist_ok=True)
for i in step5:
    Path(filePath+termN+"/"+"%d %s"%(i.ord,i.name)).mkdir(parents=True, exist_ok=True)
    for j in range(16):
        j+=1
        if i.weeks=="单" and j%2==1:
            Path(filePath+termN+"/"+"%d %s"%(i.ord,i.name)+"/lesson%d"%(j//2+1)).mkdir(parents=True, exist_ok=True)
            fp = open(filePath+termN+"/"+"%d %s"%(i.ord,i.name)+"/lesson%d"%(j//2+1)+"/note.txt","w")
            fp.close()
        elif i.weeks=="双" and j%2==0:
            Path(filePath+termN+"/"+"%d %s"%(i.ord,i.name)+"/lesson%d"%(j//2)).mkdir(parents=True, exist_ok=True)
            fp = open(filePath+termN+"/"+"%d %s"%(i.ord,i.name)+"/lesson%d"%(j//2)+"/note.txt","w")
            fp.close()
        elif i.weeks=="全":
            Path(filePath+termN+"/"+"%d %s"%(i.ord,i.name)+"/lesson%d"%(j)).mkdir(parents=True, exist_ok=True)
            fp = open(filePath+termN+"/"+"%d %s"%(i.ord,i.name)+"/lesson%d"%(j)+"/note.txt","w")
            fp.close()
        else:
            pass

cal = Calendar()
cal.add('X-WR-CALNAME', '课程表')
cal.add('X-APPLE-CALENDAR-COLOR', '#540EB9')
cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')
cal.add('VERSION', '2.0')
cnt = 0
for i in step5:
    startD = datetime(2023,9,11)
    for j in range(16):
        if i.weeks=="全":
            event = Event()
            event.add('uid', "%d"%(cnt))
            weekday = startD+timedelta(days=(weekdays[i.weekday]-1))
            event.add('dtstart', datetime.combine(weekday,dtime[i.dailyTime[0]][0]))
            event.add('dtend', datetime.combine(weekday,dtime[i.dailyTime[1]][1]))
            event.add('summary', i.name+"[%s]"%(i.teacher))
            event.add('location', i.location)
            cal.add_component(event)
            cnt+=1
            del event
        if i.weeks=="单" and j%2==0:
            event = Event()
            event.add('uid', "%d"%(cnt))
            weekday = startD+timedelta(days=(weekdays[i.weekday]-1))
            event.add('dtstart', datetime.combine(weekday,dtime[i.dailyTime[0]][0]))
            event.add('dtend', datetime.combine(weekday,dtime[i.dailyTime[1]][1]))
            event.add('summary', i.name+"[%s]"%(i.teacher))
            event.add('location', i.location)
            cal.add_component(event)
            cnt+=1
            del event
        if i.weeks=="双" and j%2==1:
            event = Event()
            event.add('uid', "%d"%(cnt))
            weekday = startD+timedelta(days=(weekdays[i.weekday]-1))
            event.add('dtstart', datetime.combine(weekday,dtime[i.dailyTime[0]][0]))
            event.add('dtend', datetime.combine(weekday,dtime[i.dailyTime[1]][1]))
            event.add('summary', i.name+"[%s]"%(i.teacher))
            event.add('location', i.location)
            cal.add_component(event)
            cnt+=1
            del event
        startD = startD + timedelta(days=7)
try:
    with open('/Users/pc/Desktop/'+filename+'.ics', 'wb') as file:
        file.write(cal.to_ical())
        print('ics日历制作完成!')
except Exception:
    raise Exception("写入文件失败, 请重试!")
