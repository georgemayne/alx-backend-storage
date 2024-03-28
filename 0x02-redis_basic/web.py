#!/usr/bin/env python3
""" In this tasks, we will implement a get_page function (prototype:
def get_page(url: str) -> str:). The core of the function is very simple.
It uses the requests module to obtain the HTML content of a particular URL and
returns it.
"""


import redis
import requests

r = redis.Redis()

def get_page(url: str) -> str:
    """Obtain HTML content of a particular URL"""
    key_count = f"count:{url}"
    key_cached = f"cached:{url}"

    # Check if URL is cached
    cached_value = r.get(key_cached)
    if cached_value:
        # Increment access count
        r.incr(key_count)
        # Return cached content
        return cached_value.decode("utf-8")
    
    # URL not cached, fetch content
    response = requests.get(url)
    html_content = response.text

    # Cache content with expiration time of 10 seconds
    r.set(key_cached, html_content, ex=10)
    # Increment access count
    r.incr(key_count)

    return html_content

if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))
