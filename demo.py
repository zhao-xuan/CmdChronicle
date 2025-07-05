#!/usr/bin/env python3
"""
Demo script for CmdChronicle
Shows how to use the tool programmatically.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from collectors.history_collector import CommandHistoryCollector
from analyzers.pattern_analyzer import PatternAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from visualizers.wordcloud_generator import WordcloudGenerator
from utils.data_manager import DataManager

def main():
    print("🎯 CmdChronicle Demo")
    print("=" * 50)
    
    # Sample command data for demo
    sample_commands = [
        {'command': 'git status', 'timestamp': 1704067200, 'shell': 'zsh'},
        {'command': 'git add .', 'timestamp': 1704067260, 'shell': 'zsh'},
        {'command': 'git commit -m "Update documentation"', 'timestamp': 1704067320, 'shell': 'zsh'},
        {'command': 'git push origin main', 'timestamp': 1704067380, 'shell': 'zsh'},
        {'command': 'docker build -t myapp .', 'timestamp': 1704067440, 'shell': 'zsh'},
        {'command': 'docker run -p 3000:3000 myapp', 'timestamp': 1704067500, 'shell': 'zsh'},
        {'command': 'npm install', 'timestamp': 1704067560, 'shell': 'zsh'},
        {'command': 'npm run dev', 'timestamp': 1704067620, 'shell': 'zsh'},
        {'command': 'ls -la', 'timestamp': 1704067680, 'shell': 'zsh'},
        {'command': 'cd /path/to/project', 'timestamp': 1704067740, 'shell': 'zsh'},
    ]
    
    print(f"📊 Analyzing {len(sample_commands)} sample commands...")
    
    # 1. Pattern Analysis
    print("\n🔍 Step 1: Pattern Analysis")
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze_patterns(sample_commands)
    
    print(f"   - Found {len(patterns['frequent_commands'])} frequent commands")
    print(f"   - Identified {len(patterns['automation_candidates'])} automation opportunities")
    print(f"   - Tool usage: {list(patterns['tool_usage'].keys())}")
    
    # 2. AI Analysis (fallback mode)
    print("\n🤖 Step 2: AI Analysis")
    ai_analyzer = AIAnalyzer()
    insights = ai_analyzer.generate_insights(sample_commands, patterns)
    
    print(f"   - Workflow type: {insights.get('workflow_type', 'Unknown')}")
    print(f"   - Primary focus: {insights.get('primary_focus', 'Unknown')}")
    print(f"   - Skill level: {insights.get('skill_level', 'Unknown')}")
    print(f"   - Fun title: {insights.get('fun_title', 'Unknown')}")
    
    # 3. Save data
    print("\n💾 Step 3: Saving Data")
    data_manager = DataManager()
    data_manager.save_commands(sample_commands, 'data/demo_commands.json')
    data_manager.save_patterns(patterns, 'data/demo_patterns.json')
    data_manager.save_insights(insights, 'data/demo_insights.json')
    print("   - Data saved to data/ directory")
    
    # 4. Generate visualizations
    print("\n🎨 Step 4: Generating Visualizations")
    wordcloud_gen = WordcloudGenerator()
    wordcloud_path = wordcloud_gen.generate_wordcloud(sample_commands, 'reports')
    print(f"   - Word cloud generated: {wordcloud_path}")
    
    # 5. Generate commemorative page
    print("\n📄 Step 5: Generating Commemorative Page")
    html_path = wordcloud_gen.generate_commemorative_page(sample_commands, insights, 'reports')
    print(f"   - HTML page generated: {html_path}")
    
    print("\n🎉 Demo complete!")
    print("\nTo run the full tool:")
    print("  python cmdchronicle.py full_analysis")
    print("\nTo see all available commands:")
    print("  python cmdchronicle.py --help")

if __name__ == '__main__':
    main() 