from flask_cors import CORS
from flask import Flask, jsonify
from redis.sentinel import Sentinel
import logging
import redis
from flask_cors import CORS

def test_redis_connection():
    try:
        r = redis.Redis(
    host='redis-sentinel-0',
    port=7000, 
    password='test')

        if r.ping():
            print('Connected to Redis successfully!')
        else:
            print('Failed to connect to Redis.')
    except redis.ConnectionError as ex:
        print('Connection error:', ex)

test_redis_connection()

cache_master_name = 'mymaster'
cache_password = 'test'
cache_sentinel_string = "redis-sentinel-0:7000,redis-sentinel-1:7000,redis-sentinel-2:7000"
cache_sentinels = [(item.split(':')[0], int(item.split(':')[1])) for item in cache_sentinel_string.split(',')]
cache_sentinel_object = Sentinel(cache_sentinels, socket_timeout=0.1)
cache_master = cache_sentinel_object.master_for(cache_master_name,password = cache_password, socket_timeout=0.1)

app = Flask(__name__)
CORS(app)

@app.route('/ui/api/hits')
def hello():
    cache_master.incr('hits')
    hits = cache_master.get('hits')
    app.logger.info('Page hit: %s', hits.decode())
    return jsonify({"message" : hits.decode()}),200


@app.route('/ui/api/health')
def health():
    return jsonify({}),200

handler = logging.FileHandler('flask.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)