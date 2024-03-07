import pymysql
import pandas as pd


def car_to_database(fstr):
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
    datas = pd.read_csv(r'C:\Users\Pet\Desktop\cars.csv', encoding="utf-8")
    sql_str = '''
       INSERT INTO `index_cars` (`length`, `Width`, `Height`, `car_type`, `brands_id`, `car`, `car_class`, 
       `car_body_form`, `company_id`, `price_interval`) VALUES (%d, %d, %d, %s, %s, %s, %s, %s, %s, %s)
       '''
    for index, row in datas.iterrows():
        try:
            length = int(row['长'])
        except ValueError:
            length = 0
        try:
            width = int(row['宽'])
        except ValueError:
            width = 0
        try:
            height = int(row['高'])
        except ValueError:
            height = 0
        try:
            car_type = "'" + row['车辆类型-SGMW'] + "'"
        except TypeError:
            car_type = "''"
        try:
            brands_id = "'" + row['品牌'] + "'"
        except TypeError:
            brands_id = "'-'"
        try:
            car = "'" + row['车型'] + "'"
        except TypeError:
            car = "''"
        try:
            car_class = "'" + row['车型级别-SGMW'] + "'"
        except TypeError:
            car_class = "''"
        try:
            car_body_form = "'" + row['车身形式-SGMW'] + "'"
        except TypeError:
            car_body_form = "''"
        company_id = "'" + row['企业简称SGMW'] + "'"
        try:
            price_interval = "'" + row['价格段'] + "'"
        except TypeError:
            price_interval = "''"
        formatted_str = sql_str % (
            length, width, height, car_type,
            brands_id, car, car_class,
            car_body_form, company_id, price_interval)
        car_to_database(formatted_str)
