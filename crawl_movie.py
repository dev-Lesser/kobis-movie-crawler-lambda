import requests, datetime
import json
import pymongo
from dotenv import load_dotenv
import os
from lxml import html
import urllib.request
import boto3

if __name__ == '__main__':
    
    load_dotenv(verbose=True)
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    KOBIS_URL =  os.getenv('KOBIS_URL')
    SECRET_KEY =os.getenv('SECRET_KEY')

    AWS_ACCESS_KEY = os.getenv('AWS_ACCESSKEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRETKEY')
    BUCKET_NAME = os.getenv('BUCKET_NAME')


    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name='ap-northeast-2',
    )
    client = pymongo.MongoClient("mongodb+srv://{user}:{pw}@{host}".format(user=DB_USER, pw=DB_PASSWORD, host=DB_HOST))
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]


    now = datetime.datetime.now()
    target_date = (now - datetime.timedelta(days=1)).strftime('%Y%m%d')

    res = requests.get(KOBIS_URL, params={"key":SECRET_KEY, "targetDt":target_date})
    date = json.loads(res.content)['boxOfficeResult']['showRange'].split('~')[0]
    date = datetime.datetime.strptime(date, "%Y%m%d")
    movie_list = json.loads(res.content)['boxOfficeResult']['dailyBoxOfficeList']
    for imovie in movie_list:
        code = imovie['movieCd']
        files = {"code" : code }
        url = os.getenv('KOBIS_IMG_URL')
        res = requests.post(url, data=files)
        root = html.fromstring(res.text)
        image_url = 'https://www.kobis.or.kr/' + root.xpath('//a[@class="fl thumb"]/@href')[0]

        urllib.request.urlretrieve(image_url, '/tmp/'+ code +'.jpg') # code 이름으로 파일 저장
        s3.upload_file(
            '/tmp/' + code +'.jpg',
            BUCKET_NAME, 
            code +'.jpg'
        )
        print('Uploaded %s' % code)

    result = {
        'datetime': date,
        'dailyList': movie_list
    }
    compare = collection.find_one({'datetime': date})
    if not compare:
        collection.insert_one(result)
        print('Insert success date %s' %date)
    else:
        print('Already exist %s' %date)