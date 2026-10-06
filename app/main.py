from agent.planner import plan_shopping_request


request = "I need a laptop under ₹50,000 for gaming with good battery life."

result = plan_shopping_request(request)

print(result)