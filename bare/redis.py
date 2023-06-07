

from pathlib import Path


CWD = Path.cwd()


cache_name = 'redis'
redis_port = '6379'
sentinel_port = '7000'
master_name = 'test'
master_password = 'test'
bind = '0.0.0.0'
slave_config = 2
sentinel_config = 3

redis_path = CWD / cache_name
redis_path.mkdir(exist_ok=True , parents=True)


master_path = redis_path  / f'{cache_name}-0'
master_path.mkdir(exist_ok=True , parents=True)

with open(str(master_path / 'Dockerfile'),'w') as f:
    f.write('''
FROM redis:6.0-alpine
WORKDIR /app
COPY redis.conf /app
CMD ["redis-server" , "redis.conf"]    
    ''')
    f.close()




with open(str(master_path / 'redis.conf'),'w') as f:
    f.write(f'''
port {redis_port}
protected-mode no
masterauth {master_name}
requirepass {master_password}
    ''')
    f.close()










for i in range(slave_config):

    index = i + 1
    slave_path = redis_path  / f'{cache_name}-{index}'
    slave_path.mkdir(exist_ok=True , parents=True)
    with open(str(slave_path / 'Dockerfile'),'w') as f:
        f.write('''
FROM redis:6.0-alpine
WORKDIR /app
COPY redis.conf /app
CMD ["redis-server" , "redis.conf"]    
    ''')
        f.close()

    with open(str(slave_path / 'redis.conf'),'w') as f:

        f.write(f'''port {redis_port}
protected-mode no
masterauth {master_name}
requirepass {master_password}
slaveof {cache_name}-0 {redis_port}''')
        f.close()



for i in range(sentinel_config):

    index = i 
    sentinel_path = redis_path  / f'{cache_name}-sentinel-{index}'
    sentinel_path.mkdir(exist_ok=True , parents=True)
    with open(str(sentinel_path / 'sentinel.conf'),'w') as f:
        f.write(f'''
port {sentinel_port}
sentinel monitor mymaster {cache_name}-{index} {redis_port} 2
sentinel auth-pass mymaster {master_password}
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 60000
''')
        f.close()

    with open(str(sentinel_path / 'Dockerfile' ),'w') as f:

        f.write('''
FROM redis:6.0-alpine
WORKDIR /app
COPY sentinel.conf /app
CMD ["redis-sentinel" , "sentinel.conf"]
    ''')
    f.close()


