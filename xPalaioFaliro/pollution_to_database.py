__author__ = 'julian'

import csv
import MySQLdb

db = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='jocstem_environment',charset='utf8', use_unicode=False)

cursor = db.cursor()

file = open('pollution.csv','rU')

csv_data = csv.reader(file)

header = csv_data.next()


for row in csv_data:
    tag = row[0]
    district = row[1]
    school = row[2]
    num_schools = int(row[3])
    NO2 = float(row[4])
    level = row[5]
    quality = row[6]

    print district
    cursor.execute("INSERT INTO game_pollution(tag, district, NO2, level,school,num_schools, quality) VALUES(%s, %s, %s, %s, %s, %s, %s)",[tag, district, NO2, level, school, num_schools, quality])

db.commit()
cursor.close()
print "--------------------------"
print "Pollution to Database Done"