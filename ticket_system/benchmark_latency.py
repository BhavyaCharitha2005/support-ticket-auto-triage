"""
benchmark_latency.py
Measures and documents the exact latency calculation for scoring
"""

import pickle
import time
import numpy as np
import pandas as pd
from datetime import datetime

print("=" * 70)
print("LATENCY BENCHMARK AND CALCULATION FOR SCORING")
print("=" * 70)

# Load model and vectorizer
print("\n📦 Loading model and vectorizer...")
model = pickle.load(open("ticket_classifier_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

# Test cases for benchmarking
test_cases = [
    ("Login failed", "Cannot access my account with correct password"),
    ("Payment issue", "Double charge on my credit card"),
    ("Bug report", "Application crashes when clicking save"),
    ("Feature request", "Please add dark mode to the application"),
    ("Technical issue", "Server timeout error when accessing dashboard")
]

print(f"\n🧪 Running latency benchmark on {len(test_cases)} test cases...")

# Run benchmark
latencies = []
for subject, description in test_cases:
    full_text = subject + " " + description
    full_text = full_text.lower()
    
    # Time the prediction
    start_time = time.perf_counter()  # High precision timer
    
    # Transform
    text_vector = vectorizer.transform([full_text])
    
    # Predict
    prediction = model.predict(text_vector)[0]
    confidence = model.predict_proba(text_vector)[0].max()
    
    end_time = time.perf_counter()
    
    latency_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    latencies.append(latency_ms)
    
    print(f"  • '{subject[:20]}...': {latency_ms:.6f} ms → {prediction} ({confidence:.1%})")

# Calculate statistics
avg_latency = np.mean(latencies)
min_latency = np.min(latencies)
max_latency = np.max(latencies)
std_latency = np.std(latencies)

print(f"\n📊 LATENCY STATISTICS:")
print(f"  Average latency: {avg_latency:.6f} ms")
print(f"  Minimum latency: {min_latency:.6f} ms")
print(f"  Maximum latency: {max_latency:.6f} ms")
print(f"  Standard deviation: {std_latency:.6f} ms")

# Now calculate the SCORE according to PDF requirements
print("\n" + "=" * 70)
print("SCORING CALCULATION (as per PDF weights)")
print("=" * 70)

# PDF says: Latency is 10% of total score
# We need to normalize latency to a 0-1 scale

# Define scoring parameters (typical for ML systems)
MAX_ALLOWED_LATENCY = 100.0  # ms - reasonable upper bound for real-time systems
IDEAL_LATENCY = 1.0  # ms - perfect score latency

# Normalized latency score (closer to 1 is better)
# Formula: 1 - (actual_latency / max_allowed_latency)
# This gives us a score between 0 and 1
normalized_score = 1 - (avg_latency / MAX_ALLOWED_LATENCY)

print(f"\n📈 NORMALIZATION CALCULATION:")
print(f"  Average measured latency: {avg_latency:.6f} ms")
print(f"  Maximum allowed latency: {MAX_ALLOWED_LATENCY} ms (for real-time systems)")
print(f"  Normalized score = 1 - ({avg_latency:.6f} / {MAX_ALLOWED_LATENCY})")
print(f"  Normalized score = 1 - {avg_latency/MAX_ALLOWED_LATENCY:.6f}")
print(f"  Normalized score = {normalized_score:.6f}")

# Calculate points (10% of total 100 points = 10 points max)
latency_points = normalized_score * 10  # 10 points available for latency

print(f"\n🎯 POINTS CALCULATION (10% weight):")
print(f"  Available points for latency: 10.00")
print(f"  Earned points = {normalized_score:.6f} × 10")
print(f"  Earned points = {latency_points:.6f}")

# Round for final score
final_latency_points = round(latency_points, 2)

print(f"\n✅ FINAL LATENCY SCORE: {final_latency_points:.2f}/10.00 points")

# Save benchmark results to file
results = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'average_latency_ms': avg_latency,
    'min_latency_ms': min_latency,
    'max_latency_ms': max_latency,
    'std_latency_ms': std_latency,
    'max_allowed_latency_ms': MAX_ALLOWED_LATENCY,
    'normalized_score': normalized_score,
    'calculated_points': final_latency_points,
    'test_cases_used': len(test_cases)
}

import json
with open('latency_benchmark_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Results saved to: latency_benchmark_results.json")
print("\n" + "=" * 70)
print("✅ BENCHMARK COMPLETE")
print("=" * 70)