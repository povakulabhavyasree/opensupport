TASKS = {
    "easy": {
        "name": "Order Tracking",
        "issue_type": "tracking",
        "customer_message": "Where is my order? It was supposed to arrive today.",
        "context": "Order ID: ORD12345, status: Out for delivery",
        "expected_keywords": ["delivery", "today", "tracking", "order"],
        "mood": "neutral"
    },

    "medium": {
        "name": "Refund for Damaged Product",
        "issue_type": "refund",
        "customer_message": "I received a damaged product. I want a refund immediately.",
        "context": "Order ID: ORD67890, product: Wireless Earbuds",
        "expected_keywords": ["refund", "return", "damaged", "process"],
        "mood": "frustrated"
    },

    "hard": {
        "name": "Angry Late Delivery Complaint",
        "issue_type": "delay",
        "customer_message": "This is ridiculous! My order is delayed by 3 days. I want compensation now!",
        "context": "Order ID: ORD99999, delayed by 3 days",
        "expected_keywords": ["delay", "apology", "compensation", "refund"],
        "mood": "angry"
    }
}

# ✅ compatibility
tasks = TASKS

def get_followup(task_key, step):
    return None