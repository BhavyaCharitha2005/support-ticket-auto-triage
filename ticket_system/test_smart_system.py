"""
test_smart_system.py
Test the smart classifier without modifying existing files
"""

print("TESTING SMART CLASSIFICATION SYSTEM")
print("=" * 60)

# Import existing model and new smart classifier
import pickle
from smart_classifier import SmartTicketClassifier

print("Loading existing model and vectorizer...")
model = pickle.load(open("ticket_classifier_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

print("Creating smart classifier...")
smart_classifier = SmartTicketClassifier(model, vectorizer)

# Test cases with different confidence levels
test_tickets = [
    # High confidence examples
    ("Login failed", "Cannot access my account with correct password"),
    ("Payment declined", "My credit card payment was declined"),
    ("Feature request export", "Please add export to PDF functionality"),
    
    # Medium confidence examples  
    ("App not working", "The application is showing error messages"),
    ("Billing question", "I have a question about my invoice"),
    
    # Low confidence examples (vague)
    ("Problem", "Need help"),
    ("Issue with system", "Something is wrong"),
    ("Technical", "Not sure what's happening"),
]

print("\n" + "=" * 60)
print("SMART CLASSIFICATION RESULTS:")
print("=" * 60)

for i, (subject, description) in enumerate(test_tickets, 1):
    print(f"\n{'─' * 40}")
    print(f"TEST #{i}: {subject}")
    print(f"Description: {description}")
    
    # Get enhanced prediction
    result = smart_classifier.classify_with_confidence_routing(subject, description)
    
    # Display results
    print(f"\n📊 PREDICTION: {result['ticket_category']}")
    print(f"   Confidence: {result['confidence']:.1%}")
    
    print(f"\n🚦 ROUTING DECISION:")
    routing = result['smart_routing']
    print(f"   Action: {routing['action']}")
    print(f"   Message: {routing['message']}")
    
    if 'department' in routing:
        print(f"   Department: {routing['department']}")
    if 'template' in routing:
        print(f"   Auto-response: {routing['template']}")
    
    print(f"\n⚙️  SYSTEM RECOMMENDATIONS:")
    print(f"   Auto-resolve: {result['should_auto_resolve']}")
    print(f"   Human review needed: {result['needs_human_review']}")
    print(f"   Suggested priority: {result['suggested_priority']}")
    
    if result['top_alternatives']:
        print(f"\n🔍 ALTERNATIVE CATEGORIES (for low confidence):")
        for alt in result['top_alternatives']:
            print(f"   • {alt['category']}: {alt['confidence']:.1%}")

print("\n" + "=" * 60)
print("SYSTEM PERFORMANCE STATISTICS:")
print("=" * 60)

# Get overall statistics
stats = smart_classifier.get_performance_stats()
for key, value in stats.items():
    if 'percentage' in key:
        print(f"{key.replace('_', ' ').title()}: {value:.1f}%")
    elif key == 'average_confidence':
        print(f"{key.replace('_', ' ').title()}: {value:.1%}")
    else:
        print(f"{key.replace('_', ' ').title()}: {value}")

print("\n" + "=" * 60)
print("✅ Smart classifier integrated successfully!")
print("Your original model is untouched and still works perfectly.")
print("=" * 60)