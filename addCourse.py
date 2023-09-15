from icalendar import Calendar, Event
from datetime import *
from pathlib import Path
filePath="/Users/pc/Desktop/"#日历和课程文件存放的路径,注意结尾有/
termN = "大三上t.nosync"#文件夹名称
dtime = [["第0节"],[time(8,0,0),time(8,45,0)],[time(8,50,0),time(9,35,0)],[time(10,0,0),time(10,45,0)],[time(10,50,0),time(11,35,0)],[time(13,30,0),time(14,15,0)],[time(14,20,0),time(15,5,0)],[time(15,30,0),time(16,15,0)],[time(16,20,0),time(17,5,0)],["第9节"],[time(19,0,0),time(19,45,0)],[time(19,50,0),time(20,35,0)],["第12节"]]
weekdays = {"星期一":1,"星期二":2,"星期三":3,"星期四":4,"星期五":5,"星期六":6,"星期天":7}
class course:
    def __init__(self,weekday,dailyTime,weeks,name,teacher,location):
        self.weekday=weekday
        self.dailyTime=dailyTime
        self.weeks=weeks
        self.name=name
        self.teacher=teacher
        self.location=location
        self.ord=weekdays[weekday]*100+dailyTime[0]

i=course("星期一",[10,11],"全","数据结构","尤鸣宇","北221")

Path(filePath+termN).mkdir(parents=True, exist_ok=True)
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
startD = datetime(2023,9,11)
for j in range(16):
    if i.weeks=="全":
        event = Event()
        event.add('uid', "%d%d"%(cnt,sum([ord(cha) for cha in i.name])))
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
        event.add('uid', "%d%d"%(cnt,sum([ord(cha) for cha in i.name])))
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
        event.add('uid', "%d%d"%(cnt,sum([ord(cha) for cha in i.name])))
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
    with open('/Users/pc/Desktop/'+"addCourse%s"%(i.name)+'.ics', 'wb') as file:
        file.write(cal.to_ical())
        print('ics日历制作完成!')
except Exception:
    raise Exception("写入文件失败, 请重试!")