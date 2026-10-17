# D:\AI-Tools\convermem\tests\test_filter.py
from convermem.filter import ConversationFilter

def test_filter_by_topic():
    turns = [
        {"user": "Let's build a payment gateway", "model": "Use Stripe API", "time": "2026-10-17T10:00:00Z"},
        {"user": "What is the weather?", "model": "Sunny today", "time": "2026-10-17T10:05:00Z"}
    ]
    cf = ConversationFilter()
    filtered = cf.filter_turns(turns, topic="payment,stripe")
    assert len(filtered) == 1
    assert "payment" in filtered[0]["user"]
