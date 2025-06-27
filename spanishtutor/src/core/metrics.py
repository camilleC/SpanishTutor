# spanishtutor/src/metrics.py
from prometheus_client import Counter

# These variables live in memory and can be used from any part of the app by importing them. 
# Prometheus scrapes the current values at each interval.
# NOTE: If metrics were defined inside the route handler, it would get re-created every time the route is called, 
# and Prometheus wouldn’t see an incrementing number.
# s.py, it's created once and stays in memory for the life of the app — so Prometheus can keep scraping and accumulating the correct values.
chat_turns_total = Counter(
    "chat_turns_total",
    "Total number of chat turns processed"
)
