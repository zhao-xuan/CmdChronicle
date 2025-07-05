"""
Word Cloud Generator
Creates word clouds and visualizations from command history data.
"""

import os
import re
from collections import Counter
from typing import List, Dict, Any
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from wordcloud import WordCloud
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class WordcloudGenerator:
    """Generates word clouds and visualizations from command data."""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers',
            'ours', 'theirs', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
            'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
            'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn',
            'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'
        }
        
        # Command-specific stop words
        self.command_stop_words = {
            'ls', 'cd', 'pwd', 'echo', 'cat', 'grep', 'find', 'cp', 'mv', 'rm',
            'mkdir', 'touch', 'chmod', 'chown', 'sudo', 'git', 'docker', 'kubectl',
            'python', 'node', 'npm', 'yarn', 'pip', 'conda', 'ssh', 'scp', 'rsync',
            'curl', 'wget', 'ping', 'telnet', 'netstat', 'ps', 'top', 'htop', 'df',
            'du', 'free', 'uptime', 'who', 'w', 'last', 'history', 'clear', 'exit',
            'logout', 'source', 'export', 'alias', 'unalias', 'function', 'if', 'then',
            'else', 'fi', 'for', 'while', 'do', 'done', 'case', 'esac', 'select',
            'until', 'break', 'continue', 'return', 'shift', 'set', 'unset', 'read',
            'printf', 'test', '[', ']', '[[', ']]', '(', ')', '{', '}', ';', '&', '|',
            '&&', '||', '>', '<', '>>', '<<', '2>', '2>>', '&>', '&>>', '|&'
        }
    
    def generate_wordcloud(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """
        Generate a word cloud from command data.
        
        Args:
            commands_data: List of command dictionaries
            output_dir: Directory to save the word cloud
            
        Returns:
            Path to the generated word cloud image
        """
        # Extract and process text
        text = self._extract_text_from_commands(commands_data)
        
        # Create word cloud
        wordcloud = self._create_wordcloud(text)
        
        # Save the word cloud
        output_path = Path(output_dir) / "command_wordcloud.png"
        wordcloud.to_file(str(output_path))
        
        return str(output_path)
    
    def generate_commemorative_page(self, commands_data: List[Dict[str, Any]], 
                                  insights_data: Dict[str, Any], output_dir: str) -> str:
        """
        Generate a commemorative page with visualizations.
        
        Args:
            commands_data: List of command dictionaries
            insights_data: AI-generated insights
            output_dir: Directory to save the page
            
        Returns:
            Path to the generated HTML page
        """
        # Create visualizations
        wordcloud_path = self.generate_wordcloud(commands_data, output_dir)
        command_frequency_path = self._generate_command_frequency_chart(commands_data, output_dir)
        tool_usage_path = self._generate_tool_usage_chart(commands_data, output_dir)
        
        # Generate HTML page
        html_path = self._generate_html_page(
            commands_data, insights_data, wordcloud_path, 
            command_frequency_path, tool_usage_path, output_dir
        )
        
        return html_path
    
    def _extract_text_from_commands(self, commands_data: List[Dict[str, Any]]) -> str:
        """Extract and process text from commands."""
        all_text = []
        
        for cmd in commands_data:
            command = cmd.get('command', '')
            
            # Split command into words
            words = re.findall(r'\b\w+\b', command.lower())
            
            # Filter out stop words and command-specific stop words
            filtered_words = [
                word for word in words 
                if (word not in self.stop_words and 
                    word not in self.command_stop_words and
                    len(word) > 2 and
                    not word.isdigit())
            ]
            
            all_text.extend(filtered_words)
        
        return ' '.join(all_text)
    
    def _create_wordcloud(self, text: str) -> WordCloud:
        """Create a word cloud from text."""
        # Count word frequencies
        word_counts = Counter(text.split())
        
        # Create word cloud
        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            random_state=42,
            font_path=self._get_font_path(),
            collocations=False
        )
        
        # Generate word cloud
        wordcloud.generate_from_frequencies(word_counts)
        
        return wordcloud
    
    def _get_font_path(self) -> str:
        """Get a suitable font path for the word cloud."""
        # Try to find a good font
        font_paths = [
            '/System/Library/Fonts/Helvetica.ttc',  # macOS
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
            'C:/Windows/Fonts/arial.ttf',  # Windows
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
        
        # Return None to use default font
        return None
    
    def _generate_command_frequency_chart(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate a command frequency chart."""
        # Count command frequencies
        command_counts = Counter(cmd['command'] for cmd in commands_data)
        top_commands = command_counts.most_common(15)
        
        if not top_commands:
            return ""
        
        # Create the chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        commands, counts = zip(*top_commands)
        
        # Create horizontal bar chart
        y_pos = np.arange(len(commands))
        bars = ax.barh(y_pos, counts, color='skyblue', alpha=0.7)
        
        # Customize the chart
        ax.set_yticks(y_pos)
        ax.set_yticklabels([cmd[:50] + '...' if len(cmd) > 50 else cmd for cmd in commands])
        ax.set_xlabel('Frequency')
        ax.set_title('Most Frequently Used Commands', fontsize=16, fontweight='bold')
        
        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                   str(count), ha='left', va='center', fontweight='bold')
        
        # Invert y-axis to show most frequent at top
        ax.invert_yaxis()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the chart
        output_path = Path(output_dir) / "command_frequency.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _generate_tool_usage_chart(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate a tool usage chart."""
        # Define tool categories
        tool_categories = {
            'git': ['git'],
            'docker': ['docker'],
            'kubernetes': ['kubectl', 'k8s'],
            'python': ['python', 'pip', 'conda'],
            'node': ['node', 'npm', 'yarn'],
            'system': ['sudo', 'apt', 'brew', 'yum'],
            'development': ['vim', 'code', 'subl'],
            'monitoring': ['top', 'htop', 'ps', 'df'],
            'network': ['ssh', 'scp', 'curl', 'wget'],
            'database': ['mysql', 'psql', 'sqlite']
        }
        
        # Count tool usage
        tool_counts = {}
        for category, keywords in tool_categories.items():
            count = sum(1 for cmd in commands_data 
                       if any(keyword in cmd['command'].lower() for keyword in keywords))
            if count > 0:
                tool_counts[category] = count
        
        if not tool_counts:
            return ""
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(tool_counts.keys())
        sizes = list(tool_counts.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'fontsize': 10})
        
        # Customize the chart
        ax.set_title('Tool Usage Distribution', fontsize=16, fontweight='bold')
        
        # Add legend
        ax.legend(wedges, labels, title="Tools", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the chart
        output_path = Path(output_dir) / "tool_usage.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _generate_html_page(self, commands_data: List[Dict[str, Any]], 
                          insights_data: Dict[str, Any], wordcloud_path: str,
                          command_frequency_path: str, tool_usage_path: str, output_dir: str) -> str:
        """Generate an HTML commemorative page."""
        
        # Get relative paths for images
        wordcloud_rel = Path(wordcloud_path).name if wordcloud_path else ""
        command_freq_rel = Path(command_frequency_path).name if command_frequency_path else ""
        tool_usage_rel = Path(tool_usage_path).name if tool_usage_path else ""
        
        # Generate statistics
        stats = self._calculate_statistics(commands_data)
        
        # Create HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CmdChronicle - Your Command Line Journey</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .content {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .insights {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .insights h2 {{
            margin-top: 0;
            font-size: 1.8em;
        }}
        .insights ul {{
            list-style: none;
            padding: 0;
        }}
        .insights li {{
            margin: 10px 0;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
        }}
        .visualizations {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        .viz-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .viz-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .personality {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .personality h2 {{
            margin-top: 0;
            font-size: 1.8em;
        }}
        .trait-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .trait-tag {{
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        .footer {{
            text-align: center;
            color: white;
            opacity: 0.8;
            font-size: 0.9em;
        }}
        @media (max-width: 768px) {{
            .visualizations {{
                grid-template-columns: 1fr;
            }}
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 {insights_data.get('fun_title', 'Your Command Line Journey')}</h1>
            <p>Generated on {insights_data.get('generated_at', 'Unknown date')}</p>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats['total_commands']}</div>
                    <div class="stat-label">Total Commands</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['unique_commands']}</div>
                    <div class="stat-label">Unique Commands</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['command_diversity']:.1%}</div>
                    <div class="stat-label">Command Diversity</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['automation_opportunities']}</div>
                    <div class="stat-label">Automation Opportunities</div>
                </div>
            </div>
            
            <div class="insights">
                <h2>🤖 AI Insights</h2>
                <ul>
                    <li><strong>Workflow Type:</strong> {insights_data.get('workflow_type', 'Unknown').replace('_', ' ').title()}</li>
                    <li><strong>Primary Focus:</strong> {insights_data.get('primary_focus', 'Unknown').replace('_', ' ').title()}</li>
                    <li><strong>Skill Level:</strong> {insights_data.get('skill_level', 'Unknown').title()}</li>
                    <li><strong>Most Used Tool:</strong> {insights_data.get('data_summary', {}).get('top_tools', ['Unknown'])[0] if insights_data.get('data_summary', {}).get('top_tools') else 'Unknown'}</li>
                </ul>
            </div>
            
            <div class="personality">
                <h2>🎭 Your Command Line Personality</h2>
                <div class="trait-tags">
                    {''.join([f'<span class="trait-tag">{trait}</span>' for trait in insights_data.get('personality_traits', [])])}
                </div>
            </div>
            
            <div class="visualizations">
                {f'<div class="viz-card"><h3>☁️ Command Word Cloud</h3><img src="{wordcloud_rel}" alt="Command Word Cloud"></div>' if wordcloud_rel else ''}
                {f'<div class="viz-card"><h3>📊 Command Frequency</h3><img src="{command_freq_rel}" alt="Command Frequency Chart"></div>' if command_freq_rel else ''}
                {f'<div class="viz-card"><h3>🛠️ Tool Usage</h3><img src="{tool_usage_rel}" alt="Tool Usage Chart"></div>' if tool_usage_rel else ''}
            </div>
            
            <div class="insights">
                <h2>💡 Recommendations</h2>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in insights_data.get('recommendations', [])])}
                </ul>
            </div>
            
            <div class="insights">
                <h2>🚀 Automation Opportunities</h2>
                <ul>
                    {''.join([f'<li>{opp}</li>' for opp in insights_data.get('automation_opportunities', [])])}
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by CmdChronicle - Your Command Line Journey Analyzer</p>
            <p>Model: {insights_data.get('model_used', 'Unknown')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML file
        output_path = Path(output_dir) / "commemorative_page.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _calculate_statistics(self, commands_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics for the commemorative page."""
        total_commands = len(commands_data)
        unique_commands = len(set(cmd['command'] for cmd in commands_data))
        command_diversity = unique_commands / total_commands if total_commands > 0 else 0
        
        # Count automation opportunities (commands with more than 3 words)
        automation_opportunities = sum(1 for cmd in commands_data if len(cmd['command'].split()) > 3)
        
        return {
            'total_commands': total_commands,
            'unique_commands': unique_commands,
            'command_diversity': command_diversity,
            'automation_opportunities': automation_opportunities
        } 