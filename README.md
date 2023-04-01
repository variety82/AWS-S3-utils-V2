# AWS-S3-utils(V2)

### Git Clone

```
git clone https://github.com/variety82/AWS-S3-utils-V2-.git
```

### Prerequisite

```
$ pip install -r requirements.txt
```

### 주의사항

.env에서 환경변수 설정을 해야합니다

```
aws_access_key_id
aws_secret_access_key
에 해당하는 내용들을 설정
```

[참고](https://variety82p.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98-%EC%84%A4%EC%A0%95%EC%9C%BC%EB%A1%9C-%EB%B3%B4%EC%95%88%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0)



#### 사용예시

```
s3 = s3_connection()

make_objects_list(s3, 'bucketName')
=> ['빨간달팽이', '파란달팽이']

obj = make_object('bucketName', '빨간달팽이')
obj => s3.Object(bucket_name='smartfarmtv', key='빨간달팽이.png')

url = get_object_url(s3, obj)
```