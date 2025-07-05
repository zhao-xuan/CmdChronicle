"""
Configuration Manager
Handles configuration settings and preferences for the CmdChronicle tool.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigManager:
    """Manages configuration settings and preferences."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.default_config = self._get_default_config()
        self.config = self._load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration settings."""
        return {
            'version': '1.0.0',
            'ollama': {
                'base_url': 'http://localhost:11434',
                'default_model': 'llama3.2',
                'timeout': 30,
                'max_tokens': 2000,
                'temperature': 0.7,
                'top_p': 0.9
            },
            'collection': {
                'default_shell': 'auto',
                'max_commands': 1000,
                'include_active_processes': True,
                'ignore_patterns': [
                    '^history$',
                    '^clear$',
                    '^exit$',
                    '^logout$',
                    '^cd$',
                    '^ls$',
                    '^pwd$',
                    '^echo$'
                ]
            },
            'analysis': {
                'automation_threshold': 0.3,
                'complexity_weight': 0.2,
                'frequency_weight': 0.3,
                'pattern_weight': 0.5
            },
            'visualization': {
                'wordcloud': {
                    'width': 1200,
                    'height': 800,
                    'max_words': 100,
                    'colormap': 'viridis'
                },
                'charts': {
                    'dpi': 300,
                    'style': 'seaborn-v0_8',
                    'figure_size': [12, 8]
                }
            },
            'output': {
                'default_output_dir': 'reports',
                'save_intermediate': True,
                'export_formats': ['html', 'png', 'json']
            },
            'ui': {
                'theme': 'default',
                'show_progress': True,
                'verbose_output': False,
                'color_output': True
            },
            'data': {
                'auto_cleanup_days': 30,
                'max_file_size_mb': 100,
                'compression_enabled': False
            }
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with default config to ensure all keys exist
                merged_config = self._merge_configs(self.default_config, config)
                return merged_config
                
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                return self.default_config.copy()
        else:
            # Create default config file
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user config with default config."""
        merged = default.copy()
        
        def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> None:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dicts(base[key], value)
                else:
                    base[key] = value
        
        merge_dicts(merged, user)
        return merged
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save (uses current config if None)
            
        Returns:
            Path to the saved config file
        """
        if config is None:
            config = self.config
        
        # Add metadata
        config_with_metadata = {
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'version': config.get('version', '1.0.0')
            },
            'config': config
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_with_metadata, f, indent=2, ensure_ascii=False)
        
        return str(self.config_file)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'ollama.base_url')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'ollama.base_url')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        for key, value in updates.items():
            self.set(key, value)
    
    def reset_to_default(self) -> None:
        """Reset configuration to default values."""
        self.config = self.default_config.copy()
        self.save_config()
    
    def validate_config(self) -> Dict[str, Any]:
        """
        Validate the current configuration.
        
        Returns:
            Validation results
        """
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = [
            'ollama.base_url',
            'ollama.default_model',
            'collection.max_commands',
            'analysis.automation_threshold'
        ]
        
        for field in required_fields:
            if self.get(field) is None:
                validation['errors'].append(f"Missing required field: {field}")
                validation['is_valid'] = False
        
        # Validate Ollama settings
        ollama_url = self.get('ollama.base_url')
        if ollama_url and not ollama_url.startswith(('http://', 'https://')):
            validation['errors'].append("Invalid Ollama URL format")
            validation['is_valid'] = False
        
        # Validate numeric ranges
        max_commands = self.get('collection.max_commands')
        if max_commands and (max_commands < 1 or max_commands > 10000):
            validation['warnings'].append("Max commands should be between 1 and 10000")
        
        automation_threshold = self.get('analysis.automation_threshold')
        if automation_threshold and (automation_threshold < 0 or automation_threshold > 1):
            validation['errors'].append("Automation threshold should be between 0 and 1")
            validation['is_valid'] = False
        
        return validation
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get Ollama-specific configuration."""
        return {
            'base_url': self.get('ollama.base_url'),
            'model': self.get('ollama.default_model'),
            'timeout': self.get('ollama.timeout'),
            'max_tokens': self.get('ollama.max_tokens'),
            'temperature': self.get('ollama.temperature'),
            'top_p': self.get('ollama.top_p')
        }
    
    def get_collection_config(self) -> Dict[str, Any]:
        """Get collection-specific configuration."""
        return {
            'shell': self.get('collection.default_shell'),
            'max_commands': self.get('collection.max_commands'),
            'include_active_processes': self.get('collection.include_active_processes'),
            'ignore_patterns': self.get('collection.ignore_patterns')
        }
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis-specific configuration."""
        return {
            'automation_threshold': self.get('analysis.automation_threshold'),
            'complexity_weight': self.get('analysis.complexity_weight'),
            'frequency_weight': self.get('analysis.frequency_weight'),
            'pattern_weight': self.get('analysis.pattern_weight')
        }
    
    def get_visualization_config(self) -> Dict[str, Any]:
        """Get visualization-specific configuration."""
        return {
            'wordcloud': self.get('visualization.wordcloud'),
            'charts': self.get('visualization.charts')
        }
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output-specific configuration."""
        return {
            'default_output_dir': self.get('output.default_output_dir'),
            'save_intermediate': self.get('output.save_intermediate'),
            'export_formats': self.get('output.export_formats')
        }
    
    def create_profile(self, name: str, config_overrides: Dict[str, Any]) -> str:
        """
        Create a named configuration profile.
        
        Args:
            name: Profile name
            config_overrides: Configuration overrides for this profile
            
        Returns:
            Path to the profile file
        """
        profile_file = self.config_dir / f"profile_{name}.json"
        
        # Create profile config by merging with current config
        profile_config = self.config.copy()
        self._merge_configs(profile_config, config_overrides)
        
        profile_data = {
            'metadata': {
                'name': name,
                'created_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'config': profile_config
        }
        
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
        
        return str(profile_file)
    
    def load_profile(self, name: str) -> bool:
        """
        Load a named configuration profile.
        
        Args:
            name: Profile name
            
        Returns:
            True if profile loaded successfully
        """
        profile_file = self.config_dir / f"profile_{name}.json"
        
        if not profile_file.exists():
            return False
        
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            self.config = profile_data['config']
            return True
            
        except Exception as e:
            print(f"Warning: Could not load profile {name}: {e}")
            return False
    
    def list_profiles(self) -> Dict[str, Any]:
        """
        List available configuration profiles.
        
        Returns:
            Dictionary of profile information
        """
        profiles = {}
        
        for profile_file in self.config_dir.glob("profile_*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                
                name = profile_data['metadata']['name']
                profiles[name] = {
                    'file': str(profile_file),
                    'created_at': profile_data['metadata'].get('created_at'),
                    'version': profile_data['metadata'].get('version')
                }
                
            except Exception as e:
                print(f"Warning: Could not read profile {profile_file}: {e}")
        
        return profiles
    
    def export_config(self, output_path: str) -> str:
        """
        Export current configuration to a file.
        
        Args:
            output_path: Path to export the configuration
            
        Returns:
            Path to the exported file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        export_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'config': self.config
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def import_config(self, import_path: str) -> bool:
        """
        Import configuration from a file.
        
        Args:
            import_path: Path to the configuration file to import
            
        Returns:
            True if import was successful
        """
        import_path = Path(import_path)
        
        if not import_path.exists():
            return False
        
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'config' in import_data:
                self.config = import_data['config']
            else:
                self.config = import_data
            
            self.save_config()
            return True
            
        except Exception as e:
            print(f"Warning: Could not import config from {import_path}: {e}")
            return False 