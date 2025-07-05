#!/usr/bin/env python3
"""
CmdChronicle - Command History Analysis Tool
Analyzes command history to discover patterns and generate insights.
"""

import click
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from collectors.history_collector import CommandHistoryCollector
from analyzers.pattern_analyzer import PatternAnalyzer
from analyzers.ai_analyzer import AIAnalyzer
from visualizers.report_generator import ReportGenerator
from visualizers.wordcloud_generator import WordcloudGenerator
from utils.config_manager import ConfigManager
from utils.data_manager import DataManager

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """CmdChronicle - Analyze your command history and discover patterns!"""
    pass

@cli.command()
@click.option('--shell', default='auto', help='Shell type (bash, zsh, auto)')
@click.option('--limit', default=1000, help='Number of commands to collect')
@click.option('--output', default='data/commands.json', help='Output file path')
def collect(shell, limit, output):
    """Collect command history from active terminal sessions."""
    console.print(Panel.fit("🔍 [bold blue]Collecting Command History[/bold blue]", border_style="blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Collecting commands...", total=None)
        
        try:
            collector = CommandHistoryCollector()
            commands = collector.collect_commands(shell=shell, limit=limit)
            
            progress.update(task, description="Saving data...")
            data_manager = DataManager()
            data_manager.save_commands(commands, output)
            
            console.print(f"✅ [green]Collected {len(commands)} commands[/green]")
            console.print(f"📁 [blue]Saved to: {output}[/blue]")
            
        except Exception as e:
            console.print(f"❌ [red]Error: {str(e)}[/red]")
            sys.exit(1)

@cli.command()
@click.option('--input', default='data/commands.json', help='Input file path')
@click.option('--output', default='data/patterns.json', help='Output file path')
def analyze(input, output):
    """Analyze command patterns and identify automation opportunities."""
    console.print(Panel.fit("🧠 [bold green]Analyzing Command Patterns[/bold green]", border_style="green"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Loading commands...", total=None)
        
        try:
            data_manager = DataManager()
            commands = data_manager.load_commands(input)
            
            progress.update(task, description="Analyzing patterns...")
            analyzer = PatternAnalyzer()
            patterns = analyzer.analyze_patterns(commands)
            
            progress.update(task, description="Saving analysis...")
            data_manager.save_patterns(patterns, output)
            
            console.print(f"✅ [green]Analyzed {len(commands)} commands[/green]")
            console.print(f"🔍 [blue]Found {len(patterns['frequent_commands'])} frequent patterns[/blue]")
            console.print(f"🤖 [yellow]Identified {len(patterns['automation_candidates'])} automation candidates[/yellow]")
            
        except Exception as e:
            console.print(f"❌ [red]Error: {str(e)}[/red]")
            sys.exit(1)

@cli.command()
@click.option('--commands', default='data/commands.json', help='Commands file path')
@click.option('--patterns', default='data/patterns.json', help='Patterns file path')
@click.option('--output', default='data/insights.json', help='Output file path')
@click.option('--model', default='llama3.2', help='Ollama model to use')
def insights(commands, patterns, output, model):
    """Generate AI-powered insights about your workflow."""
    console.print(Panel.fit("🤖 [bold purple]Generating AI Insights[/bold purple]", border_style="purple"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Loading data...", total=None)
        
        try:
            data_manager = DataManager()
            commands_data = data_manager.load_commands(commands)
            patterns_data = data_manager.load_patterns(patterns)
            
            progress.update(task, description="Generating AI insights...")
            ai_analyzer = AIAnalyzer(model=model)
            insights = ai_analyzer.generate_insights(commands_data, patterns_data)
            
            progress.update(task, description="Saving insights...")
            data_manager.save_insights(insights, output)
            
            console.print(f"✅ [green]Generated insights using {model}[/green]")
            console.print(f"📊 [blue]Workflow type: {insights.get('workflow_type', 'Unknown')}[/blue]")
            console.print(f"🎯 [yellow]Primary focus: {insights.get('primary_focus', 'Unknown')}[/yellow]")
            
        except Exception as e:
            console.print(f"❌ [red]Error: {str(e)}[/red]")
            sys.exit(1)

@cli.command()
@click.option('--commands', default='data/commands.json', help='Commands file path')
@click.option('--insights', default='data/insights.json', help='Insights file path')
@click.option('--output-dir', default='reports', help='Output directory')
def visualize(commands, insights, output_dir):
    """Generate visualizations and reports."""
    console.print(Panel.fit("🎨 [bold magenta]Generating Visualizations[/bold magenta]", border_style="magenta"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Loading data...", total=None)
        
        try:
            data_manager = DataManager()
            commands_data = data_manager.load_commands(commands)
            insights_data = data_manager.load_insights(insights)
            
            progress.update(task, description="Generating word cloud...")
            wordcloud_gen = WordcloudGenerator()
            wordcloud_path = wordcloud_gen.generate_wordcloud(commands_data, output_dir)
            
            progress.update(task, description="Generating report...")
            report_gen = ReportGenerator()
            report_path = report_gen.generate_report(commands_data, insights_data, output_dir)
            
            console.print(f"✅ [green]Generated visualizations[/green]")
            console.print(f"☁️ [blue]Word cloud: {wordcloud_path}[/blue]")
            console.print(f"📄 [blue]Report: {report_path}[/blue]")
            
        except Exception as e:
            console.print(f"❌ [red]Error: {str(e)}[/red]")
            sys.exit(1)

@cli.command()
def full_analysis():
    """Run complete analysis pipeline: collect → analyze → insights → visualize."""
    console.print(Panel.fit("🚀 [bold cyan]Running Full Analysis Pipeline[/bold cyan]", border_style="cyan"))
    
    try:
        # Step 1: Collect
        console.print("\n[bold]Step 1: Collecting Commands[/bold]")
        ctx = click.Context(cli)
        collect.callback(shell='auto', limit=1000, output='data/commands.json')
        
        # Step 2: Analyze
        console.print("\n[bold]Step 2: Analyzing Patterns[/bold]")
        analyze.callback(input='data/commands.json', output='data/patterns.json')
        
        # Step 3: Generate Insights
        console.print("\n[bold]Step 3: Generating AI Insights[/bold]")
        insights.callback(commands='data/commands.json', patterns='data/patterns.json', output='data/insights.json')
        
        # Step 4: Visualize
        console.print("\n[bold]Step 4: Creating Visualizations[/bold]")
        visualize.callback(commands='data/commands.json', insights='data/insights.json', output_dir='reports')
        
        console.print("\n🎉 [bold green]Full analysis complete![/bold green]")
        console.print("📁 [blue]Check the 'reports' directory for your results[/blue]")
        
    except Exception as e:
        console.print(f"❌ [red]Error in pipeline: {str(e)}[/red]")
        sys.exit(1)

@cli.command()
def status():
    """Show current status and available data."""
    console.print(Panel.fit("📊 [bold yellow]CmdChronicle Status[/bold yellow]", border_style="yellow"))
    
    data_dir = Path("data")
    reports_dir = Path("reports")
    
    if data_dir.exists():
        console.print("\n[bold]Data Files:[/bold]")
        for file in data_dir.glob("*.json"):
            size = file.stat().st_size
            console.print(f"  📄 {file.name} ({size} bytes)")
    else:
        console.print("  ❌ No data directory found")
    
    if reports_dir.exists():
        console.print("\n[bold]Reports:[/bold]")
        for file in reports_dir.glob("*"):
            if file.is_file():
                size = file.stat().st_size
                console.print(f"  📄 {file.name} ({size} bytes)")
    else:
        console.print("  ❌ No reports directory found")

if __name__ == '__main__':
    cli() 