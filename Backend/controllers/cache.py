import redis
from functools import wraps
from flask import jsonify, make_response
import json

# Redis client for caching with short timeout to avoid blocking
# If Redis is not available, the app will work without caching
try:
    redis_client = redis.Redis(
        host='localhost', 
        port=6379, 
        db=1, 
        decode_responses=True,
        socket_connect_timeout=1,  # 1 second connection timeout
        socket_timeout=1           # 1 second operation timeout
    )
    # Test connection
    redis_client.ping()
    REDIS_AVAILABLE = True
except:
    redis_client = None
    REDIS_AVAILABLE = False

# Cache timeout constants (in seconds)
CACHE_TIMEOUT_SHORT = 60        # 1 minute - for frequently changing data
CACHE_TIMEOUT_MEDIUM = 300      # 5 minutes - for moderately changing data
CACHE_TIMEOUT_LONG = 3600       # 1 hour - for rarely changing data
CACHE_TIMEOUT_STATS = 120       # 2 minutes - for dashboard stats

def cache_response(timeout=300, key_prefix=None):
    """
    Decorator to cache API responses in Redis.
    
    Args:
        timeout: Cache expiry time in seconds (default: 300)
        key_prefix: Optional custom prefix for cache key
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip caching if Redis is not available
            if not REDIS_AVAILABLE or redis_client is None:
                return f(*args, **kwargs)
            
            # Build cache key
            prefix = key_prefix or f.__name__
            cache_key = f"cache:{prefix}:{str(args)}:{str(kwargs)}"
            
            try:
                # Try to get cached response
                cached = redis_client.get(cache_key)
                
                if cached:
                    cached_data = json.loads(cached)
                    return make_response(jsonify(cached_data), 200)
                
                # Execute the function
                result = f(*args, **kwargs)
                
                # Cache successful responses
                if isinstance(result, tuple) and len(result) == 2:
                    response, status_code = result
                    if hasattr(response, 'get_json'):
                        data = response.get_json()
                    else:
                        data = response
                    
                    if status_code == 200:
                        redis_client.setex(cache_key, timeout, json.dumps(data))
                    return make_response(jsonify(data), status_code)
                
                return result
                
            except (redis.ConnectionError, redis.TimeoutError):
                # Redis unavailable, execute without caching
                return f(*args, **kwargs)
                
        return decorated_function
    return decorator

def cache_with_user(timeout=300, key_prefix=None):
    """
    Decorator to cache API responses per user.
    Uses JWT identity to create user-specific cache keys.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_jwt_extended import get_jwt_identity
            
            # Skip caching if Redis is not available
            if not REDIS_AVAILABLE:
                return f(*args, **kwargs)
            
            try:
                user_id = get_jwt_identity()
                prefix = key_prefix or f.__name__
                cache_key = f"cache:{prefix}:user_{user_id}"
                
                cached = redis_client.get(cache_key)
                
                if cached:
                    cached_data = json.loads(cached)
                    return make_response(jsonify(cached_data), 200)
                
                result = f(*args, **kwargs)
                
                if isinstance(result, tuple) and len(result) == 2:
                    response, status_code = result
                    if hasattr(response, 'get_json'):
                        data = response.get_json()
                    else:
                        data = response
                    
                    if status_code == 200:
                        redis_client.setex(cache_key, timeout, json.dumps(data))
                    return make_response(jsonify(data), status_code)
                
                return result
                
            except (redis.ConnectionError, redis.TimeoutError):
                return f(*args, **kwargs)
                
        return decorated_function
    return decorator

def invalidate_cache(pattern):
    """
    Invalidate all cache keys matching a pattern.
    
    Args:
        pattern: Redis key pattern (e.g., "cache:departments:*")
    """
    if not REDIS_AVAILABLE:
        return 0
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            return len(keys)
        return 0
    except (redis.ConnectionError, redis.TimeoutError):
        return 0

def invalidate_user_cache(user_id, key_prefix=None):
    """
    Invalidate cache for a specific user.
    
    Args:
        user_id: The user ID
        key_prefix: Optional specific cache prefix to invalidate
    """
    if key_prefix:
        pattern = f"cache:{key_prefix}:user_{user_id}"
    else:
        pattern = f"cache:*:user_{user_id}"
    return invalidate_cache(pattern)

def invalidate_all_cache():
    """Invalidate all cached data."""
    return invalidate_cache("cache:*")

def get_cache_stats():
    """Get cache statistics for monitoring."""
    if not REDIS_AVAILABLE:
        return {"error": "Redis not available", "status": "disabled"}
    try:
        info = redis_client.info()
        keys = redis_client.keys("cache:*")
        return {
            "total_cached_keys": len(keys),
            "used_memory": info.get("used_memory_human", "N/A"),
            "connected_clients": info.get("connected_clients", 0),
            "uptime_seconds": info.get("uptime_in_seconds", 0),
            "status": "connected"
        }
    except (redis.ConnectionError, redis.TimeoutError):
        return {"error": "Redis not available", "status": "disconnected"}
