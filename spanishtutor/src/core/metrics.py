# spanishtutor/src/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Summary, Info
import time

# These variables live in memory and can be used from any part of the app by importing them. 
# Prometheus scrapes the current values at each interval.
# NOTE: If metrics were defined inside the route handler, it would get re-created every time the route is called, 
# and Prometheus wouldn't see an incrementing number.
# s.py, it's created once and stays in memory for the life of the app — so Prometheus can keep scraping and accumulating the correct values.

# === Core Chat Metrics ===
chat_turns_total = Counter(
    "chat_turns_total",
    "Total number of chat turns processed"
)

chat_requests_total = Counter(
    "chat_requests_total", 
    "Total number of chat requests received"
)

chat_response_latency = Histogram(
    "chat_response_latency_seconds", 
    "Time taken to respond to a chat request"
)

chat_chunks_total = Counter(
    "chat_chunks_total", 
    "Total number of LLM streaming chunks sent"
)

# === Error Metrics ===
llm_error_count = Counter(
    "llm_error_count", 
    "Total number of LLM errors", 
    ["error_type"]
)

# === User Behavior Metrics ===
user_level_gauge = Gauge(
    "active_user_level", 
    "Gauge for user level", 
    ["level"]
)

# === Application Info ===
app_info = Info(
    "spanishtutor_app", 
    "Info about the Spanish Tutor app"
)
