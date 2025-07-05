"""
AI Analyzer
Uses local Ollama to generate insights about command patterns and workflows.
"""

import json
import requests
from typing import List, Dict, Any
from datetime import datetime


class AIAnalyzer:
    """Uses Ollama to analyze command patterns and generate insights."""
    
    def __init__(self, model: str = 'llama3.2', base_url: str = 'http://localhost:11434'):
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Workflow archetypes for classification
        self.workflow_archetypes = {
            'frontend_developer': {
                'keywords': ['npm', 'yarn', 'node', 'react', 'vue', 'angular', 'webpack', 'babel'],
                'description': 'Frontend development with modern JavaScript frameworks'
            },
            'backend_developer': {
                'keywords': ['python', 'django', 'flask', 'node', 'express', 'java', 'spring'],
                'description': 'Backend development with server-side technologies'
            },
            'devops_engineer': {
                'keywords': ['docker', 'kubernetes', 'kubectl', 'terraform', 'ansible', 'jenkins'],
                'description': 'DevOps and infrastructure management'
            },
            'data_scientist': {
                'keywords': ['python', 'jupyter', 'pandas', 'numpy', 'matplotlib', 'r', 'sql'],
                'description': 'Data analysis and machine learning'
            },
            'system_administrator': {
                'keywords': ['sudo', 'systemctl', 'apt', 'yum', 'ssh', 'rsync', 'cron'],
                'description': 'System administration and maintenance'
            },
            'security_analyst': {
                'keywords': ['nmap', 'wireshark', 'tcpdump', 'openssl', 'gpg', 'hash'],
                'description': 'Security analysis and penetration testing'
            }
        }
    
    def generate_insights(self, commands_data: List[Dict[str, Any]], patterns_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-powered insights about the user's workflow.
        
        Args:
            commands_data: List of command dictionaries
            patterns_data: Pattern analysis results
            
        Returns:
            Dictionary containing AI-generated insights
        """
        try:
            # Prepare data for AI analysis
            analysis_data = self._prepare_analysis_data(commands_data, patterns_data)
            
            # Generate insights using Ollama
            insights = self._generate_ollama_insights(analysis_data)
            
            # Add metadata
            insights['generated_at'] = datetime.now().isoformat()
            insights['model_used'] = self.model
            insights['data_summary'] = self._create_data_summary(commands_data, patterns_data)
            
            return insights
            
        except Exception as e:
            print(f"Warning: AI analysis failed: {e}")
            return self._fallback_insights(commands_data, patterns_data)
    
    def _prepare_analysis_data(self, commands_data: List[Dict[str, Any]], patterns_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for AI analysis."""
        # Extract key information
        commands = [cmd['command'] for cmd in commands_data]
        frequent_commands = patterns_data.get('frequent_commands', [])
        tool_usage = patterns_data.get('tool_usage', {})
        workflows = patterns_data.get('workflows', [])
        
        # Create analysis context
        analysis_data = {
            'total_commands': len(commands),
            'unique_commands': len(set(commands)),
            'most_frequent_commands': frequent_commands[:10],
            'tool_usage': tool_usage,
            'workflow_types': [w.get('workflow_type', 'unknown') for w in workflows],
            'command_sample': commands[:50],  # Sample for context
            'time_span': self._calculate_time_span(commands_data)
        }
        
        return analysis_data
    
    def _generate_ollama_insights(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights using Ollama API."""
        prompt = self._create_analysis_prompt(analysis_data)
        
        try:
            response = requests.post(
                self.api_url,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.7,
                        'top_p': 0.9,
                        'max_tokens': 2000
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Parse the response
                insights = self._parse_ai_response(response_text, analysis_data)
                return insights
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Ollama: {e}")
    
    def _create_analysis_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Create a prompt for AI analysis."""
        prompt = f"""
You are an expert command-line workflow analyst. Analyze the following command history data and provide insights about the user's work patterns, automation opportunities, and workflow characteristics.

Data Summary:
- Total commands: {analysis_data['total_commands']}
- Unique commands: {analysis_data['unique_commands']}
- Time span: {analysis_data['time_span']}

Most frequent commands:
{self._format_frequent_commands(analysis_data['most_frequent_commands'])}

Tool usage:
{self._format_tool_usage(analysis_data['tool_usage'])}

Workflow types observed:
{', '.join(analysis_data['workflow_types'])}

Sample commands:
{chr(10).join(analysis_data['command_sample'][:20])}

Please provide a JSON response with the following structure:
{{
    "workflow_type": "classification of the user's primary workflow",
    "primary_focus": "main area of work/technology focus",
    "workflow_characteristics": ["list", "of", "key", "characteristics"],
    "automation_opportunities": ["list", "of", "automation", "suggestions"],
    "productivity_insights": ["list", "of", "productivity", "observations"],
    "skill_level": "estimated skill level (beginner/intermediate/advanced/expert)",
    "recommendations": ["list", "of", "recommendations", "for", "improvement"],
    "fun_title": "a fun, creative title for this user's workflow",
    "personality_traits": ["list", "of", "personality", "traits", "inferred", "from", "commands"]
}}

Focus on being insightful, practical, and fun. The user is a developer who wants to understand their patterns and improve their workflow.
"""
        return prompt
    
    def _format_frequent_commands(self, frequent_commands: List[Dict]) -> str:
        """Format frequent commands for the prompt."""
        formatted = []
        for cmd in frequent_commands[:10]:
            formatted.append(f"- {cmd['command']} (used {cmd['count']} times, {cmd['percentage']}%)")
        return '\n'.join(formatted)
    
    def _format_tool_usage(self, tool_usage: Dict) -> str:
        """Format tool usage for the prompt."""
        formatted = []
        for tool, stats in tool_usage.items():
            formatted.append(f"- {tool}: {stats['count']} commands ({stats['percentage']:.1f}%)")
        return '\n'.join(formatted)
    
    def _parse_ai_response(self, response_text: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the AI response and extract insights."""
        try:
            # Try to extract JSON from the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                insights = json.loads(json_str)
            else:
                # Fallback parsing
                insights = self._parse_text_response(response_text)
            
            # Validate and enhance insights
            insights = self._validate_and_enhance_insights(insights, analysis_data)
            
            return insights
            
        except json.JSONDecodeError:
            # Fallback to text parsing
            return self._parse_text_response(response_text)
    
    def _parse_text_response(self, response_text: str) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails."""
        insights = {
            'workflow_type': 'general_development',
            'primary_focus': 'command_line_automation',
            'workflow_characteristics': ['command-line focused', 'pattern-driven'],
            'automation_opportunities': ['alias creation', 'script automation'],
            'productivity_insights': ['frequent command repetition', 'opportunity for optimization'],
            'skill_level': 'intermediate',
            'recommendations': ['create aliases for frequent commands', 'develop automation scripts'],
            'fun_title': 'The Command Line Explorer',
            'personality_traits': ['efficient', 'systematic', 'automation-minded']
        }
        
        # Try to extract information from the text
        text_lower = response_text.lower()
        
        if any(word in text_lower for word in ['frontend', 'react', 'vue', 'angular']):
            insights['workflow_type'] = 'frontend_development'
        elif any(word in text_lower for word in ['backend', 'server', 'api']):
            insights['workflow_type'] = 'backend_development'
        elif any(word in text_lower for word in ['devops', 'docker', 'kubernetes']):
            insights['workflow_type'] = 'devops_engineering'
        
        return insights
    
    def _validate_and_enhance_insights(self, insights: Dict[str, Any], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enhance AI-generated insights."""
        # Ensure all required fields exist
        required_fields = [
            'workflow_type', 'primary_focus', 'workflow_characteristics',
            'automation_opportunities', 'productivity_insights', 'skill_level',
            'recommendations', 'fun_title', 'personality_traits'
        ]
        
        for field in required_fields:
            if field not in insights:
                insights[field] = self._get_default_value(field)
        
        # Enhance with data-driven insights
        insights['data_driven_insights'] = self._generate_data_driven_insights(analysis_data)
        insights['command_diversity_score'] = analysis_data['unique_commands'] / analysis_data['total_commands']
        
        return insights
    
    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing fields."""
        defaults = {
            'workflow_type': 'general_development',
            'primary_focus': 'command_line_automation',
            'workflow_characteristics': ['command-line focused'],
            'automation_opportunities': ['alias creation'],
            'productivity_insights': ['frequent command repetition'],
            'skill_level': 'intermediate',
            'recommendations': ['create aliases for frequent commands'],
            'fun_title': 'The Command Line Explorer',
            'personality_traits': ['efficient']
        }
        return defaults.get(field, 'unknown')
    
    def _generate_data_driven_insights(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate insights based on the actual data."""
        insights = []
        
        # Command diversity
        diversity = analysis_data['unique_commands'] / analysis_data['total_commands']
        if diversity < 0.3:
            insights.append("Low command diversity suggests heavy reliance on a few commands")
        elif diversity > 0.7:
            insights.append("High command diversity indicates exploratory and varied work patterns")
        
        # Tool usage patterns
        tool_usage = analysis_data['tool_usage']
        if tool_usage:
            most_used_tool = max(tool_usage.items(), key=lambda x: x[1]['count'])
            insights.append(f"Primary tool focus: {most_used_tool[0]} ({most_used_tool[1]['percentage']:.1f}% of commands)")
        
        # Workflow patterns
        workflow_types = analysis_data['workflow_types']
        if workflow_types:
            most_common_workflow = max(set(workflow_types), key=workflow_types.count)
            insights.append(f"Most common workflow type: {most_common_workflow}")
        
        return insights
    
    def _calculate_time_span(self, commands_data: List[Dict[str, Any]]) -> str:
        """Calculate the time span of the commands."""
        if not commands_data:
            return "Unknown"
        
        timestamps = [cmd.get('timestamp', 0) for cmd in commands_data if 'timestamp' in cmd]
        if not timestamps:
            return "Unknown"
        
        earliest = min(timestamps)
        latest = max(timestamps)
        span_hours = (latest - earliest) / 3600
        
        if span_hours < 24:
            return f"{span_hours:.1f} hours"
        else:
            days = span_hours / 24
            return f"{days:.1f} days"
    
    def _fallback_insights(self, commands_data: List[Dict[str, Any]], patterns_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback insights when AI analysis fails."""
        # Basic analysis without AI
        commands = [cmd['command'] for cmd in commands_data]
        tool_usage = patterns_data.get('tool_usage', {})
        
        # Determine workflow type based on tool usage
        workflow_type = self._classify_workflow_from_tools(tool_usage)
        
        # Generate basic insights
        insights = {
            'workflow_type': workflow_type,
            'primary_focus': self._get_primary_focus(tool_usage),
            'workflow_characteristics': self._get_workflow_characteristics(commands, tool_usage),
            'automation_opportunities': self._get_automation_opportunities(patterns_data),
            'productivity_insights': self._get_productivity_insights(commands_data, patterns_data),
            'skill_level': self._estimate_skill_level(commands, tool_usage),
            'recommendations': self._get_basic_recommendations(patterns_data),
            'fun_title': self._generate_fun_title(workflow_type, tool_usage),
            'personality_traits': self._infer_personality_traits(commands, tool_usage),
            'data_driven_insights': self._generate_data_driven_insights({
                'total_commands': len(commands),
                'unique_commands': len(set(commands)),
                'tool_usage': tool_usage,
                'workflow_types': []
            }),
            'command_diversity_score': len(set(commands)) / len(commands) if commands else 0,
            'generated_at': datetime.now().isoformat(),
            'model_used': 'fallback_analysis',
            'data_summary': self._create_data_summary(commands_data, patterns_data)
        }
        
        return insights
    
    def _classify_workflow_from_tools(self, tool_usage: Dict) -> str:
        """Classify workflow type based on tool usage."""
        if not tool_usage:
            return 'general_development'
        
        # Score each workflow type
        scores = {}
        for workflow, config in self.workflow_archetypes.items():
            score = 0
            for keyword in config['keywords']:
                for tool, stats in tool_usage.items():
                    if keyword in tool.lower():
                        score += stats['count']
            scores[workflow] = score
        
        # Return the highest scoring workflow
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        else:
            return 'general_development'
    
    def _get_primary_focus(self, tool_usage: Dict) -> str:
        """Get primary focus area."""
        if not tool_usage:
            return 'command_line_automation'
        
        most_used = max(tool_usage.items(), key=lambda x: x[1]['count'])
        return most_used[0]
    
    def _get_workflow_characteristics(self, commands: List[str], tool_usage: Dict) -> List[str]:
        """Get workflow characteristics."""
        characteristics = []
        
        if tool_usage.get('git'):
            characteristics.append('version control focused')
        if tool_usage.get('docker'):
            characteristics.append('containerization aware')
        if tool_usage.get('python'):
            characteristics.append('python development')
        if tool_usage.get('node'):
            characteristics.append('javascript/node.js development')
        
        if len(set(commands)) / len(commands) > 0.5:
            characteristics.append('diverse command usage')
        else:
            characteristics.append('focused command patterns')
        
        return characteristics
    
    def _get_automation_opportunities(self, patterns_data: Dict) -> List[str]:
        """Get automation opportunities."""
        opportunities = []
        
        frequent_commands = patterns_data.get('frequent_commands', [])
        if frequent_commands:
            opportunities.append(f"Create aliases for {len(frequent_commands[:5])} most frequent commands")
        
        automation_candidates = patterns_data.get('automation_candidates', [])
        if automation_candidates:
            opportunities.append(f"Automate {len(automation_candidates[:3])} complex command sequences")
        
        return opportunities
    
    def _get_productivity_insights(self, commands_data: List[Dict], patterns_data: Dict) -> List[str]:
        """Get productivity insights."""
        insights = []
        
        total_commands = len(commands_data)
        unique_commands = len(set(cmd['command'] for cmd in commands_data))
        
        if unique_commands / total_commands < 0.3:
            insights.append("High command repetition suggests automation opportunities")
        elif unique_commands / total_commands > 0.7:
            insights.append("Diverse command usage indicates exploratory work patterns")
        
        return insights
    
    def _estimate_skill_level(self, commands: List[str], tool_usage: Dict) -> str:
        """Estimate skill level."""
        # Simple heuristic based on command complexity and tool usage
        complex_commands = sum(1 for cmd in commands if len(cmd.split()) > 3)
        total_commands = len(commands)
        
        if complex_commands / total_commands > 0.3 and len(tool_usage) > 3:
            return 'advanced'
        elif complex_commands / total_commands > 0.1 and len(tool_usage) > 1:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _get_basic_recommendations(self, patterns_data: Dict) -> List[str]:
        """Get basic recommendations."""
        recommendations = [
            "Create aliases for frequently used commands",
            "Consider automation scripts for repetitive tasks",
            "Explore shell configuration improvements"
        ]
        
        return recommendations
    
    def _generate_fun_title(self, workflow_type: str, tool_usage: Dict) -> str:
        """Generate a fun title for the workflow."""
        titles = {
            'frontend_developer': 'The Frontend Wizard',
            'backend_developer': 'The Backend Architect',
            'devops_engineer': 'The Infrastructure Maestro',
            'data_scientist': 'The Data Explorer',
            'system_administrator': 'The System Guardian',
            'security_analyst': 'The Security Sentinel',
            'general_development': 'The Command Line Explorer'
        }
        
        return titles.get(workflow_type, 'The Terminal Master')
    
    def _infer_personality_traits(self, commands: List[str], tool_usage: Dict) -> List[str]:
        """Infer personality traits from command patterns."""
        traits = []
        
        if tool_usage.get('git'):
            traits.append('version control conscious')
        if tool_usage.get('docker'):
            traits.append('containerization minded')
        if len(set(commands)) / len(commands) > 0.5:
            traits.append('exploratory')
        else:
            traits.append('focused')
        
        return traits
    
    def _create_data_summary(self, commands_data: List[Dict], patterns_data: Dict) -> Dict[str, Any]:
        """Create a summary of the analyzed data."""
        return {
            'total_commands': len(commands_data),
            'unique_commands': len(set(cmd['command'] for cmd in commands_data)),
            'time_range': self._calculate_time_span(commands_data),
            'shell_distribution': self._get_shell_distribution(commands_data),
            'top_tools': self._get_top_tools(patterns_data.get('tool_usage', {}))
        }
    
    def _get_shell_distribution(self, commands_data: List[Dict]) -> Dict[str, int]:
        """Get shell distribution."""
        distribution = {}
        for cmd in commands_data:
            shell = cmd.get('shell', 'unknown')
            distribution[shell] = distribution.get(shell, 0) + 1
        return distribution
    
    def _get_top_tools(self, tool_usage: Dict) -> List[str]:
        """Get top tools used."""
        if not tool_usage:
            return []
        
        sorted_tools = sorted(tool_usage.items(), key=lambda x: x[1]['count'], reverse=True)
        return [tool for tool, _ in sorted_tools[:5]] 