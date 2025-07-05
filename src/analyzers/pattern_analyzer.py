"""
Pattern Analyzer
Analyzes command patterns to identify frequent commands and automation opportunities.
"""

import re
import json
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta


class PatternAnalyzer:
    """Analyzes command patterns and identifies automation opportunities."""
    
    def __init__(self):
        self.common_tools = {
            'git': ['git', 'commit', 'push', 'pull', 'branch', 'checkout', 'merge'],
            'docker': ['docker', 'run', 'build', 'ps', 'exec', 'logs'],
            'kubernetes': ['kubectl', 'k8s', 'pod', 'service', 'deployment'],
            'python': ['python', 'pip', 'virtualenv', 'conda', 'py'],
            'node': ['node', 'npm', 'yarn', 'npx'],
            'system': ['sudo', 'apt', 'brew', 'yum', 'systemctl'],
            'development': ['vim', 'code', 'subl', 'nano', 'emacs'],
            'monitoring': ['top', 'htop', 'ps', 'df', 'du', 'netstat'],
            'network': ['ssh', 'scp', 'curl', 'wget', 'ping', 'telnet'],
            'database': ['mysql', 'psql', 'sqlite', 'mongo', 'redis-cli']
        }
        
        self.automation_patterns = [
            r'cd\s+\S+',  # Directory navigation
            r'ls\s+\S+',  # Directory listing with path
            r'find\s+\S+',  # File finding
            r'grep\s+\S+',  # Text searching
            r'cat\s+\S+',  # File viewing
            r'cp\s+\S+',  # File copying
            r'mv\s+\S+',  # File moving
            r'rm\s+\S+',  # File removal
            r'chmod\s+\S+',  # Permission changes
            r'chown\s+\S+',  # Ownership changes
        ]
    
    def analyze_patterns(self, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze command patterns and identify automation opportunities.
        
        Args:
            commands: List of command dictionaries
            
        Returns:
            Dictionary containing analysis results
        """
        if not commands:
            return self._empty_analysis()
        
        # Extract command texts
        command_texts = [cmd['command'] for cmd in commands]
        
        # Basic frequency analysis
        frequent_commands = self._analyze_frequency(command_texts)
        
        # Command type analysis
        command_types = self._analyze_command_types(command_texts)
        
        # Pattern analysis
        patterns = self._analyze_patterns(command_texts)
        
        # Automation candidates
        automation_candidates = self._identify_automation_candidates(command_texts)
        
        # Workflow analysis
        workflows = self._analyze_workflows(commands)
        
        # Tool usage analysis
        tool_usage = self._analyze_tool_usage(command_texts)
        
        # Time-based patterns
        time_patterns = self._analyze_time_patterns(commands)
        
        return {
            'frequent_commands': frequent_commands,
            'command_types': command_types,
            'patterns': patterns,
            'automation_candidates': automation_candidates,
            'workflows': workflows,
            'tool_usage': tool_usage,
            'time_patterns': time_patterns,
            'summary': self._generate_summary(command_texts, frequent_commands, tool_usage)
        }
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure."""
        return {
            'frequent_commands': [],
            'command_types': {},
            'patterns': {},
            'automation_candidates': [],
            'workflows': [],
            'tool_usage': {},
            'time_patterns': {},
            'summary': {}
        }
    
    def _analyze_frequency(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Analyze command frequency."""
        counter = Counter(commands)
        total_commands = len(commands)
        
        frequent_commands = []
        for command, count in counter.most_common(20):
            percentage = (count / total_commands) * 100
            frequent_commands.append({
                'command': command,
                'count': count,
                'percentage': round(percentage, 2),
                'automation_potential': self._calculate_automation_potential(command)
            })
        
        return frequent_commands
    
    def _analyze_command_types(self, commands: List[str]) -> Dict[str, Any]:
        """Analyze types of commands being used."""
        type_counts = defaultdict(int)
        
        for command in commands:
            cmd_parts = command.split()
            if not cmd_parts:
                continue
            
            base_command = cmd_parts[0]
            
            # Categorize by tool/technology
            categorized = False
            for tool, keywords in self.common_tools.items():
                if any(keyword in base_command.lower() for keyword in keywords):
                    type_counts[tool] += 1
                    categorized = True
                    break
            
            if not categorized:
                type_counts['other'] += 1
        
        return dict(type_counts)
    
    def _analyze_patterns(self, commands: List[str]) -> Dict[str, Any]:
        """Analyze command patterns."""
        patterns = {
            'repeated_sequences': self._find_repeated_sequences(commands),
            'common_prefixes': self._find_common_prefixes(commands),
            'common_suffixes': self._find_common_suffixes(commands),
            'parameter_patterns': self._find_parameter_patterns(commands)
        }
        
        return patterns
    
    def _find_repeated_sequences(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Find repeated command sequences."""
        sequences = defaultdict(int)
        
        # Look for sequences of 2-4 commands
        for seq_len in range(2, 5):
            for i in range(len(commands) - seq_len + 1):
                sequence = ' | '.join(commands[i:i+seq_len])
                sequences[sequence] += 1
        
        # Return sequences that appear more than once
        repeated = [
            {'sequence': seq, 'count': count}
            for seq, count in sequences.items()
            if count > 1
        ]
        
        return sorted(repeated, key=lambda x: x['count'], reverse=True)[:10]
    
    def _find_common_prefixes(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Find common command prefixes."""
        prefixes = defaultdict(int)
        
        for command in commands:
            parts = command.split()
            for i in range(1, min(4, len(parts) + 1)):
                prefix = ' '.join(parts[:i])
                prefixes[prefix] += 1
        
        common_prefixes = [
            {'prefix': prefix, 'count': count}
            for prefix, count in prefixes.items()
            if count > 2
        ]
        
        return sorted(common_prefixes, key=lambda x: x['count'], reverse=True)[:10]
    
    def _find_common_suffixes(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Find common command suffixes/arguments."""
        suffixes = defaultdict(int)
        
        for command in commands:
            parts = command.split()
            if len(parts) > 1:
                suffix = ' '.join(parts[1:])
                suffixes[suffix] += 1
        
        common_suffixes = [
            {'suffix': suffix, 'count': count}
            for suffix, count in suffixes.items()
            if count > 2
        ]
        
        return sorted(common_suffixes, key=lambda x: x['count'], reverse=True)[:10]
    
    def _find_parameter_patterns(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Find common parameter patterns."""
        patterns = defaultdict(int)
        
        for command in commands:
            # Extract flags and parameters
            flags = re.findall(r'--?\w+', command)
            if flags:
                flag_pattern = ' '.join(sorted(flags))
                patterns[flag_pattern] += 1
        
        common_patterns = [
            {'pattern': pattern, 'count': count}
            for pattern, count in patterns.items()
            if count > 1
        ]
        
        return sorted(common_patterns, key=lambda x: x['count'], reverse=True)[:10]
    
    def _identify_automation_candidates(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Identify commands that could be automated."""
        candidates = []
        
        for command in commands:
            automation_score = self._calculate_automation_potential(command)
            
            if automation_score > 0.3:  # Threshold for automation potential
                candidates.append({
                    'command': command,
                    'automation_score': automation_score,
                    'automation_type': self._suggest_automation_type(command),
                    'suggested_alias': self._suggest_alias(command),
                    'suggested_script': self._suggest_script(command)
                })
        
        # Sort by automation score
        candidates.sort(key=lambda x: x['automation_score'], reverse=True)
        return candidates[:20]
    
    def _calculate_automation_potential(self, command: str) -> float:
        """Calculate automation potential score (0-1)."""
        score = 0.0
        
        # Check if command matches automation patterns
        for pattern in self.automation_patterns:
            if re.search(pattern, command):
                score += 0.3
        
        # Check command length (longer commands are better candidates)
        if len(command.split()) > 3:
            score += 0.2
        
        # Check for repetitive elements
        if any(word in command.lower() for word in ['find', 'grep', 'sed', 'awk', 'xargs']):
            score += 0.2
        
        # Check for file operations
        if any(word in command.lower() for word in ['cp', 'mv', 'rm', 'mkdir', 'touch']):
            score += 0.1
        
        return min(score, 1.0)
    
    def _suggest_automation_type(self, command: str) -> str:
        """Suggest automation type for a command."""
        if 'cd' in command:
            return 'alias'
        elif 'find' in command or 'grep' in command:
            return 'function'
        elif len(command.split()) > 5:
            return 'script'
        else:
            return 'alias'
    
    def _suggest_alias(self, command: str) -> str:
        """Suggest an alias for a command."""
        parts = command.split()
        if not parts:
            return ''
        
        base_cmd = parts[0]
        
        # Generate alias based on command type
        if base_cmd == 'cd':
            path = parts[1] if len(parts) > 1 else ''
            return f"alias cd{path.replace('/', '_')}='{command}'"
        elif base_cmd == 'ls':
            return f"alias ll='{command}'"
        elif base_cmd == 'find':
            return f"alias find{parts[1] if len(parts) > 1 else ''}='{command}'"
        else:
            return f"alias {base_cmd}_custom='{command}'"
    
    def _suggest_script(self, command: str) -> str:
        """Suggest a script for a complex command."""
        parts = command.split()
        if not parts:
            return ''
        
        base_cmd = parts[0]
        script_name = f"{base_cmd}_script.sh"
        
        script_content = f"""#!/bin/bash
# Automated script for: {command}

{command}

echo "Command completed successfully!"
"""
        
        return {
            'name': script_name,
            'content': script_content
        }
    
    def _analyze_workflows(self, commands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze command workflows and sequences."""
        workflows = []
        
        # Group commands by time proximity (within 5 minutes)
        time_groups = self._group_commands_by_time(commands, 300)
        
        for group in time_groups:
            if len(group) >= 2:
                workflow = {
                    'commands': [cmd['command'] for cmd in group],
                    'duration': group[-1]['timestamp'] - group[0]['timestamp'],
                    'command_count': len(group),
                    'workflow_type': self._classify_workflow(group)
                }
                workflows.append(workflow)
        
        return workflows[:10]  # Return top 10 workflows
    
    def _group_commands_by_time(self, commands: List[Dict[str, Any]], time_window: int) -> List[List[Dict[str, Any]]]:
        """Group commands by time proximity."""
        if not commands:
            return []
        
        # Sort by timestamp
        sorted_commands = sorted(commands, key=lambda x: x.get('timestamp', 0))
        
        groups = []
        current_group = [sorted_commands[0]]
        
        for cmd in sorted_commands[1:]:
            time_diff = cmd.get('timestamp', 0) - current_group[-1].get('timestamp', 0)
            
            if time_diff <= time_window:
                current_group.append(cmd)
            else:
                if len(current_group) > 1:
                    groups.append(current_group)
                current_group = [cmd]
        
        if len(current_group) > 1:
            groups.append(current_group)
        
        return groups
    
    def _classify_workflow(self, commands: List[Dict[str, Any]]) -> str:
        """Classify the type of workflow."""
        command_texts = [cmd['command'] for cmd in commands]
        text = ' '.join(command_texts).lower()
        
        if any(word in text for word in ['git', 'commit', 'push']):
            return 'git_workflow'
        elif any(word in text for word in ['docker', 'build', 'run']):
            return 'docker_workflow'
        elif any(word in text for word in ['python', 'pip', 'install']):
            return 'python_workflow'
        elif any(word in text for word in ['npm', 'yarn', 'node']):
            return 'node_workflow'
        elif any(word in text for word in ['cd', 'ls', 'find']):
            return 'file_exploration'
        else:
            return 'general_workflow'
    
    def _analyze_tool_usage(self, commands: List[str]) -> Dict[str, Any]:
        """Analyze usage of different tools and technologies."""
        tool_stats = {}
        
        for tool, keywords in self.common_tools.items():
            count = sum(1 for cmd in commands 
                       if any(keyword in cmd.lower() for keyword in keywords))
            if count > 0:
                tool_stats[tool] = {
                    'count': count,
                    'percentage': (count / len(commands)) * 100,
                    'primary_commands': self._get_primary_commands(commands, keywords)
                }
        
        return tool_stats
    
    def _get_primary_commands(self, commands: List[str], keywords: List[str]) -> List[str]:
        """Get primary commands for a tool."""
        primary_commands = []
        
        for cmd in commands:
            if any(keyword in cmd.lower() for keyword in keywords):
                base_cmd = cmd.split()[0] if cmd.split() else ''
                if base_cmd not in primary_commands:
                    primary_commands.append(base_cmd)
        
        return primary_commands[:5]  # Return top 5
    
    def _analyze_time_patterns(self, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze time-based patterns in command usage."""
        if not commands:
            return {}
        
        # Group by hour of day
        hourly_counts = defaultdict(int)
        for cmd in commands:
            if 'timestamp' in cmd:
                dt = datetime.fromtimestamp(cmd['timestamp'])
                hourly_counts[dt.hour] += 1
        
        # Group by day of week
        daily_counts = defaultdict(int)
        for cmd in commands:
            if 'timestamp' in cmd:
                dt = datetime.fromtimestamp(cmd['timestamp'])
                daily_counts[dt.strftime('%A')] += 1
        
        return {
            'hourly_distribution': dict(hourly_counts),
            'daily_distribution': dict(daily_counts)
        }
    
    def _generate_summary(self, commands: List[str], frequent_commands: List[Dict], tool_usage: Dict) -> Dict[str, Any]:
        """Generate a summary of the analysis."""
        total_commands = len(commands)
        unique_commands = len(set(commands))
        
        # Most used tool
        most_used_tool = max(tool_usage.items(), key=lambda x: x[1]['count']) if tool_usage else None
        
        # Most frequent command
        most_frequent = frequent_commands[0] if frequent_commands else None
        
        return {
            'total_commands': total_commands,
            'unique_commands': unique_commands,
            'command_diversity': unique_commands / total_commands if total_commands > 0 else 0,
            'most_used_tool': most_used_tool[0] if most_used_tool else 'None',
            'most_frequent_command': most_frequent['command'] if most_frequent else 'None',
            'automation_opportunities': len([cmd for cmd in frequent_commands if cmd['automation_potential'] > 0.3])
        } 