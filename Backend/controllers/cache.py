import redis
from functools import wraps
from flask import jsonify
import json

redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

def cache_response(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{str(args)}:{str(kwargs)}"
            cached = redis_client.get(cache_key)
            
            if cached:
                return jsonify(json.loads(cached)), 200
            
            result = f(*args, **kwargs)
            
            if isinstance(result, tuple) and len(result) == 2:
                data, status_code = result
                if status_code == 200:
                    redis_client.setex(cache_key, timeout, json.dumps(data))
                return jsonify(data), status_code
            
            return result
        return decorated_function
    return decorator

def invalidate_cache(pattern):
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
