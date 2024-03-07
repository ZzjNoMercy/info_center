import pandas as pd
import pymysql


def info_to_database(fstr):
    datas = pd.read_excel(r'D:\Nas同步\Pet\工作\信息科\爬虫项目\太平洋车型\all_models.xlsx')
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


if __name__ == '__main__':
    datas = pd.read_excel(r'D:\Nas同步\Pet\工作\信息科\爬虫项目\太平洋车型\all_models.xlsx')
    notnull_datas = datas[datas['制造商'].notnull()]
    sql_str = """INSERT INTO index_pcautocars (`car_id`, `car_name`, `price`, `type`, `update_time`, `sell_status`, 
                `car_url`, `car_class`, `company`, `brand`, `pic_url`) VALUES (%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                ON DUPLICATE KEY 
                UPDATE `update_time`=values(`update_time`)"""
    for index, row in notnull_datas.iterrows():
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
        try:
            car_class = "'" + row['车型级别'] + "'"
        except TypeError:
            car_class = "''"
        try:
            company = "'" + row['制造商'] + "'"
        except TypeError:
            company = "''"
        try:
            brand = "'" + row['品牌'] + "'"
        except TypeError:
            brand = "''"
        formatted_str = sql_str % (
            car_id, car_name, price, update_type,
            update_time, sell_status, car_url, car_class, company, brand, pic_url)
        info_to_database(formatted_str)
