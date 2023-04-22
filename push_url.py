import redis

user = ["34087486", "15994269"]
keyword = ["原神"]

r = redis.StrictRedis(host='localhost', port=6379, db=0)

for i in user:
    r.lpush('pixiv:start_urls', i)

# for i in keyword:
#     r.lpush('pixiv_server:start_urls', i)
