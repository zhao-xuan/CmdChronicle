"""
Command History Collector
Collects command history from various shell sources and active sessions.
"""

import os
import subprocess
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import psutil


class CommandHistoryCollector:
    """Collects command history from shell history files and active processes."""
    
    def __init__(self):
        self.shell_configs = {
            'bash': {
                'history_file': '~/.bash_history',
                'history_command': 'history',
                'process_names': ['bash']
            },
            'zsh': {
                'history_file': '~/.zsh_history',
                'history_command': 'history',
                'process_names': ['zsh']
            },
            'fish': {
                'history_file': '~/.local/share/fish/fish_history',
                'history_command': 'history',
                'process_names': ['fish']
            }
        }
    
    def collect_commands(self, shell: str = 'auto', limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Collect commands from shell history and active sessions.
        
        Args:
            shell: Shell type ('bash', 'zsh', 'fish', 'auto')
            limit: Maximum number of commands to collect
            
        Returns:
            List of command dictionaries with metadata
        """
        commands = []
        
        # Determine shell type
        if shell == 'auto':
            shell = self._detect_shell()
        
        # Collect from history files
        history_commands = self._collect_from_history(shell, limit)
        commands.extend(history_commands)
        
        # Collect from active processes
        active_commands = self._collect_from_active_processes(shell, limit // 2)
        commands.extend(active_commands)
        
        # Remove duplicates and sort by timestamp
        unique_commands = self._deduplicate_commands(commands)
        unique_commands.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        return unique_commands[:limit]
    
    def _detect_shell(self) -> str:
        """Detect the current shell type."""
        shell = os.environ.get('SHELL', '').lower()
        
        if 'zsh' in shell:
            return 'zsh'
        elif 'bash' in shell:
            return 'bash'
        elif 'fish' in shell:
            return 'fish'
        else:
            # Default to bash if we can't detect
            return 'bash'
    
    def _collect_from_history(self, shell: str, limit: int) -> List[Dict[str, Any]]:
        """Collect commands from shell history files."""
        commands = []
        
        if shell not in self.shell_configs:
            return commands
        
        config = self.shell_configs[shell]
        history_file = Path(config['history_file']).expanduser()
        
        if not history_file.exists():
            return commands
        
        try:
            with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Parse history based on shell type
            if shell == 'zsh':
                commands = self._parse_zsh_history(lines, limit)
            elif shell == 'bash':
                commands = self._parse_bash_history(lines, limit)
            elif shell == 'fish':
                commands = self._parse_fish_history(lines, limit)
                
        except Exception as e:
            print(f"Warning: Could not read {shell} history: {e}")
        
        return commands
    
    def _parse_zsh_history(self, lines: List[str], limit: int) -> List[Dict[str, Any]]:
        """Parse zsh history format."""
        commands = []
        
        for line in lines[-limit:]:
            line = line.strip()
            if not line:
                continue
            
            # Zsh history format: : timestamp:0;command
            match = re.match(r': (\d+):\d+;(.+)', line)
            if match:
                timestamp = int(match.group(1))
                command = match.group(2).strip()
                
                if command and not self._is_ignored_command(command):
                    commands.append({
                        'command': command,
                        'timestamp': timestamp,
                        'source': 'zsh_history',
                        'shell': 'zsh'
                    })
        
        return commands
    
    def _parse_bash_history(self, lines: List[str], limit: int) -> List[Dict[str, Any]]:
        """Parse bash history format."""
        commands = []
        current_time = datetime.now()
        
        for i, line in enumerate(lines[-limit:]):
            line = line.strip()
            if not line or self._is_ignored_command(line):
                continue
            
            # Estimate timestamp (bash history doesn't include timestamps by default)
            # Use reverse chronological order
            estimated_timestamp = int((current_time - timedelta(minutes=i)).timestamp())
            
            commands.append({
                'command': line,
                'timestamp': estimated_timestamp,
                'source': 'bash_history',
                'shell': 'bash'
            })
        
        return commands
    
    def _parse_fish_history(self, lines: List[str], limit: int) -> List[Dict[str, Any]]:
        """Parse fish history format."""
        commands = []
        
        for line in lines[-limit:]:
            line = line.strip()
            if not line:
                continue
            
            # Fish history format: - cmd: command
            if line.startswith('- cmd: '):
                command = line[7:].strip()
                if command and not self._is_ignored_command(command):
                    commands.append({
                        'command': command,
                        'timestamp': int(datetime.now().timestamp()),
                        'source': 'fish_history',
                        'shell': 'fish'
                    })
        
        return commands
    
    def _collect_from_active_processes(self, shell: str, limit: int) -> List[Dict[str, Any]]:
        """Collect commands from active shell processes."""
        commands = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    if proc.info['name'] in self.shell_configs[shell]['process_names']:
                        # Get command line arguments
                        cmdline = proc.info['cmdline']
                        if cmdline and len(cmdline) > 1:
                            command = ' '.join(cmdline[1:])  # Skip shell name
                            if command and not self._is_ignored_command(command):
                                commands.append({
                                    'command': command,
                                    'timestamp': int(proc.info['create_time']),
                                    'source': 'active_process',
                                    'shell': shell,
                                    'pid': proc.info['pid']
                                })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Warning: Could not collect from active processes: {e}")
        
        return commands[:limit]
    
    def _is_ignored_command(self, command: str) -> bool:
        """Check if command should be ignored."""
        ignored_patterns = [
            r'^\s*$',  # Empty or whitespace only
            r'^history\s*$',  # history command
            r'^clear\s*$',  # clear command
            r'^exit\s*$',  # exit command
            r'^logout\s*$',  # logout command
            r'^cd\s*$',  # cd without arguments
            r'^ls\s*$',  # ls without arguments
            r'^pwd\s*$',  # pwd command
            r'^echo\s*$',  # echo without arguments
        ]
        
        for pattern in ignored_patterns:
            if re.match(pattern, command):
                return True
        
        return False
    
    def _deduplicate_commands(self, commands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate commands based on command text and timestamp."""
        seen = set()
        unique_commands = []
        
        for cmd in commands:
            # Create a key based on command and timestamp (within 1 minute)
            timestamp_key = cmd['timestamp'] // 60  # Round to minute
            key = (cmd['command'], timestamp_key)
            
            if key not in seen:
                seen.add(key)
                unique_commands.append(cmd)
        
        return unique_commands
    
    def get_command_stats(self, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics about collected commands."""
        if not commands:
            return {}
        
        total_commands = len(commands)
        unique_commands = len(set(cmd['command'] for cmd in commands))
        
        # Count by shell
        shell_counts = {}
        for cmd in commands:
            shell = cmd.get('shell', 'unknown')
            shell_counts[shell] = shell_counts.get(shell, 0) + 1
        
        # Most common commands
        command_counts = {}
        for cmd in commands:
            command = cmd['command']
            command_counts[command] = command_counts.get(command, 0) + 1
        
        most_common = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Time range
        timestamps = [cmd['timestamp'] for cmd in commands if 'timestamp' in cmd]
        if timestamps:
            time_range = {
                'earliest': min(timestamps),
                'latest': max(timestamps),
                'span_hours': (max(timestamps) - min(timestamps)) / 3600
            }
        else:
            time_range = {}
        
        return {
            'total_commands': total_commands,
            'unique_commands': unique_commands,
            'shell_distribution': shell_counts,
            'most_common_commands': most_common,
            'time_range': time_range
        } 