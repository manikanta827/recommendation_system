# -*- coding: utf-8 -*-
"""
Created on Sat May  1 14:14:20 2021

@author: manik
"""

import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                         database='shout_final',
                                         user='root',
                                         password='root',
                                         auth_plugin='mysql_native_password')
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

import pandas as pd

db_cursor = connection.cursor()
db_cursor.execute('select a.*,b.mrp, b.sp, b.status as item_status from (select a.*,b.rating  from (select a.id as redemptionid, a.userid, a.date as redemptiondate, a.offerId, a.offerStatus,a.json as issued_redeemed,   b.merchantId,b.itemId,b.discount,b.startDate,b.endDate,b.status as offer_status from offerredemption a left join offers b on a.offerId = b.id ) a left join ratings b on (a.userId=b.userId and a.merchantId=b.merchantId) ) a left join items b on a.itemId =b.id')

table_rows = db_cursor.fetchall()

df = pd.DataFrame(table_rows)
print(df)

df.to_pickle("full_data.pkl")

db_cursor.execute('select * from offers')

table_rows = db_cursor.fetchall()

df_offers = pd.DataFrame(table_rows)
df_offers.to_pickle("offers_data.pkl")
