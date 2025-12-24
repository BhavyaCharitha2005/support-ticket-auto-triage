print("CUSTOMER SUPPORT TICKET TESTER")
print("=" * 40)

# Load model
import pickle
model = pickle.load(open("ticket_classifier_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

print("Model loaded successfully")

# Test cases
tests = [
    ("Login failed", "Cannot access account"),
    ("Payment issue", "Double charge on card"),
    ("Feature request", "Add export feature"),
    ("Bug report", "Application crashes"),
    ("Technical issue", "Server timeout")
]

print("\nTest Results:")
for subject, desc in tests:
    text = subject + " " + desc
    text = text.lower()
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    conf = model.predict_proba(vec)[0].max()
    print(f"{subject}: {pred} ({conf:.1%})")

print("\nTEST COMPLETE")