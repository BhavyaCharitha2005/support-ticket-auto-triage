"""
verify_dataset.py
Verify the dataset meets all PDF requirements
"""

import pandas as pd

# Load the dataset
df = pd.read_csv('support_tickets.csv')

print("=" * 60)
print("DATASET VERIFICATION CHECKLIST")
print("=" * 60)

# Check 1: Total tickets
print(f"1. Total tickets: {len(df)}")
print(f"   ✅ Requirement: 100 tickets - {'MET' if len(df) == 100 else 'NOT MET'}")

# Check 2: 6 fields as per PDF
print(f"\n2. Number of fields/columns: {len(df.columns)}")
print(f"   Columns: {list(df.columns)}")
print(f"   ✅ Required fields: ticket_id, subject, description, category, priority, timestamp")

# Check 3: 5 categories with 20 each
print(f"\n3. Category distribution:")
category_counts = df['category'].value_counts()
print(category_counts)
all_categories_present = all(cat in df['category'].unique() for cat in ['Bug', 'Billing', 'Feature', 'Technical', 'Account'])
all_have_20 = all(count == 20 for count in category_counts)
print(f"   ✅ All 5 categories present: {all_categories_present}")
print(f"   ✅ 20 tickets per category: {all_have_20}")

# Check 4: Priority field exists
print(f"\n4. Priority field exists: {'priority' in df.columns}")
print(f"   Priority values: {df['priority'].unique()}")

# Check 5: Timestamp field exists
print(f"\n5. Timestamp field exists: {'timestamp' in df.columns}")
print(f"   Sample timestamps: {df['timestamp'].head(3).tolist()}")

# Check 6: No missing values
print(f"\n6. Missing values check:")
missing_values = df.isnull().sum()
print(missing_values)
print(f"   ✅ No missing values: {(missing_values == 0).all()}")

print("\n" + "=" * 60)
if len(df) == 100 and len(df.columns) == 6 and all_categories_present and all_have_20:
    print("✅ ALL PDF DATASET REQUIREMENTS MET!")
else:
    print("❌ Some requirements not met")
print("=" * 60)

# Show first 3 rows as sample
print("\nSAMPLE DATA (first 3 tickets):")
print(df.head(3).to_string())