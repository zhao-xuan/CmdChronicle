"""
Report Generator
Generates comprehensive reports and visualizations from analysis results.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
from jinja2 import Template


class ReportGenerator:
    """Generates comprehensive reports and visualizations."""
    
    def __init__(self):
        # Set style for matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Color schemes
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#4facfe',
            'warning': '#f093fb',
            'danger': '#f5576c',
            'info': '#00f2fe'
        }
    
    def generate_report(self, commands_data: List[Dict[str, Any]], 
                       insights_data: Dict[str, Any], output_dir: str) -> str:
        """
        Generate a comprehensive report with visualizations.
        
        Args:
            commands_data: List of command dictionaries
            insights_data: AI-generated insights
            output_dir: Directory to save the report
            
        Returns:
            Path to the generated report
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate visualizations
        viz_paths = self._generate_visualizations(commands_data, insights_data, output_dir)
        
        # Generate comprehensive report
        report_path = self._generate_comprehensive_report(
            commands_data, insights_data, viz_paths, output_dir
        )
        
        return report_path
    
    def _generate_visualizations(self, commands_data: List[Dict[str, Any]], 
                               insights_data: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Generate all visualizations for the report."""
        viz_paths = {}
        
        # Time-based analysis
        viz_paths['time_analysis'] = self._generate_time_analysis(commands_data, output_dir)
        
        # Command complexity analysis
        viz_paths['complexity_analysis'] = self._generate_complexity_analysis(commands_data, output_dir)
        
        # Workflow patterns
        viz_paths['workflow_patterns'] = self._generate_workflow_patterns(commands_data, output_dir)
        
        # Automation opportunities
        viz_paths['automation_opportunities'] = self._generate_automation_chart(commands_data, output_dir)
        
        # Skill progression
        viz_paths['skill_progression'] = self._generate_skill_progression(commands_data, output_dir)
        
        return viz_paths
    
    def _generate_time_analysis(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate time-based analysis visualizations."""
        if not commands_data:
            return ""
        
        # Extract timestamps
        timestamps = [cmd.get('timestamp', 0) for cmd in commands_data if 'timestamp' in cmd]
        if not timestamps:
            return ""
        
        # Convert to datetime objects
        dates = [datetime.fromtimestamp(ts) for ts in timestamps]
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Hourly distribution
        hours = [d.hour for d in dates]
        hour_counts = np.bincount(hours, minlength=24)
        ax1.bar(range(24), hour_counts, color=self.colors['primary'], alpha=0.7)
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Number of Commands')
        ax1.set_title('Command Activity by Hour')
        ax1.set_xticks(range(0, 24, 2))
        
        # 2. Daily distribution
        days = [d.strftime('%A') for d in dates]
        day_counts = {}
        for day in days:
            day_counts[day] = day_counts.get(day, 0) + 1
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_values = [day_counts.get(day, 0) for day in day_order]
        
        ax2.bar(day_order, day_values, color=self.colors['secondary'], alpha=0.7)
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Number of Commands')
        ax2.set_title('Command Activity by Day')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Command frequency over time
        sorted_dates = sorted(dates)
        command_counts = []
        time_points = []
        
        # Group by day
        current_date = None
        current_count = 0
        
        for date in sorted_dates:
            date_str = date.strftime('%Y-%m-%d')
            if date_str != current_date:
                if current_date:
                    time_points.append(current_date)
                    command_counts.append(current_count)
                current_date = date_str
                current_count = 1
            else:
                current_count += 1
        
        if current_date:
            time_points.append(current_date)
            command_counts.append(current_count)
        
        if time_points:
            ax3.plot(range(len(time_points)), command_counts, 
                    color=self.colors['success'], linewidth=2, marker='o')
            ax3.set_xlabel('Day')
            ax3.set_ylabel('Commands per Day')
            ax3.set_title('Command Activity Over Time')
            ax3.set_xticks(range(0, len(time_points), max(1, len(time_points)//5)))
            ax3.set_xticklabels([time_points[i] for i in range(0, len(time_points), max(1, len(time_points)//5))], rotation=45)
        
        # 4. Activity heatmap
        activity_matrix = np.zeros((7, 24))
        for date in dates:
            day_idx = date.weekday()
            hour_idx = date.hour
            activity_matrix[day_idx, hour_idx] += 1
        
        im = ax4.imshow(activity_matrix, cmap='YlOrRd', aspect='auto')
        ax4.set_xlabel('Hour of Day')
        ax4.set_ylabel('Day of Week')
        ax4.set_title('Activity Heatmap')
        ax4.set_xticks(range(0, 24, 4))
        ax4.set_yticks(range(7))
        ax4.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        
        plt.colorbar(im, ax=ax4, label='Number of Commands')
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = Path(output_dir) / "time_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _generate_complexity_analysis(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate command complexity analysis."""
        if not commands_data:
            return ""
        
        # Analyze command complexity
        complexities = []
        word_counts = []
        flag_counts = []
        
        for cmd in commands_data:
            command = cmd.get('command', '')
            words = command.split()
            
            # Word count
            word_count = len(words)
            word_counts.append(word_count)
            
            # Flag count (arguments starting with - or --)
            flags = sum(1 for word in words if word.startswith('-'))
            flag_counts.append(flags)
            
            # Complexity score (simple heuristic)
            complexity = word_count + flags * 2
            if '|' in command:
                complexity += 3  # Pipes add complexity
            if '>' in command or '<' in command:
                complexity += 2  # Redirection adds complexity
            if '&&' in command or '||' in command:
                complexity += 4  # Logical operators add complexity
            
            complexities.append(complexity)
        
        # Create visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Complexity distribution
        ax1.hist(complexities, bins=20, color=self.colors['primary'], alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Command Complexity Score')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Command Complexity Distribution')
        ax1.axvline(np.mean(complexities), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(complexities):.1f}')
        ax1.legend()
        
        # 2. Word count distribution
        ax2.hist(word_counts, bins=15, color=self.colors['secondary'], alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Number of Words')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Command Word Count Distribution')
        ax2.axvline(np.mean(word_counts), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(word_counts):.1f}')
        ax2.legend()
        
        # 3. Flag usage
        ax3.hist(flag_counts, bins=10, color=self.colors['success'], alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Number of Flags')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Command Flag Usage')
        
        # 4. Complexity vs frequency scatter
        command_freq = {}
        for cmd in commands_data:
            command = cmd.get('command', '')
            command_freq[command] = command_freq.get(command, 0) + 1
        
        # Get complexity for unique commands
        unique_commands = list(command_freq.keys())
        unique_complexities = []
        unique_frequencies = []
        
        for cmd in unique_commands:
            words = cmd.split()
            word_count = len(words)
            flags = sum(1 for word in words if word.startswith('-'))
            complexity = word_count + flags * 2
            if '|' in cmd:
                complexity += 3
            if '>' in cmd or '<' in cmd:
                complexity += 2
            if '&&' in cmd or '||' in cmd:
                complexity += 4
            
            unique_complexities.append(complexity)
            unique_frequencies.append(command_freq[cmd])
        
        ax4.scatter(unique_complexities, unique_frequencies, alpha=0.6, color=self.colors['warning'])
        ax4.set_xlabel('Command Complexity')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Complexity vs Frequency')
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = Path(output_dir) / "complexity_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _generate_workflow_patterns(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate workflow pattern analysis."""
        if not commands_data:
            return ""
        
        # Analyze command sequences
        sequences = []
        for i in range(len(commands_data) - 1):
            seq = f"{commands_data[i]['command']} → {commands_data[i+1]['command']}"
            sequences.append(seq)
        
        # Count sequence frequencies
        sequence_counts = {}
        for seq in sequences:
            sequence_counts[seq] = sequence_counts.get(seq, 0) + 1
        
        # Get top sequences
        top_sequences = sorted(sequence_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if not top_sequences:
            return ""
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 1. Top command sequences
        sequences, counts = zip(*top_sequences)
        y_pos = np.arange(len(sequences))
        
        bars = ax1.barh(y_pos, counts, color=self.colors['primary'], alpha=0.7)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels([seq[:60] + '...' if len(seq) > 60 else seq for seq in sequences])
        ax1.set_xlabel('Frequency')
        ax1.set_title('Most Common Command Sequences')
        ax1.invert_yaxis()
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    str(count), ha='left', va='center', fontweight='bold')
        
        # 2. Command type analysis
        command_types = {}
        for cmd in commands_data:
            command = cmd.get('command', '')
            base_cmd = command.split()[0] if command.split() else ''
            
            # Categorize commands
            if base_cmd in ['git', 'docker', 'kubectl', 'python', 'node', 'npm']:
                category = base_cmd
            elif base_cmd in ['ls', 'cd', 'pwd', 'find', 'grep']:
                category = 'file_ops'
            elif base_cmd in ['sudo', 'apt', 'brew', 'yum']:
                category = 'system'
            elif base_cmd in ['ssh', 'scp', 'curl', 'wget']:
                category = 'network'
            else:
                category = 'other'
            
            command_types[category] = command_types.get(category, 0) + 1
        
        if command_types:
            categories, type_counts = zip(*command_types.items())
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            
            wedges, texts, autotexts = ax2.pie(type_counts, labels=categories, colors=colors, 
                                              autopct='%1.1f%%', startangle=90)
            ax2.set_title('Command Type Distribution')
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = Path(output_dir) / "workflow_patterns.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _generate_automation_chart(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate automation opportunities chart."""
        if not commands_data:
            return ""
        
        # Analyze automation potential
        automation_scores = []
        command_texts = []
        
        for cmd in commands_data:
            command = cmd.get('command', '')
            score = self._calculate_automation_score(command)
            automation_scores.append(score)
            command_texts.append(command)
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 1. Automation score distribution
        ax1.hist(automation_scores, bins=20, color=self.colors['warning'], alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Automation Score')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Command Automation Potential')
        ax1.axvline(0.5, color='red', linestyle='--', label='High automation threshold')
        ax1.legend()
        
        # 2. Top automation candidates
        # Create list of (command, score) tuples
        command_scores = list(zip(command_texts, automation_scores))
        command_scores.sort(key=lambda x: x[1], reverse=True)
        
        top_candidates = command_scores[:10]
        candidates, scores = zip(*top_candidates)
        
        y_pos = np.arange(len(candidates))
        bars = ax2.barh(y_pos, scores, color=self.colors['danger'], alpha=0.7)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels([cmd[:50] + '...' if len(cmd) > 50 else cmd for cmd in candidates])
        ax2.set_xlabel('Automation Score')
        ax2.set_title('Top Automation Candidates')
        ax2.invert_yaxis()
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{score:.2f}', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = Path(output_dir) / "automation_opportunities.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _calculate_automation_score(self, command: str) -> float:
        """Calculate automation potential score for a command."""
        score = 0.0
        
        # Length factor
        words = command.split()
        if len(words) > 3:
            score += 0.2
        
        # Flag factor
        flags = sum(1 for word in words if word.startswith('-'))
        score += flags * 0.1
        
        # Complexity factors
        if '|' in command:
            score += 0.3
        if '>' in command or '<' in command:
            score += 0.2
        if '&&' in command or '||' in command:
            score += 0.4
        
        # File operations
        if any(word in command.lower() for word in ['find', 'grep', 'sed', 'awk']):
            score += 0.3
        
        return min(score, 1.0)
    
    def _generate_skill_progression(self, commands_data: List[Dict[str, Any]], output_dir: str) -> str:
        """Generate skill progression analysis."""
        if not commands_data:
            return ""
        
        # Sort commands by timestamp
        sorted_commands = sorted(commands_data, key=lambda x: x.get('timestamp', 0))
        
        # Calculate skill progression over time
        skill_scores = []
        time_points = []
        
        window_size = max(1, len(sorted_commands) // 20)  # 20 data points
        
        for i in range(0, len(sorted_commands), window_size):
            window = sorted_commands[i:i+window_size]
            if not window:
                continue
            
            # Calculate average complexity for this window
            complexities = []
            for cmd in window:
                command = cmd.get('command', '')
                complexity = self._calculate_automation_score(command)
                complexities.append(complexity)
            
            avg_complexity = np.mean(complexities)
            skill_scores.append(avg_complexity)
            
            # Use timestamp from middle of window
            mid_idx = i + len(window) // 2
            if mid_idx < len(sorted_commands):
                timestamp = sorted_commands[mid_idx].get('timestamp', 0)
                time_points.append(datetime.fromtimestamp(timestamp))
        
        if len(skill_scores) < 2:
            return ""
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 1. Skill progression over time
        ax1.plot(range(len(skill_scores)), skill_scores, 
                color=self.colors['success'], linewidth=2, marker='o')
        ax1.set_xlabel('Time Window')
        ax1.set_ylabel('Average Command Complexity')
        ax1.set_title('Skill Progression Over Time')
        ax1.grid(True, alpha=0.3)
        
        # Add trend line
        if len(skill_scores) > 1:
            z = np.polyfit(range(len(skill_scores)), skill_scores, 1)
            p = np.poly1d(z)
            ax1.plot(range(len(skill_scores)), p(range(len(skill_scores))), 
                    "r--", alpha=0.8, label=f'Trend: {"+" if z[0] > 0 else ""}{z[0]:.3f}x')
            ax1.legend()
        
        # 2. Command diversity over time
        diversity_scores = []
        for i in range(0, len(sorted_commands), window_size):
            window = sorted_commands[i:i+window_size]
            if not window:
                continue
            
            unique_commands = len(set(cmd.get('command', '') for cmd in window))
            total_commands = len(window)
            diversity = unique_commands / total_commands if total_commands > 0 else 0
            diversity_scores.append(diversity)
        
        if diversity_scores:
            ax2.plot(range(len(diversity_scores)), diversity_scores, 
                    color=self.colors['info'], linewidth=2, marker='s')
            ax2.set_xlabel('Time Window')
            ax2.set_ylabel('Command Diversity')
            ax2.set_title('Command Diversity Over Time')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the visualization
        output_path = Path(output_dir) / "skill_progression.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def _generate_comprehensive_report(self, commands_data: List[Dict[str, Any]], 
                                     insights_data: Dict[str, Any], 
                                     viz_paths: Dict[str, str], output_dir: str) -> str:
        """Generate a comprehensive HTML report."""
        
        # Calculate additional statistics
        stats = self._calculate_detailed_statistics(commands_data, insights_data)
        
        # Create HTML content
        html_content = self._get_report_template().render(
            commands_data=commands_data,
            insights_data=insights_data,
            viz_paths=viz_paths,
            stats=stats,
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Save HTML file
        output_path = Path(output_dir) / "comprehensive_report.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _calculate_detailed_statistics(self, commands_data: List[Dict[str, Any]], 
                                     insights_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed statistics for the report."""
        if not commands_data:
            return {}
        
        total_commands = len(commands_data)
        unique_commands = len(set(cmd['command'] for cmd in commands_data))
        
        # Command complexity analysis
        complexities = []
        for cmd in commands_data:
            command = cmd.get('command', '')
            complexity = self._calculate_automation_score(command)
            complexities.append(complexity)
        
        # Time analysis
        timestamps = [cmd.get('timestamp', 0) for cmd in commands_data if 'timestamp' in cmd]
        if timestamps:
            dates = [datetime.fromtimestamp(ts) for ts in timestamps]
            time_span = max(dates) - min(dates)
            avg_commands_per_day = total_commands / max(1, time_span.days)
        else:
            time_span = None
            avg_commands_per_day = 0
        
        # Tool usage analysis
        tool_usage = insights_data.get('data_summary', {}).get('top_tools', [])
        
        return {
            'total_commands': total_commands,
            'unique_commands': unique_commands,
            'command_diversity': unique_commands / total_commands if total_commands > 0 else 0,
            'avg_complexity': np.mean(complexities) if complexities else 0,
            'max_complexity': max(complexities) if complexities else 0,
            'time_span': time_span,
            'avg_commands_per_day': avg_commands_per_day,
            'top_tools': tool_usage,
            'automation_opportunities': len([c for c in complexities if c > 0.5]),
            'skill_level': insights_data.get('skill_level', 'Unknown'),
            'workflow_type': insights_data.get('workflow_type', 'Unknown')
        }
    
    def _get_report_template(self) -> Template:
        """Get the HTML report template."""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CmdChronicle - Comprehensive Analysis Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .section {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .viz-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }
        .viz-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .viz-card img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .insights {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .insights h3 {
            margin-top: 0;
        }
        .insights ul {
            list-style: none;
            padding: 0;
        }
        .insights li {
            margin: 10px 0;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 50px;
            padding: 20px;
            border-top: 1px solid #ddd;
        }
        @media (max-width: 768px) {
            .viz-container {
                grid-template-columns: 1fr;
            }
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 CmdChronicle Analysis Report</h1>
            <p>Comprehensive analysis of your command line workflow</p>
            <p>Generated on {{ generated_at }}</p>
        </div>
        
        <div class="section">
            <h2>📈 Executive Summary</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ stats.total_commands }}</div>
                    <div class="stat-label">Total Commands</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.unique_commands }}</div>
                    <div class="stat-label">Unique Commands</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ "%.1f"|format(stats.command_diversity * 100) }}%</div>
                    <div class="stat-label">Command Diversity</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ stats.automation_opportunities }}</div>
                    <div class="stat-label">Automation Opportunities</div>
                </div>
            </div>
            
            <div class="insights">
                <h3>🎯 Key Insights</h3>
                <ul>
                    <li><strong>Workflow Type:</strong> {{ stats.workflow_type.replace('_', ' ').title() }}</li>
                    <li><strong>Skill Level:</strong> {{ stats.skill_level.title() }}</li>
                    <li><strong>Average Command Complexity:</strong> {{ "%.2f"|format(stats.avg_complexity) }}</li>
                    <li><strong>Commands per Day:</strong> {{ "%.1f"|format(stats.avg_commands_per_day) }}</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>🕒 Time Analysis</h2>
            <div class="viz-container">
                {% if viz_paths.time_analysis %}
                <div class="viz-card">
                    <h3>Time-based Patterns</h3>
                    <img src="{{ viz_paths.time_analysis.split('/')[-1] }}" alt="Time Analysis">
                </div>
                {% endif %}
                {% if viz_paths.skill_progression %}
                <div class="viz-card">
                    <h3>Skill Progression</h3>
                    <img src="{{ viz_paths.skill_progression.split('/')[-1] }}" alt="Skill Progression">
                </div>
                {% endif %}
            </div>
        </div>
        
        <div class="section">
            <h2>🧠 Command Analysis</h2>
            <div class="viz-container">
                {% if viz_paths.complexity_analysis %}
                <div class="viz-card">
                    <h3>Command Complexity</h3>
                    <img src="{{ viz_paths.complexity_analysis.split('/')[-1] }}" alt="Complexity Analysis">
                </div>
                {% endif %}
                {% if viz_paths.workflow_patterns %}
                <div class="viz-card">
                    <h3>Workflow Patterns</h3>
                    <img src="{{ viz_paths.workflow_patterns.split('/')[-1] }}" alt="Workflow Patterns">
                </div>
                {% endif %}
            </div>
        </div>
        
        <div class="section">
            <h2>🤖 Automation Opportunities</h2>
            <div class="viz-container">
                {% if viz_paths.automation_opportunities %}
                <div class="viz-card">
                    <h3>Automation Potential</h3>
                    <img src="{{ viz_paths.automation_opportunities.split('/')[-1] }}" alt="Automation Opportunities">
                </div>
                {% endif %}
            </div>
            
            <div class="insights">
                <h3>💡 Recommendations</h3>
                <ul>
                    {% for rec in insights_data.get('recommendations', []) %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>🎭 AI-Generated Insights</h2>
            <div class="insights">
                <h3>Workflow Characteristics</h3>
                <ul>
                    {% for char in insights_data.get('workflow_characteristics', []) %}
                    <li>{{ char }}</li>
                    {% endfor %}
                </ul>
            </div>
            
            <div class="insights">
                <h3>Personality Traits</h3>
                <ul>
                    {% for trait in insights_data.get('personality_traits', []) %}
                    <li>{{ trait }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by CmdChronicle - Your Command Line Journey Analyzer</p>
            <p>Model: {{ insights_data.get('model_used', 'Unknown') }}</p>
        </div>
    </div>
</body>
</html>
"""
        return Template(template_str) 