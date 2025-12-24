"""
smart_classifier.py
SMART CONFIDENCE-BASED TICKET ROUTING SYSTEM
Enhances the existing model by adding intelligent routing decisions
"""

import time
from datetime import datetime
import re

class SmartTicketClassifier:
    """
    Wrapper around the existing model that adds confidence-based routing.
    This DOES NOT modify the trained model - it just makes smarter decisions
    using the model's outputs.
    """
    
    def __init__(self, model, vectorizer):
        """
        Initialize with the existing trained model and vectorizer.
        
        Args:
            model: Your existing trained MultinomialNB model
            vectorizer: Your existing TF-IDF vectorizer
        """
        self.model = model  # Your existing model - untouched!
        self.vectorizer = vectorizer  # Your existing vectorizer - untouched!
        self.prediction_history = []
        
    def classify_with_confidence_routing(self, subject, description):
        """
        Enhanced classification that includes confidence-based routing decisions.
        
        Args:
            subject: Ticket subject (string)
            description: Ticket description (string)
        
        Returns:
            Dictionary with classification PLUS routing recommendations
        """
        # Step 1: Get prediction from EXISTING model (NO CHANGES)
        full_text = subject + ' ' + description
        cleaned_text = self._clean_text(full_text)
        text_vector = self.vectorizer.transform([cleaned_text])
        
        prediction = self.model.predict(text_vector)[0]  # Existing prediction
        probabilities = self.model.predict_proba(text_vector)[0]  # All category probabilities
        confidence = float(probabilities.max())  # Highest probability (0 to 1)
        
        # Step 2: MAKE SMART ROUTING DECISIONS (NEW ENHANCEMENT)
        routing_info = self._get_routing_recommendation(prediction, confidence)
        
        # Step 3: Log this prediction for analytics
        self._log_prediction(subject[:50], prediction, confidence)
        
        # Step 4: Return enhanced response
        return {
            # Existing fields (for backward compatibility):
            'ticket_category': prediction,
            'confidence': confidence,
            
            # NEW ENHANCED FIELDS:
            'smart_routing': routing_info,
            'should_auto_resolve': confidence > 0.9,
            'needs_human_review': confidence < 0.7,
            'suggested_priority': self._calculate_priority(confidence, prediction),
            'top_alternatives': self._get_top_alternatives(probabilities, confidence)
        }
    
    def _clean_text(self, text):
        """Simple text cleaning (same as before)"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return ' '.join(text.split())
    
    def _get_routing_recommendation(self, category, confidence):
        """
        Determine how to route this ticket based on confidence level.
        
        Confidence Rules:
        - > 0.9: Auto-resolve with template response
        - 0.7-0.9: Route to appropriate department automatically
        - < 0.7: Flag for human review
        """
        if confidence > 0.9:
            return {
                'action': 'AUTO_RESOLVE',
                'message': 'High confidence - can be auto-resolved',
                'template': self._get_response_template(category)
            }
        elif confidence >= 0.7:
            return {
                'action': 'AUTO_ROUTE',
                'message': f'Route to {category} department',
                'department': self._get_department(category)
            }
        else:
            return {
                'action': 'HUMAN_REVIEW',
                'message': 'Low confidence - needs agent review',
                'urgency': 'HIGH' if 'error' in category.lower() or 'bug' in category.lower() else 'NORMAL'
            }
    
    def _get_department(self, category):
        """Map categories to support departments"""
        department_map = {
            'Bug': 'Technical Support - Tier 2',
            'Technical': 'Technical Support - Tier 1',
            'Billing': 'Finance Department',
            'Account': 'Customer Success',
            'Feature': 'Product Management'
        }
        return department_map.get(category, 'General Support')
    
    def _calculate_priority(self, confidence, category):
        """Calculate ticket priority based on confidence and category"""
        if confidence < 0.7:
            return 'HIGH'  # Low confidence = needs attention
        elif category in ['Bug', 'Technical']:
            return 'MEDIUM-HIGH'
        else:
            return 'MEDIUM'
    
    def _get_top_alternatives(self, probabilities, confidence):
        """Return top alternative categories if confidence is low"""
        if confidence >= 0.8:
            return []  # High confidence, no alternatives needed
        
        # Get indices of top 3 probabilities
        top_3_indices = probabilities.argsort()[-3:][::-1]
        alternatives = []
        
        for idx in top_3_indices[1:]:  # Skip the top one (already predicted)
            cat = self.model.classes_[idx]
            prob = probabilities[idx]
            if prob > 0.1:  # Only include reasonable alternatives
                alternatives.append({
                    'category': cat,
                    'confidence': float(prob)
                })
        
        return alternatives
    
    def _get_response_template(self, category):
        """Get auto-response template for high-confidence predictions"""
        templates = {
            'Bug': "We've identified this as a known bug. Our development team is working on a fix.",
            'Billing': "Your billing inquiry has been received. Our finance team will contact you within 24 hours.",
            'Account': "Your account issue has been logged. Please check your email for reset instructions.",
            'Technical': "We're aware of this technical issue. Please try clearing your cache and restarting.",
            'Feature': "Thank you for your feature request! Our product team will review this suggestion."
        }
        return templates.get(category, "We've received your ticket and will respond soon.")
    
    def _log_prediction(self, subject, category, confidence):
        """Log prediction for analytics and monitoring"""
        self.prediction_history.append({
            'timestamp': datetime.now().isoformat(),
            'subject': subject,
            'category': category,
            'confidence': confidence
        })
    
    def get_performance_stats(self):
        """Get statistics about classification performance"""
        if not self.prediction_history:
            return {"total_predictions": 0}
        
        total = len(self.prediction_history)
        high_conf = sum(1 for p in self.prediction_history if p['confidence'] > 0.9)
        low_conf = sum(1 for p in self.prediction_history if p['confidence'] < 0.7)
        
        return {
            'total_predictions': total,
            'high_confidence_predictions': high_conf,
            'low_confidence_predictions': low_conf,
            'auto_resolvable_percentage': (high_conf / total * 100) if total > 0 else 0,
            'needs_human_review_percentage': (low_conf / total * 100) if total > 0 else 0,
            'average_confidence': sum(p['confidence'] for p in self.prediction_history) / total if total > 0 else 0
        }