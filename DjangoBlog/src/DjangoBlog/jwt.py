"""

curl -X POST -d "username=ranjeetsingh&password=ranjeetsingh" http://127.0.0.1:8000/api/auth/token/

curl -X POST -d "username=hello&password=world" http://127.0.0.1:8000/api/auth/token/


eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InJhbmplZXRzaW5naCIsImV4cCI6MTU1NTI0NDcyMywiZW1haWwiOiJyYW5qZWU5NzBAZ21pbC5jb20ifQ.ZMVIlQYeWnxUjWXGAvAtfLPsyRFWQS0a05DNIct3z9E

curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMywidXNlcm5hbWUiOiJoZWxsbyIsImV4cCI6MTU1NTI0NTc2MSwiZW1haWwiOiIxMTIzQGdtYWlsLmNvbSJ9.kn6o2W8oMTa8231n1fjafEaUZFeWNhSsQy61KbL_co0" http://127.0.0.1:8000/api/comments/

curl http://127.0.0.1:8000/api/comments/

curl -X POST -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMywidXNlcm5hbWUiOiJoZWxsbyIsImV4cCI6MTU1NTI0NTc2MSwiZW1haWwiOiIxMTIzQGdtYWlsLmNvbSJ9.kn6o2W8oMTa8231n1fjafEaUZFeWNhSsQy61KbL_co0" -H "Content-Type: application/json" -d '{"content":"reply to hello jwt comment"}' 'http://127.0.0.1:8000/api/comments/create/?slug=skvjgs&type=post&parent_id=62'


curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api-token-auth/

"""