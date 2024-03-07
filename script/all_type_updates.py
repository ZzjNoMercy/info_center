import pymysql
import pandas as pd
import time
from datetime import datetime


def info_to_database(fstr):
    db = pymysql.connect(host='localhost',
                         user='root',
                         port=3306,
                         password='P@ssw0rd',
                         database='info_center')
    cursor = db.cursor()
    try:
        cursor.execute(fstr)
        db.commit()
    except Exception as e:
        if "1062" in e.args:
            print("重复")
        else:
            print(e)
            print(fstr, "失败")
            db.rollback()
    db.close()


def str_to_stamp(timestr: str):
    """
    时间字符串转时间戳，支持多种时间格式的输入，如：2022-05-10，2022/05/10，2022-05-10 12:10:00等方式输入
    :param timestr:
    :param timeStr: 时间字符串
    :return: 时间戳
    """
    pandas_time = pd.to_datetime(timestr)  # pandas 将字符串转为日期类型，可以接受多种格式的输入，用于标准化
    # 方法1：用time
    # timeType = time.strptime(str(pandasTime), "%Y-%m-%d %H:%M:%S")
    # timeStamp = time.mktime(timeType)
    # return int(timeStamp)
    # 方法2：用datetime
    # datetime
    time_type = datetime.strptime(str(pandas_time), "%Y-%m-%d %H:%M:%S")
    # 时间戳
    time_stamp = time_type.timestamp()
    return int(time_stamp)


if __name__ == '__main__':
    datas = pd.read_excel(r'D:\Nas同步\Pet\工作\信息科\爬虫项目\太平洋车型\all_type_updates.xlsx')
    sql_str = '''
       INSERT INTO `index_gtminfo` (`car_id`, `car_name`, `pic_url`, `price`, `type`,`update_time`, `sell_status`, `car_url` )
       VALUES (%d, %s, %s, %s, %s, %s, %s, %s)
       '''
    for index, row in datas.iterrows():
        try:
            car_id = int(row['ID'])
        except ValueError:
            car_id = 0
        try:
            car_name = "'" + row['车型'] + "'"
        except TypeError:
            car_name = "''"
        try:
            pic_url = "'" + row['图片'] + "'"
        except TypeError:
            pic_url = "''"
        try:
            price = "'" + row['指导价'] + "'"
        except TypeError:
            price = "''"
        try:
            update_type = "'" + row['更新类型'] + "'"
        except TypeError:
            update_type = "''"
        try:
            update_time = "'" + str(row['更新时间']) + "'"
        except TypeError as e:
            print(e)
            update_time = "''"
        try:
            sell_status = "'" + row['销售状态'] + "'"
        except TypeError:
            sell_status = "''"
        try:
            car_url = "'" + row['车型链接'] + "'"
        except TypeError:
            car_url = "''"
        formatted_str = sql_str % (
            car_id, car_name, pic_url, price, update_type,
            update_time, sell_status, car_url)
        info_to_database(formatted_str)
