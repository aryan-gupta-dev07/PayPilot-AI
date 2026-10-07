from agent.planner import extract_intent


user_request = input("What are you looking to buy? ")

intent = extract_intent(user_request)

print("\nPayPilot AI - Extracted Intent:")
print(intent)