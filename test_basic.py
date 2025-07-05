#!/usr/bin/env python3
"""
Basic test script for CmdChronicle core functionality
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Test that core modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from collectors.history_collector import CommandHistoryCollector
        print("✅ CommandHistoryCollector imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CommandHistoryCollector: {e}")
        return False
    
    try:
        from analyzers.pattern_analyzer import PatternAnalyzer
        print("✅ PatternAnalyzer imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PatternAnalyzer: {e}")
        return False
    
    try:
        from utils.data_manager import DataManager
        print("✅ DataManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DataManager: {e}")
        return False
    
    try:
        from utils.config_manager import ConfigManager
        print("✅ ConfigManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ConfigManager: {e}")
        return False
    
    return True

def test_data_manager():
    """Test data manager functionality."""
    print("\n💾 Testing DataManager...")
    
    try:
        from utils.data_manager import DataManager
        
        # Create data manager
        data_manager = DataManager("test_data")
        
        # Test data
        test_commands = [
            {'command': 'git status', 'timestamp': 1704067200, 'shell': 'zsh'},
            {'command': 'ls -la', 'timestamp': 1704067260, 'shell': 'zsh'},
        ]
        
        # Save commands
        output_path = data_manager.save_commands(test_commands, 'test_data/test_commands.json')
        print(f"✅ Commands saved to: {output_path}")
        
        # Load commands
        loaded_commands = data_manager.load_commands('test_data/test_commands.json')
        print(f"✅ Commands loaded: {len(loaded_commands)} commands")
        
        # Get summary
        summary = data_manager.get_data_summary()
        print(f"✅ Data summary: {summary['total_files']} files")
        
        # Cleanup
        import shutil
        shutil.rmtree('test_data', ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"❌ DataManager test failed: {e}")
        return False

def test_config_manager():
    """Test config manager functionality."""
    print("\n⚙️ Testing ConfigManager...")
    
    try:
        from utils.config_manager import ConfigManager
        
        # Create config manager
        config_manager = ConfigManager("test_config")
        
        # Test getting values
        ollama_url = config_manager.get('ollama.base_url')
        print(f"✅ Ollama URL: {ollama_url}")
        
        # Test setting values
        config_manager.set('test.value', 'test_data')
        test_value = config_manager.get('test.value')
        print(f"✅ Test value set and retrieved: {test_value}")
        
        # Test validation
        validation = config_manager.validate_config()
        print(f"✅ Config validation: {validation['is_valid']}")
        
        # Cleanup
        import shutil
        shutil.rmtree('test_config', ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"❌ ConfigManager test failed: {e}")
        return False

def test_pattern_analyzer():
    """Test pattern analyzer functionality."""
    print("\n🧠 Testing PatternAnalyzer...")
    
    try:
        from analyzers.pattern_analyzer import PatternAnalyzer
        
        # Create analyzer
        analyzer = PatternAnalyzer()
        
        # Test data
        test_commands = [
            {'command': 'git status', 'timestamp': 1704067200, 'shell': 'zsh'},
            {'command': 'git add .', 'timestamp': 1704067260, 'shell': 'zsh'},
            {'command': 'git commit -m "test"', 'timestamp': 1704067320, 'shell': 'zsh'},
            {'command': 'ls -la', 'timestamp': 1704067380, 'shell': 'zsh'},
        ]
        
        # Analyze patterns
        patterns = analyzer.analyze_patterns(test_commands)
        
        print(f"✅ Patterns analyzed:")
        print(f"   - Frequent commands: {len(patterns['frequent_commands'])}")
        print(f"   - Automation candidates: {len(patterns['automation_candidates'])}")
        print(f"   - Tool usage: {list(patterns['tool_usage'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ PatternAnalyzer test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎯 CmdChronicle Basic Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_data_manager,
        test_config_manager,
        test_pattern_analyzer,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Core functionality is working.")
        print("\nTo install full dependencies:")
        print("  pip install -r requirements.txt")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 