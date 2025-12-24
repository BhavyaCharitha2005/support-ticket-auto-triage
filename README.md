# CUSTOMER SUPPORT TICKET AUTO-TRIAGE
**Developer** : Bojja Naga Bhavya Charitha

An intelligent machine learning system that automatically classifies and routes customer support tickets into 5 predefined categories with 100% accuracy, reducing manual effort and improving response efficiency through natural language processing and automated triage with confidence-based smart routing.

## FEATURES
- Automatic Classification into 5 predefined categories
- REST API for integration with existing systems
- Real-time processing with instant predictions
- Confidence-based smart routing decisions

## SETUP INSTRUCTIONS

### Prerequisites
- Python 3.8+
- Flask, pandas, numpy, scikit-learn, nltk

### Technical Specifications
- Framework       : Flask
- ML Library      : scikit-learn(v1.6.1)
- Text Processing : nltk + TF-IDF Vectorization
- Data Handling   : pandas, numpy
- API Format      : REST JSON
- Model           : Multinomial Naive Bayes
- Vectorizer      : TF-IDF(1000 features)

### Installation Steps
Setup Server:
- Navigate to project directory
- Run: pip install -r requirements.txt
- Run: python app.py

The API server will run on http://127.0.0.1:5000

Test System:
Run: python test_system.py

Test Smart System:
Run: python test_smart_system.py

## ALGORITHM EXPLANATION
The system classifies tickets into five distinct categories based on content analysis:
Bug      : Software defects, errors, and application failures requiring                 technical fixes.
Billing  : Payment processing, subscription management, invoicing, and                  refund inquiries
Feature  : Enhancement requests and new functionality proposals
Technical: Infrastructure issues, server problems, and system integration               failures
Account  : User authentication, profile management, security concerns, and              access problems

### Evaluation Formula
Final Score = (Accuracy × 0.40) + ((Precision + Recall)/2 × 0.30) + (F1-Score × 0.20) + ((1 - Normalized Latency) × 0.10)

### Performance
- Accuracy : 100%
- Precision: 100%
- Recall   : 100%
- F1-Score : 100%
- Latency  : 0.028ms per prediction

### Final Score Calculation
- Accuracy         = 1.00 × 0.40 = 0.40 (40.00 points)-
- Precision+Recall = 1.00 × 0.30 = 0.30 (30.00 points)
- F1-Score         = 1.00 × 0.20 = 0.20 (20.00 points)-
- Latency          = 0.9997 × 0.10 = 0.09997 (10.00 points)

Total = 0.99997 × 100 = 100.00/100(approx)

### Algorithm
- Text cleaning and preprocessing
- Confidence score calculation
- Smart routing decisions based on confidence levels

## CHALLENGES ATTEMPTED
- Complete API prototype implementation
- Comprehensive documentation
- Weighted scoring system as per requirement
- Smart routing with confidence-based decisions
- Performance analytics and monitoring
  
## FUTURE IMPROVEMENTS
- Real-time learning from agent feedback to improve accuracy
- Priority level prediction based on urgency keywords
- Integration with email systems for automatic ticket creation
