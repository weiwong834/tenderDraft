from services.ted_service import TEDService
import logging

logging.basicConfig(level=logging.INFO)

def test_ted():
    ted = TEDService()
    
    # Test connection
    print("Testing TED API connection...")
    if ted.test_connection():
        print("✅ TED API is accessible")
    else:
        print("❌ TED API connection failed")
    
    # Test search
    print("\nTesting search...")
    results = ted.search_tenders("software development", limit=5)
    print(f"Found {len(results)} results")
    
    for result in results[:2]:  # Show first 2
        print(f"- {result['title']} ({result['country']}) - €{result.get('value', 'N/A')}")

if __name__ == "__main__":
    test_ted()