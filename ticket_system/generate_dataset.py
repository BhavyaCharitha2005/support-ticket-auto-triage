"""
generate_dataset.py
Creates the required 100-ticket dataset with 6 fields as specified in the PDF
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Ticket categories as per PDF
categories = ['Bug', 'Billing', 'Feature', 'Technical', 'Account']

# Sample data for each category
ticket_templates = {
    'Bug': [
        ("Software crash", "Application crashes when clicking save button"),
        ("Login error", "Getting error message when trying to login"),
        ("Database issue", "Cannot connect to database, getting timeout"),
        ("Export failure", "PDF export feature not working properly"),
        ("UI glitch", "Buttons overlapping on mobile view"),
        ("Performance issue", "System running very slow during peak hours"),
        ("Data loss", "Entered data disappears after refresh"),
        ("File upload error", "Cannot upload files larger than 10MB"),
        ("Notification bug", "Not receiving email notifications"),
        ("Search not working", "Search function returns no results"),
        ("Calendar bug", "Wrong dates showing in calendar widget"),
        ("Print error", "Print preview shows blank pages"),
        ("Mobile app crash", "App crashes on Android when opening settings"),
        ("Payment gateway bug", "Payment fails with error code 500"),
        ("Report generation", "Reports show incorrect totals"),
        ("API timeout", "Third-party API calls timing out"),
        ("Cache issue", "Old data showing even after updates"),
        ("Security bug", "Password field showing plain text"),
        ("Browser compatibility", "Not working on Safari browser"),
        ("Memory leak", "Application memory usage keeps increasing")
    ],
    
    'Billing': [
        ("Invoice incorrect", "Received wrong amount on invoice"),
        ("Payment declined", "Credit card payment was declined"),
        ("Refund request", "Need refund for cancelled subscription"),
        ("Double charge", "Charged twice for same service"),
        ("Subscription renewal", "Auto-renewal charged incorrectly"),
        ("Tax calculation", "Tax amount seems incorrect on bill"),
        ("Late fee", "Charged late fee but paid on time"),
        ("Payment method", "Cannot update payment method"),
        ("Invoice not received", "Didn't receive monthly invoice"),
        ("Billing cycle", "Want to change billing cycle"),
        ("Discount not applied", "Promo code not working"),
        ("Receipt needed", "Need receipt for accounting"),
        ("Plan upgrade", "Charged wrong amount for upgrade"),
        ("Plan downgrade", "Refund for downgrade not processed"),
        ("Trial period", "Charged before trial ended"),
        ("Currency issue", "Charged in wrong currency"),
        ("Invoice duplicate", "Received duplicate invoices"),
        ("Payment history", "Cannot see payment history"),
        ("Auto-pay issue", "Auto-payment failed"),
        ("Bank transfer", "Bank transfer not reflecting")
    ],
    
    'Feature': [
        ("Export to PDF", "Need ability to export reports as PDF"),
        ("Dark mode", "Request for dark mode theme"),
        ("Mobile app", "Need mobile application version"),
        ("API access", "Want API for data integration"),
        ("Custom reports", "Need custom report builder"),
        ("Bulk actions", "Want bulk upload feature"),
        ("Two-factor auth", "Request for 2FA security"),
        ("Calendar integration", "Integrate with Google Calendar"),
        ("Language support", "Add Spanish language option"),
        ("Dashboard widgets", "Customizable dashboard widgets"),
        ("Email templates", "Custom email templates needed"),
        ("Workflow automation", "Automated workflow builder"),
        ("Real-time chat", "Add live chat support"),
        ("Analytics dashboard", "Advanced analytics features"),
        ("Import from Excel", "Import data from Excel files"),
        ("Voice commands", "Voice control feature request"),
        ("Offline mode", "Work offline capability"),
        ("Collaboration tools", "Team collaboration features"),
        ("Keyboard shortcuts", "More keyboard shortcuts"),
        ("Search filters", "Advanced search filters")
    ],
    
    'Technical': [
        ("Server down", "Website not loading, server error"),
        ("Slow performance", "Application very slow to respond"),
        ("Connection timeout", "Getting connection timeout errors"),
        ("Database slow", "Database queries taking too long"),
        ("Email not sending", "Cannot send emails from system"),
        ("File upload slow", "File uploads taking forever"),
        ("API rate limit", "Hitting API rate limits frequently"),
        ("SSL certificate", "SSL certificate warning showing"),
        ("CDN issue", "Static assets not loading properly"),
        ("Cache not clearing", "Cache not updating with changes"),
        ("DNS problem", "Domain not resolving correctly"),
        ("Firewall blocking", "Firewall blocking legitimate traffic"),
        ("Load balancer", "Load balancer configuration issue"),
        ("Backup failed", "Automated backup failed"),
        ("Monitoring alert", "Server monitoring alerts firing"),
        ("Database backup", "Database backup not completing"),
        ("SSL renewal", "SSL certificate renewal issue"),
        ("Server migration", "Issues after server migration"),
        ("Security scan", "Security vulnerability found"),
        ("Performance tuning", "Need performance optimization")
    ],
    
    'Account': [
        ("Password reset", "Cannot reset my password"),
        ("Login issue", "Account locked, cannot login"),
        ("Profile update", "Cannot update profile information"),
        ("Account merge", "Need to merge two accounts"),
        ("Access denied", "Getting access denied errors"),
        ("Account deletion", "Want to delete my account"),
        ("Permission issue", "Don't have correct permissions"),
        ("Two-factor setup", "Cannot setup two-factor auth"),
        ("Email change", "Need to change account email"),
        ("Username change", "Want to change username"),
        ("Account recovery", "Cannot recover deleted account"),
        ("Suspicious activity", "Account security alert"),
        ("Session timeout", "Getting logged out frequently"),
        ("Multiple accounts", "Accidentally created multiple accounts"),
        ("Verification issue", "Email verification not working"),
        ("Profile picture", "Cannot upload profile picture"),
        ("Privacy settings", "Privacy settings not saving"),
        ("Notification settings", "Cannot change notification settings"),
        ("Language preference", "Language setting not sticking"),
        ("Time zone issue", "Time zone not updating correctly")
    ]
}

# Priority levels
priorities = ['Low', 'Medium', 'High', 'Critical']

# Generate 100 tickets (20 per category)
tickets = []
ticket_id = 1000

# Start date for timestamps
base_date = datetime(2024, 1, 1, 9, 0, 0)

for category in categories:
    for i in range(20):  # 20 tickets per category
        ticket_id += 1
        
        # Get random template for this category
        subject, description = random.choice(ticket_templates[category])
        
        # Add some variation to make them unique
        if i % 3 == 0:
            description = f"Urgent: {description}"
        elif i % 5 == 0:
            description = f"Important: {description}. Need quick resolution."
        
        # Assign priority based on category and random chance
        if category == 'Bug':
            priority = random.choice(['High', 'Critical', 'Medium'])
        elif category == 'Account':
            priority = random.choice(['High', 'Medium', 'Low'])
        else:
            priority = random.choice(priorities)
        
        # Generate timestamp (spread over 30 days)
        days_offset = random.randint(0, 30)
        hours_offset = random.randint(0, 8)  # Business hours
        timestamp = base_date + timedelta(days=days_offset, hours=hours_offset)
        
        tickets.append({
            'ticket_id': ticket_id,
            'subject': subject,
            'description': description,
            'category': category,
            'priority': priority,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

# Create DataFrame
df = pd.DataFrame(tickets)

# Save to CSV
df.to_csv('support_tickets.csv', index=False)
print(f"✅ Dataset created with {len(df)} tickets")
print(f"📊 Category distribution:")
print(df['category'].value_counts())
print(f"\n📊 Priority distribution:")
print(df['priority'].value_counts())
print(f"\n💾 Saved to: support_tickets.csv")
print(f"📅 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")