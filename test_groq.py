from backend.services.groq_service import generate_response

print("Testing Groq API...")

answer = generate_response(
    "Explain Retrieval Augmented Generation in simple English."
)

print("\nGROQ RESPONSE:")
print(answer)