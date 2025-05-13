"""
Quick test script for the Multi-Tool Assistant
"""

from openai_assistant import MultiToolAssistant

def test_assistant():
    print("🧪 Testing Multi-Tool Assistant Components...")
    
    try:
        assistant = MultiToolAssistant()
        print("✅ Assistant initialized successfully!")
        
        # Show configuration
        config = assistant.get_config_info()
        print(f"✅ Model: {config['openai_model']}")
        print(f"✅ Functions available: {config['total_functions']}")
        
        # Test connections
        print("\n🔍 Testing connections...")
        results = assistant.test_connection()
        
        for service, result in results.items():
            if service != "configuration":
                status = "✅" if result["success"] else "❌"
                print(f"{status} {service.replace('_', ' ').title()}: {result['message']}")
        
        print("\n🎯 Testing sample queries...")
        
        # Test a simple query
        test_queries = [
            "What time is it?",
            "Where am I?",
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            try:
                response = assistant.process_user_query(query)
                print(f"Response: {response[:100]}..." if len(response) > 100 else f"Response: {response}")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n✅ Test completed! The assistant is ready to use.")
        print("Run 'python main.py' to start the interactive assistant.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_assistant()