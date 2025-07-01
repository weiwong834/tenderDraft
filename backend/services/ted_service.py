import requests
import os
from typing import Dict, List, Optional
import json

class TEDService:
    """Service to interact with TED (Tenders Electronic Daily) API"""
    
    def __init__(self):
        self.base_url = "https://ted.europa.eu/api"
        self.api_key = os.getenv("TED_API_KEY")
    
    # Update your ted_service.py
    def search_tenders(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for tenders in TED database"""
        try:
            # Real TED API endpoint
            url = "https://ted.europa.eu/api/v2/notices"
            
            params = {
                'q': query,
                'limit': limit,
                'fields': 'title,value,country,cpv_divisions'
            }
            
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'TenderOptimizer/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error fetching TED data: {e}")
            # Fallback to mock data during development
            return self._get_mock_data()
    
    def get_tender_details(self, tender_id: str) -> Optional[Dict]:
        """Get detailed information about a specific tender"""
        try:
            # Mock detailed tender data
            mock_detail = {
                "id": tender_id,
                "title": "Industrial Equipment Supply Contract",
                "description": "Supply and installation of industrial automation equipment...",
                "estimated_value": 75000,
                "deadline": "2024-08-15",
                "requirements": [
                    "ISO 9001 certification",
                    "5+ years experience",
                    "EU presence required"
                ],
                "evaluation_criteria": {
                    "price": 60,
                    "technical": 30,
                    "experience": 10
                }
            }
            return mock_detail
        except Exception as e:
            print(f"Error fetching tender details: {e}")
            return None
        
    def _get_mock_tenders(self) -> List[Dict]:
        """Return mock tender data as fallback"""
        return [
            {
                "id": "12345-2024",
                "title": "Supply of Industrial Equipment",
                "value": 65000,
                "country": "DE",
                "sector": "Industrial machinery"
            },
            {
                "id": "67890-2024", 
                "title": "Automotive Parts Supply Contract",
                "value": 120000,
                "country": "FR",
                "sector": "Automotive"
            }
        ]
        