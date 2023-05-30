import time
import random
from influxdb import InfluxDBClient as influxdb

while True:
    data=[
            random.randint(35,40),
            random.randint(200,250),
            random.randint(250,350),
            random.randint(900,1100),
            random.randint(500,600),
            random.randint(800,1000),
            random.randint(700,900),
            random.randint(2000,2500),
            ]
    strResult = 'Current 1:'+str(data[0]).zfill(6) + ' 2:'+str(data[1]).zfill(6) +' 3:'+str(data[2]).zfill(6) + ' 4:'+str(data[3]).zfill(6) + ' 5:'+str(data[4]).zfill(6)+' 6:'+str(data[5]).zfill(6) + ' 7:'+str(data[6]).zfill(6) + ' 8:'+str(data[7]).zfill(6)
    print(strResult)


    allData=[]
    index = 0
    while True:
        index = strResult.find(':',index+1)   
        if index == -1:
            break
        thisData =int(strResult[index+1:index+7])
        allData.append(thisData)


    data=[{'measurement' : 'CH1',
            'tags':{'inhatc' : '2022',},
            'fields':{'CH1':allData[0],},},
        {'measurement' : 'CH2',
            'tags':{'inhatc' : '2022',},
            'fields':{'CH2':allData[1],},},
        {'measurement' :'CH3',
            'tags':{'inhatc' : '2022',},
            'fields':{'CH3':allData[2],},},
        {'measurement' :'CH4',
            'tags':{'inhatc' :'2022',},
            'fields':{'CH4':allData[3],},},
        {'measurement' :'CH5',
            'tags':{'inhatc' :'2022',},
            'fields':{'CH5':allData[4],},},
        {'measurement' :'CH6',
            'tags':{'inhatc' : '2022',},
            'fields':{'CH6':allData[5],},},
        {'measurement' : 'CH7',
            'tags':{'inhatc':'2022',},
            'fields':{'CH7':allData[6],},},
        {'measurement':'CH8',
            'tags':{'inhatc':'2022',},
            'fields':{'CH8':allData[7],},},]
    client = None
    try :
        client=influxdb('localhost',8086,'admin','admin','FormatTest')
    except Exception as e:
        print("Exception " + str(e))

    if client is not None:
        try:
            client.write_points(data)
        except Exception as e:
            print("Exception " + str(e))
        finally:
            client.close()

    time.sleep(1)
