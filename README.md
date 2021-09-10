## movie crawl 및 이미지 s3에 적재


### aws lambda python library 계층 주의점
폴더구조
```
[].zip
python <- 반드시 포함
    | -- library 들의 폴더
```

- 특정 라이브러리는 amazon-linux 에서 맞는 python 버전과 그 환경에서 pip install 을 한 라이브러리들이 필요
- 이번 경우 lxml 의 경우가 그러함

### .env
```
DB_HOST=[]
DB_USER=[]
DB_PASSWORD=[]
DB_NAME=[]
COLLECTION_NAME=[]

KOBIS_URL=[]
SECRET_KEY=[]

AWS_ACCESSKEY=[] --> lambda 내의 AWS_ACCESS_KEY 라는 환경변수가 default 로 존재하여 사용하지 못함 (언더바 제거)
AWS_SECRETKEY=[] --> lambda 내의 AWS_SECRET_KEY 라는 환경변수가 default 로 존재하여 사용하지 못함 (언더바 제거)
BUCKET_NAME=[]

KOBIS_IMG_URL=[]
```