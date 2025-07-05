"""
Tests for the Command History Collector
"""

import unittest
from unittest.mock import patch, MagicMock
from src.collectors.history_collector import CommandHistoryCollector


class TestCommandHistoryCollector(unittest.TestCase):
    """Test cases for CommandHistoryCollector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.collector = CommandHistoryCollector()
    
    def test_detect_shell(self):
        """Test shell detection."""
        with patch.dict('os.environ', {'SHELL': '/bin/zsh'}):
            shell = self.collector._detect_shell()
            self.assertEqual(shell, 'zsh')
        
        with patch.dict('os.environ', {'SHELL': '/bin/bash'}):
            shell = self.collector._detect_shell()
            self.assertEqual(shell, 'bash')
        
        with patch.dict('os.environ', {'SHELL': '/usr/bin/fish'}):
            shell = self.collector._detect_shell()
            self.assertEqual(shell, 'fish')
    
    def test_is_ignored_command(self):
        """Test command filtering."""
        self.assertTrue(self.collector._is_ignored_command('history'))
        self.assertTrue(self.collector._is_ignored_command('clear'))
        self.assertTrue(self.collector._is_ignored_command('cd'))
        self.assertFalse(self.collector._is_ignored_command('git status'))
        self.assertFalse(self.collector._is_ignored_command('ls -la'))
    
    def test_deduplicate_commands(self):
        """Test command deduplication."""
        commands = [
            {'command': 'git status', 'timestamp': 1000},
            {'command': 'git status', 'timestamp': 1001},  # Within 1 minute
            {'command': 'git status', 'timestamp': 2000},  # Different time
            {'command': 'ls -la', 'timestamp': 1000}
        ]
        
        unique = self.collector._deduplicate_commands(commands)
        self.assertEqual(len(unique), 3)  # Should remove one duplicate
    
    def test_get_command_stats(self):
        """Test command statistics generation."""
        commands = [
            {'command': 'git status', 'shell': 'zsh'},
            {'command': 'git add .', 'shell': 'zsh'},
            {'command': 'ls -la', 'shell': 'bash'}
        ]
        
        stats = self.collector.get_command_stats(commands)
        self.assertEqual(stats['total_commands'], 3)
        self.assertEqual(stats['unique_commands'], 3)
        self.assertEqual(stats['shell_distribution']['zsh'], 2)
        self.assertEqual(stats['shell_distribution']['bash'], 1)


if __name__ == '__main__':
    unittest.main() 