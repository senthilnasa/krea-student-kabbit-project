
import base64

token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjkzYjQ5NTE2MmFmMGM4N2NjN2E1MTY4NjI5NDA5NzA0MGRhZjNiNDMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5NDMzNDkwOTAxMTAtZjZxbWhtM2ZpaWRkdDJwNG4xbTRrbnE4bm1idjNjMmMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5NDMzNDkwOTAxMTAtZjZxbWhtM2ZpaWRkdDJwNG4xbTRrbnE4bm1idjNjMmMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDIwMzg5OTU2Mzg2NjQ0MzA4NzUiLCJoZCI6ImtyZWEuYWMuaW4iLCJlbWFpbCI6InZhdHNhbHlhX2JldGFsYS5zaWFzMjJAa3JlYS5hYy5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYmYiOjE3MTMxMDg5MTcsIm5hbWUiOiJWYXRzYWx5YSBCZXRhbGEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSnlMZm9yOHZtY3RQa3RTaTIwcGpjeEVSeXN1ODE0Y3NNRDdqZmNMb3Q0Uk9UbGdncz1zOTYtYyIsImdpdmVuX25hbWUiOiJWYXRzYWx5YSIsImZhbWlseV9uYW1lIjoiQmV0YWxhIiwiaWF0IjoxNzEzMTA5MjE3LCJleHAiOjE3MTMxMTI4MTcsImp0aSI6IjBiMDEyZjBiNjU5YWI0NTBiOTY5MmYyMzNlZjlkMzg4ZWVjYTEyZGYifQ.bS_Qs2Ke8PsdjtLiEtXZSSN0-cTybbRsBlf78R9Uix2jvW8SSJk8ROiRHJnLkQmD2XT2ActmQAzjYmBQn-CaiTJ_qW9f8dP3lUGnWqEla7GIpEZ8t855bw7n-Rpo0kusyW0BJO7hbgdGAZCFGCLX1cytqQqm95Q3XKZGpd-rsYpnkwQEdWqYXF1ykorzS2N0yqeStAWUBGr2porpoTG1x3Ql1HpGv7Toah2cV4kF_yLy-p4a3AGYK04ECt-kma8rrymr6bI0Jq6qAxQ1aOrNf8BVseefseBH3BJf2faFYSc-uAN1czH9j0ojjiQ3uqws6k3T0tPdDFi5D7O5d9XjQw"

dtoken = base64.b64decode(token.split('.')[1] + '==').decode('utf-8')
name = dtoken.split('"name":')[1].split(',')[0].replace('"','')

print(name)