import re
import sqlite3

from gevent import os


class Period:
    def __init__(self):
        self.Path="Period.sqlite3"

    def sql_add(self,sql,para):
        conn = sqlite3.connect(self.Path)
        cursor = conn.cursor()
        cursor.execute(sql,para)
        conn.commit()
        cursor.close()
        conn.close()


    def sql_check(self,sql):
        conn = sqlite3.connect(self.Path)
        cursor = conn.cursor()
        result = cursor.execute(sql)
        re = result.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return re




    def data_add_s(self):
        print("大姨妈又来了啊，快点告诉我她什么时候来的（20180808  2018-08-08  2018.08.08  2018/08/08）：",end="")
        start = str(self.getDate())
        sql = "insert into Period(startDate) values (\""+start+"\")"
        para = (start)
        self.sql_check(sql)

    def data_add_se(self):
        print("大姨妈终于走了呀，快点告诉我她来的时候是什么时候（20180808  2018-08-08  2018.08.08  2018/08/08）：",end="")
        start=self.getDate()
        print("大姨妈是什么时候离开的呀（20180808  2018-08-08  2018.08.08  2018/08/08）：",end="")
        end=self.getDate()

        interval = end - start  # 获取大姨妈的历时
        interval = int(interval.days)+1  # 获取历时的天数

        if interval<2:
            print("大姨妈就来住了一天啊，是不是你弄错了呀")
            return 0

        if interval>20:
            print("大姨妈喜欢你呀，来了{}天，你是不是弄错了呀".format(interval))
            return 0


        start=str(start)
        end=str(end)

        sql = "select * from Period where startDate=\"" + start + "\""
        checkDateLists = self.sql_check(sql)
        if checkDateLists.__len__() > 0:
            sql = "update Period  set endDate=(?),takeDate=(?) where startDate=(?)"
            para = (end, interval, start)
            self.sql_add(sql, para)
        else:
            sql = " insert into Period values(?,?,?)"
            para = (start, end, interval)
            self.sql_add(sql, para)


    def data_show(self):
        sql="select * from Period"
        lists=self.sql_check(sql)

        if lists.__len__()>0:
            count=0
            for list in lists:
                if str(list[2])=="None":
                    print("大姨妈正在探望你，这是她第{}次来了，她是{}来的，还没有离开，你要好好休息".format(count,list[0]))
                    continue
                count+=1
                print("大姨妈第{}次来探望你的时候，是从{}来的，{}就离开了，一共呆了{}天.".format(count,list[0],list[1],list[2]))
        else:
            print("大姨妈还没有来过哟，你好幸运呀.......")

    def getDate(self):
        while True:
            try:
                readin=input()
                try:
                    if readin.__len__() == 8:#全数字输入
                        date = []
                        date.append(readin[0:4])
                        date.append(readin[4:6])
                        date.append(readin[6:8])
                    elif readin.__len__() == 10:#有分隔符输入
                        separator = readin[4]
                        date = []
                        for i in readin.split(separator):
                            date.append(i)
                    else:
                        continue
                    import datetime
                    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))#转换成日期格式
                    return date.date()
                except:
                    pass
            except:
                pass

if __name__ == '__main__':
    a=Period()
    # a.data_show()
    while True:
        try:
            print("1.大姨妈来探望你了，2.大姨妈探望回去了，3.看看大姨妈都来了几次,4.我不要你了，再见")
            while True:
                try:
                    sgin=input()
                    if sgin=="1":
                        a.data_add_s()
                        break
                    elif sgin=="2":
                        a.data_add_se()
                        break
                    elif sgin=="3":
                        a.data_show()
                        break
                    elif sgin=="4":
                        exit()
                    elif sgin=="create":
                        conn = sqlite3.connect("Period.sqlite3")
                        cursor = conn.cursor()
                        sql = "create table Period (startDate text PRIMARY KEY,endDate text,takeDate Integer)"
                        cursor.execute(sql)
                        cursor.close()
                        break
                except:
                    pass
            print("\n\n-------------------------------------------------------------------------------------------------------------")
        except:
            pass



    # conn = sqlite3.connect("Period.sqlite3")
    # cursor = conn.cursor()
    # sql = "create table Period (startDate text PRIMARY KEY,endDate text,takeDate Integer)"
    # cursor.execute(sql)
    # cursor.close()