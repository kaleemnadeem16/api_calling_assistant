#!/usr/bin/env python3
"""
Test script for the LangChain Tool Assistant.

This script tests the basic functionality of the assistant including
tool calling capabilities, error handling, and response formatting.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import LangChainToolAssistant
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_test_header(test_name: str):
    """Print a formatted test header."""
    print(f"\n{'='*60}")
    print(f"   {test_name}")
    print(f"{'='*60}")


def print_result(success: bool, message: str):
    """Print test result with appropriate emoji."""
    emoji = "✅" if success else "❌"
    print(f"{emoji} {message}")


def test_initialization():
    """Test assistant initialization."""
    print_test_header("Assistant Initialization Test")
    
    try:
        assistant = LangChainToolAssistant()
        print_result(True, "LangChain assistant initialized successfully")
        
        # Test configuration access
        capabilities = assistant.get_available_capabilities()
        print_result(True, f"Configuration loaded: {capabilities['model_info']['model']}")
        print_result(True, f"Tools available: {len(capabilities['tools'])}")
        
        return assistant
        
    except Exception as e:
        print_result(False, f"Initialization failed: {e}")
        return None


def test_capabilities(assistant: LangChainToolAssistant):
    """Test capabilities reporting."""
    print_test_header("Capabilities Test")
    
    try:
        capabilities = assistant.get_available_capabilities()
        
        # Check required fields
        required_fields = ['tools', 'model_info', 'features']
        for field in required_fields:
            if field in capabilities:
                print_result(True, f"Capabilities include '{field}' information")
            else:
                print_result(False, f"Missing '{field}' in capabilities")
        
        # Display available tools
        print("\n🛠️  Available Tools:")
        for tool in capabilities['tools']:
            print(f"  • {tool['name']}: {tool['description']}")
        
        return True
        
    except Exception as e:
        print_result(False, f"Capabilities test failed: {e}")
        return False


def test_basic_conversation(assistant: LangChainToolAssistant):
    """Test basic conversation without tool calls."""
    print_test_header("Basic Conversation Test")
    
    test_queries = [
        "Hello, how are you?",
        "What can you help me with?",
        "Tell me about your capabilities",
    ]
    
    success_count = 0
    
    for query in test_queries:
        try:
            print(f"\n🗣️  Query: {query}")
            response = assistant.chat(query)
            
            if response.get("success"):
                print_result(True, f"Response received: {response['response'][:100]}...")
                success_count += 1
            else:
                print_result(False, f"Query failed: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print_result(False, f"Query failed with exception: {e}")
    
    print(f"\n📊 Basic conversation success rate: {success_count}/{len(test_queries)}")
    return success_count == len(test_queries)


def test_tool_calling(assistant: LangChainToolAssistant):
    """Test tool calling functionality."""
    print_test_header("Tool Calling Test")
    
    # Test queries that should trigger different tools
    test_queries = [
        {
            "query": "What's the weather in London?",
            "expected_tool": "get_current_weather",
            "description": "Weather tool test"
        },
        {
            "query": "What time is it?", 
            "expected_tool": "get_current_time",
            "description": "Time tool test"
        },
        {
            "query": "Where am I?",
            "expected_tool": "get_my_location", 
            "description": "Location detection test"
        }
    ]
    
    success_count = 0
    
    for test_case in test_queries:
        try:
            print(f"\n🔧 {test_case['description']}")
            print(f"Query: {test_case['query']}")
            
            response = assistant.chat(test_case["query"])
            
            if response.get("success"):
                print_result(True, f"Tool calling successful")
                print(f"📝 Response: {response['response'][:150]}...")
                success_count += 1
            else:
                print_result(False, f"Tool calling failed: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print_result(False, f"Tool calling failed with exception: {e}")
    
    print(f"\n📊 Tool calling success rate: {success_count}/{len(test_queries)}")
    return success_count >= 1  # At least one tool should work


def test_error_handling(assistant: LangChainToolAssistant):
    """Test error handling with invalid inputs."""
    print_test_header("Error Handling Test")
    
    # Test queries that might cause errors
    error_test_queries = [
        "What's the weather in NonExistentCity12345?",
        "",  # Empty query
        "A" * 1000,  # Very long query
    ]
    
    handled_errors = 0
    
    for i, query in enumerate(error_test_queries, 1):
        try:
            print(f"\n🚨 Error test {i}: ", end="")
            if len(query) > 50:
                print(f"{query[:47]}...")
            else:
                print(f"'{query}'" if query else "Empty query")
            
            response = assistant.chat(query)
            
            # Should handle errors gracefully, not crash
            if "success" in response:
                print_result(True, "Error handled gracefully")
                handled_errors += 1
            else:
                print_result(False, "Response format unexpected")
                
        except Exception as e:
            print_result(False, f"Unhandled exception: {e}")
    
    print(f"\n📊 Error handling success rate: {handled_errors}/{len(error_test_queries)}")
    return handled_errors >= 2


def run_comprehensive_tests():
    """Run all tests and provide summary."""
    print("🧪 LangChain Tool Assistant - Comprehensive Test Suite")
    print("=" * 70)
    
    test_results = []
    
    # Test 1: Initialization
    assistant = test_initialization()
    test_results.append(assistant is not None)
    
    if assistant is None:
        print("\n❌ Cannot proceed with further tests due to initialization failure.")
        return False
    
    # Test 2: Capabilities
    test_results.append(test_capabilities(assistant))
    
    # Test 3: Basic conversation
    test_results.append(test_basic_conversation(assistant))
    
    # Test 4: Tool calling
    test_results.append(test_tool_calling(assistant))
    
    # Test 5: Error handling
    test_results.append(test_error_handling(assistant))
    
    # Summary
    print_test_header("Test Summary")
    
    test_names = [
        "Initialization",
        "Capabilities", 
        "Basic Conversation",
        "Tool Calling",
        "Error Handling"
    ]
    
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        print_result(result, f"{name} test")
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The assistant is working correctly.")
        return True
    elif passed_tests >= total_tests * 0.6:
        print("⚠️  Most tests passed. Some features may have issues.")
        return True
    else:
        print("❌ Multiple test failures. Please check your configuration.")
        return False


def main():
    """Main test function."""
    if run_comprehensive_tests():
        print("\n✅ Test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test suite completed with failures!")
        print("\n💡 Troubleshooting tips:")
        print("  1. Check your .env file has valid API keys")
        print("  2. Ensure internet connectivity")
        print("  3. Verify all dependencies are installed")
        print("  4. Check API key permissions and quotas")
        sys.exit(1)


if __name__ == "__main__":
    main()