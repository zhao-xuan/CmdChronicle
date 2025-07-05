"""
Data Manager
Handles data persistence, loading, and management for the CmdChronicle tool.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class DataManager:
    """Manages data persistence and loading operations."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_commands(self, commands: List[Dict[str, Any]], filepath: str) -> str:
        """
        Save commands data to a JSON file.
        
        Args:
            commands: List of command dictionaries
            filepath: Path to save the file
            
        Returns:
            Path to the saved file
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_commands': len(commands),
                'unique_commands': len(set(cmd.get('command', '') for cmd in commands)),
                'version': '1.0.0'
            },
            'commands': commands
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_commands(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load commands data from a JSON file.
        
        Args:
            filepath: Path to the file to load
            
        Returns:
            List of command dictionaries
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Commands file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both old and new format
        if 'commands' in data:
            return data['commands']
        else:
            # Assume old format where data is directly a list
            return data
    
    def save_patterns(self, patterns: Dict[str, Any], filepath: str) -> str:
        """
        Save pattern analysis results to a JSON file.
        
        Args:
            patterns: Pattern analysis results
            filepath: Path to save the file
            
        Returns:
            Path to the saved file
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'patterns': patterns
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_patterns(self, filepath: str) -> Dict[str, Any]:
        """
        Load pattern analysis results from a JSON file.
        
        Args:
            filepath: Path to the file to load
            
        Returns:
            Pattern analysis results
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Patterns file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both old and new format
        if 'patterns' in data:
            return data['patterns']
        else:
            # Assume old format where data is directly the patterns
            return data
    
    def save_insights(self, insights: Dict[str, Any], filepath: str) -> str:
        """
        Save AI insights to a JSON file.
        
        Args:
            insights: AI-generated insights
            filepath: Path to save the file
            
        Returns:
            Path to the saved file
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'insights': insights
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_insights(self, filepath: str) -> Dict[str, Any]:
        """
        Load AI insights from a JSON file.
        
        Args:
            filepath: Path to the file to load
            
        Returns:
            AI-generated insights
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Insights file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both old and new format
        if 'insights' in data:
            return data['insights']
        else:
            # Assume old format where data is directly the insights
            return data
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all available data files.
        
        Returns:
            Dictionary containing data summary
        """
        summary = {
            'data_directory': str(self.data_dir),
            'files': [],
            'total_files': 0,
            'last_updated': None
        }
        
        if not self.data_dir.exists():
            return summary
        
        latest_time = None
        
        for filepath in self.data_dir.glob("*.json"):
            try:
                stat = filepath.stat()
                file_info = {
                    'name': filepath.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'type': self._get_file_type(filepath.name)
                }
                summary['files'].append(file_info)
                
                if latest_time is None or stat.st_mtime > latest_time:
                    latest_time = stat.st_mtime
                    
            except Exception as e:
                print(f"Warning: Could not read file {filepath}: {e}")
        
        summary['total_files'] = len(summary['files'])
        if latest_time:
            summary['last_updated'] = datetime.fromtimestamp(latest_time).isoformat()
        
        return summary
    
    def _get_file_type(self, filename: str) -> str:
        """Determine the type of data file based on filename."""
        filename_lower = filename.lower()
        
        if 'command' in filename_lower:
            return 'commands'
        elif 'pattern' in filename_lower:
            return 'patterns'
        elif 'insight' in filename_lower:
            return 'insights'
        else:
            return 'unknown'
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """
        Clean up old data files.
        
        Args:
            days: Number of days to keep files
            
        Returns:
            Number of files deleted
        """
        if not self.data_dir.exists():
            return 0
        
        cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
        deleted_count = 0
        
        for filepath in self.data_dir.glob("*.json"):
            try:
                if filepath.stat().st_mtime < cutoff_time:
                    filepath.unlink()
                    deleted_count += 1
            except Exception as e:
                print(f"Warning: Could not delete file {filepath}: {e}")
        
        return deleted_count
    
    def export_data(self, output_dir: str, format: str = 'json') -> str:
        """
        Export all data to a specified format.
        
        Args:
            output_dir: Directory to export data to
            format: Export format ('json', 'csv')
            
        Returns:
            Path to the exported data
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == 'json':
            return self._export_json(output_dir)
        elif format.lower() == 'csv':
            return self._export_csv(output_dir)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, output_dir: Path) -> str:
        """Export data as JSON."""
        export_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'data_files': {}
        }
        
        for filepath in self.data_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                export_data['data_files'][filepath.name] = data
            except Exception as e:
                print(f"Warning: Could not read file {filepath}: {e}")
        
        output_path = output_dir / "cmdchronicle_export.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def _export_csv(self, output_dir: Path) -> str:
        """Export data as CSV."""
        import csv
        
        # Export commands to CSV
        commands_file = self.data_dir / "commands.json"
        if commands_file.exists():
            try:
                commands = self.load_commands(str(commands_file))
                
                output_path = output_dir / "commands.csv"
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    if commands:
                        fieldnames = commands[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(commands)
                
                return str(output_path)
            except Exception as e:
                print(f"Warning: Could not export commands to CSV: {e}")
        
        return ""
    
    def validate_data(self, filepath: str) -> Dict[str, Any]:
        """
        Validate data file integrity.
        
        Args:
            filepath: Path to the file to validate
            
        Returns:
            Validation results
        """
        filepath = Path(filepath)
        
        validation = {
            'file_exists': filepath.exists(),
            'is_readable': False,
            'is_valid_json': False,
            'has_required_fields': False,
            'errors': []
        }
        
        if not validation['file_exists']:
            validation['errors'].append("File does not exist")
            return validation
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            validation['is_readable'] = True
            validation['is_valid_json'] = True
        except json.JSONDecodeError as e:
            validation['errors'].append(f"Invalid JSON: {e}")
            return validation
        except Exception as e:
            validation['errors'].append(f"Read error: {e}")
            return validation
        
        # Check for required fields based on file type
        file_type = self._get_file_type(filepath.name)
        
        if file_type == 'commands':
            if isinstance(data, dict) and 'commands' in data:
                validation['has_required_fields'] = True
            elif isinstance(data, list):
                validation['has_required_fields'] = True
            else:
                validation['errors'].append("Missing 'commands' field")
        
        elif file_type == 'patterns':
            if isinstance(data, dict) and 'patterns' in data:
                validation['has_required_fields'] = True
            elif isinstance(data, dict):
                validation['has_required_fields'] = True
            else:
                validation['errors'].append("Missing 'patterns' field")
        
        elif file_type == 'insights':
            if isinstance(data, dict) and 'insights' in data:
                validation['has_required_fields'] = True
            elif isinstance(data, dict):
                validation['has_required_fields'] = True
            else:
                validation['errors'].append("Missing 'insights' field")
        
        return validation 