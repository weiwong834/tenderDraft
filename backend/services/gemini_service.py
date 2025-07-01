import os
import logging
from typing import List, Dict, Optional
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")

logger = logging.getLogger(__name__)

class GeminiService:
    """Service to interact with Google Gemini AI for tender optimization"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini AI service initialized successfully")
        else:
            self.model = None
            if not self.api_key:
                logger.warning("GEMINI_API_KEY not found in environment variables")
            if not GEMINI_AVAILABLE:
                logger.warning("Google Generative AI library not available")
    
    def optimize_tender_response(self, tender_description: str, company_description: str, 
                               relevant_tenders: List[Dict] = None) -> str:
        """Generate optimized tender response suggestions using Gemini AI"""
        
        if not self.model:
            return self._get_mock_optimization(tender_description, company_description)
        
        try:
            # Prepare context from relevant tenders
            tender_context = ""
            if relevant_tenders:
                tender_context = "\n\nRelevant market tenders for reference:\n"
                for i, tender in enumerate(relevant_tenders[:3], 1):
                    tender_context += f"{i}. {tender.get('title', 'N/A')} - "
                    tender_context += f"€{tender.get('value', 'N/A')} ({tender.get('country', 'N/A')})\n"
                    if tender.get('description'):
                        tender_context += f"   Description: {tender['description'][:200]}...\n"
            
            prompt = f"""
You are an expert tender consultant helping companies optimize their procurement responses.

TENDER REQUIREMENT:
{tender_description}

COMPANY PROFILE:
{company_description}

{tender_context}

Please provide a comprehensive tender optimization strategy including:

1. **Key Winning Factors**: What are the most important elements this tender is looking for?

2. **Competitive Positioning**: How should this company position itself based on their profile?

3. **Pricing Strategy**: Recommendations for competitive pricing based on market data

4. **Technical Approach**: Suggested technical approach and methodologies

5. **Risk Mitigation**: Potential risks and how to address them

6. **Proposal Structure**: Recommended structure for the tender response

7. **Compliance Checklist**: Key requirements that must be addressed

8. **Differentiators**: Unique selling points to highlight

Please provide actionable, specific advice that increases the chances of winning this tender.
"""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._get_mock_optimization(tender_description, company_description)
    
    def analyze_tender(self, tender_details: Dict) -> str:
        """Analyze a specific tender and provide insights"""
        
        if not self.model:
            return self._get_mock_analysis(tender_details)
        
        try:
            prompt = f"""
Analyze this tender opportunity and provide strategic insights:

TENDER DETAILS:
Title: {tender_details.get('title', 'N/A')}
Description: {tender_details.get('description', 'N/A')}
Estimated Value: €{tender_details.get('estimated_value', 'N/A')}
Deadline: {tender_details.get('deadline', 'N/A')}
Requirements: {', '.join(tender_details.get('requirements', []))}

Please provide:
1. Opportunity Assessment (High/Medium/Low and why)
2. Competition Level Analysis
3. Key Success Factors
4. Required Capabilities
5. Potential Challenges
6. Recommended Approach

Keep the analysis concise but comprehensive.
"""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return self._get_mock_analysis(tender_details)
    
    def generate_proposal_outline(self, tender_details: Dict, company_profile: str) -> str:
        """Generate a proposal outline for a specific tender"""
        
        if not self.model:
            return self._get_mock_proposal_outline()
        
        try:
            prompt = f"""
Create a detailed proposal outline for this tender:

TENDER: {tender_details.get('title', 'N/A')}
REQUIREMENTS: {tender_details.get('description', 'N/A')}
COMPANY: {company_profile}

Generate a structured proposal outline with:
1. Executive Summary points
2. Technical approach sections
3. Project methodology
4. Timeline considerations
5. Team structure
6. Risk management approach
7. Quality assurance measures

Format as a clear, actionable outline.
"""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini proposal outline error: {e}")
            return self._get_mock_proposal_outline()
    
    def _get_mock_optimization(self, tender_description: str, company_description: str) -> str:
        """Fallback mock optimization when Gemini is not available"""
        return f"""
## Tender Optimization Strategy (Mock Response)

**Tender**: {tender_description}
**Company**: {company_description}

### 1. Key Winning Factors
- Demonstrate relevant experience and expertise
- Competitive pricing with clear value proposition
- Strong technical approach aligned with requirements
- Proven track record in similar projects

### 2. Competitive Positioning
- Highlight unique capabilities and differentiators
- Emphasize innovation and modern approaches
- Showcase relevant certifications and partnerships
- Present strong team credentials

### 3. Pricing Strategy
- Research market rates for similar services
- Consider value-based pricing model
- Include detailed cost breakdown
- Offer flexible pricing options if appropriate

### 4. Technical Approach
- Align methodology with tender requirements
- Propose modern, efficient solutions
- Include quality assurance measures
- Address scalability and future needs

### 5. Risk Mitigation
- Identify potential project risks
- Present mitigation strategies
- Include contingency planning
- Demonstrate risk management experience

### 6. Compliance Checklist
- Review all tender requirements carefully
- Ensure all mandatory documents are included
- Meet submission deadlines and format requirements
- Address evaluation criteria systematically

*Note: This is a mock response. Connect Gemini AI for personalized optimization.*
"""
    
    def _get_mock_analysis(self, tender_details: Dict) -> str:
        """Fallback mock analysis"""
        return f"""
## Tender Analysis (Mock Response)

**Opportunity Assessment**: Medium - Good potential based on requirements alignment

**Competition Level**: Moderate - Expect 5-10 competitive bids

**Key Success Factors**:
- Technical expertise in required areas
- Competitive pricing
- Strong project management capabilities
- Relevant experience portfolio

**Required Capabilities**:
- Domain-specific knowledge
- Certified team members
- Project management framework
- Quality assurance processes

**Recommended Approach**:
- Focus on value proposition
- Highlight unique differentiators
- Present clear methodology
- Include risk mitigation strategies

*Note: This is a mock analysis. Connect Gemini AI for detailed insights.*
"""
    
    def _get_mock_proposal_outline(self) -> str:
        """Fallback mock proposal outline"""
        return """
## Proposal Outline (Mock Template)

### 1. Executive Summary
- Project understanding
- Our approach overview
- Key benefits and value proposition
- Team qualifications summary

### 2. Technical Approach
- Methodology and framework
- Implementation strategy
- Technology stack and tools
- Quality assurance measures

### 3. Project Management
- Project phases and milestones
- Timeline and deliverables
- Communication plan
- Risk management approach

### 4. Team and Experience
- Team structure and roles
- Key personnel qualifications
- Relevant project experience
- References and case studies

### 5. Commercial Proposal
- Cost breakdown
- Payment terms
- Value-added services
- Support and maintenance

### 6. Appendices
- Company certifications
- Detailed CVs
- Technical specifications
- Terms and conditions

*Note: This is a mock outline. Connect Gemini AI for customized proposals.*
"""

    def test_connection(self) -> bool:
        """Test if Gemini AI is properly configured and accessible"""
        if not self.model or not GEMINI_AVAILABLE:
            return False
        
        try:
            response = self.model.generate_content("Test connection")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False