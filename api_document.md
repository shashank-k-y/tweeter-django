# API Document:

## 1. Registration API

method: POST
URL: http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/profiles/register/

Request Parameters

| parameters     | type       |
| -------------- | -----------|
| username       | str        |
| password       | str        |
| password_2     | str        |
| email          | str        |

Response:

status code: 200

```json
{
    "message": "tanjiro1 Successfully registerd !",
    "token": "4e68307ab59399f96f659203659d8b88ce42557a",
    "username": "tanjiro1",
    "email": "tanjiro@demonslayer1.com"
}
```

status code: 400

```json
{
    "username": [
        "This field is required."
    ],
    "email": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ],
    "password_2": [
        "This field is required."
    ]
}
```

## 2. Login Api

method: POST
URL: http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/profiles/login/

Request Parameters

| parameters     | type       |
| -------------- | -----------|
| username       | str        |
| password       | str        |

Response:

status code 200:

```json
{
"token": "107ac919be1e2c0152c667b9db98ecfc5d200a13"
}
```

ststus code 400:

```json
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```


## 3. Logout Api

method: POST
URL: http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/profiles/logout/

header:
Authorization: Token 'access token'

response:

```json
"mohan logged out Successfully !"
```

## 4. Get all Profiles:

header:
Authorization: Token 'access token'

method: GET
URL: http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/profiles/

response:

```json
[
    {
        "id": 1,
        "username": "shashank",
        "email": "django@gmail.com",
        "bio": "Bio",
        "followers": [],
        "following": []
    },
    {
        "id": 2,
        "username": "mohan",
        "email": "mohan@gmail.com",
        "bio": "Bio",
        "followers": [],
        "following": []
    }
]
```

## 5. Get profiles by id:

header:
Authorization: Token 'access token'

method: GET
URL: ```http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/profiles/<id>```

success response:

```json

{
    "id": 1,
    "username": "shashank",
    "email": "django@gmail.com",
    "bio": "Bio",
    "followers": [],
    "following": []
}
```
  
failed response 404:
  
```json
  "Profile doesnot exist."
```
  
## 6. Follow/unfollow api:

header:
Authorization: Token 'access token'

method: POST
URL: ```http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/profiles/<id>/<action>```
  
Request Parameters

| parameters     | description       |
| -------------- | ------------------|
| id             | primary key of the profile that needs to be followed/unfollowed|
| action         | follow/unfollow   |
  
Success Response 200:
  
```json
  "successfully following mohan."
```
  
```json
  "successfully unfollowed mohan."
```
  
  
## 7. Post Tweet API
  
method: POST
URL: ```http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/tweets/```
  
Authorization: Token 'access token'
  
FORM DATA:
| parameters     | description       |
| -------------- | ------------------|
| text           | tweet's text content|
| file           | file to upload   |

  
Success Response:

```json
  {
    "id": 5,
    "tweeter": 2,
    "file": "https://tweetmedia.s3.amazonaws.com/django11_HuJN8ch.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T131449Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4b960d0a59c08a9c09fbbcea0952db1b904d45032d41eea691ad62c0a23d013d",
    "text": "tweet 4",
    "presigned_url": "https://tweetmedia.s3.amazonaws.com/django11.jpg?response-content-type=image%2Fjpeg&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T131449Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=554953950db197be9b4359a13d642730028251bcb4a301b6a37a8889d8414422"
}

```
NOTE: Presigned url will expire after 3600 seconds
  
failed response 400
 
```json
 {
    "text": [
        "This field is required."
    ]
}
```

## 8. Get all tweets posted by user.
  method: GET
  URL: ```http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/tweets/```
  
  
Authorization: Token 'access token'
  
success response:

```json
  [
    {
        "id": 5,
        "tweeter": 2,
        "file": "https://tweetmedia.s3.amazonaws.com/django11_HuJN8ch.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4ba713f97d04c826bd9a1082e5bd1eeca7ddb14a9234a670487ead763c76fff0",
        "text": "tweet 4",
        "presigned_url": "https://tweetmedia.s3.amazonaws.com/django11.jpg?response-content-type=image%2Fjpeg&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=772bed7264d1c79d8fd0e58e425565a6ded9890761fc49148feadf5d2420caf2"
    },
    {
        "id": 4,
        "tweeter": 2,
        "file": null,
        "text": "tweet 3",
        "presigned_url": null
    },
    {
        "id": 3,
        "tweeter": 2,
        "file": "https://tweetmedia.s3.amazonaws.com/du.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=27457a19979c571de81fb7ed2258b1e55f598f633ee93c51e166d001508604ea",
        "text": "tweet 2",
        "presigned_url": "https://tweetmedia.s3.amazonaws.com/du.jpg?response-content-type=image%2Fjpeg&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=03211141052ded26fe61c6287491cf474339a678557ab0447716635aeb69c82a"
    },
    {
        "id": 2,
        "tweeter": 2,
        "file": "https://tweetmedia.s3.amazonaws.com/django-unchained-_p3k6z8V.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a272cc4307660b1bfaa7f47dba37af6dd2d04981d9e4944b1e93a1c32cbeab00",
        "text": "tweet 2",
        "presigned_url": null
    },
    {
        "id": 1,
        "tweeter": 2,
        "file": "https://tweetmedia.s3.amazonaws.com/django-unchained-poster3.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132116Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d85e07f142d9e3ce1236d85f632ef2c96c7a21a767652391d8420c7260391684",
        "text": "shashanks tweet",
        "presigned_url": null
    }
]
```
  
failed Response:
  
```json
  "You have not posted any tweets."
```
  
## 9. Fetch tweet by id
  
  method: GET
  URL: ```http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/tweets/<id>```
  
Authorization: Token 'access token'
  
  
success response:
  
```json
  {
    "id": 3,
    "tweeter": 2,
    "file": "https://tweetmedia.s3.amazonaws.com/du.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132304Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e5a6e36b9722a0ff30965963173500ca645c37d72c38c27f32bc88f73155ad42",
    "text": "tweet 2",
    "presigned_url": "https://tweetmedia.s3.amazonaws.com/du.jpg?response-content-type=image%2Fjpeg&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GVBHIFXHX27AQJZ%2F20221022%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20221022T132304Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=9a4f6a92af4f24ce654656a4739bd5a89a3df7ac7a7bd3d1287efed18a159bfb"
}
```
  
failed response 404:
```json
  "tweet does not exist."
```
403:
```json
  "you are not permitted to access this tweet"
```
  
## Feed Api:
  
Authorization: Token 'access token'
  
method: GET
URL: ```http://ec2-3-111-186-37.ap-south-1.compute.amazonaws.com:8000/tweets/feed```
  
 

