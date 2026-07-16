"""
Quick smoke test against the running FastAPI server.
Usage: python test_requests.py
Requires: pip install httpx (already in requirements.txt)
"""
import httpx

BASE_URL = "http://localhost:8000"
API_KEY = "change-me"  # match .env

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def test_health():
    r = httpx.get(f"{BASE_URL}/health")
    print("health:", r.status_code, r.json())


def test_chat():
    r = httpx.post(
        f"{BASE_URL}/api/chat",
        headers=headers,
        json={"message": "What is Prisma used for?"},
        timeout=60,
    )
    print("chat:", r.status_code, r.json())


def test_agent():
    r = httpx.post(
        f"{BASE_URL}/api/agent/chat",
        headers=headers,
        json={"message": "What's the weather in Dallas?", "session_id": "test-session"},
        timeout=60,
    )
    print("agent:", r.status_code, r.json())


if __name__ == "__main__":
    test_health()
    test_chat()
    test_agent()
