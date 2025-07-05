# CmdChronicle

A command-line tool that analyzes your command history to discover patterns, identify automation opportunities, and generate fun insights about your development workflow.

## Features

- 🔍 **Command History Analysis**: Collects and analyzes commands from active terminal sessions
- 🧠 **Pattern Recognition**: Identifies repetitive commands and workflows
- 🤖 **Automation Suggestions**: Recommends commands that can be automated
- 📊 **Workflow Insights**: Generates summaries and visualizations of your development patterns
- 🎨 **Fun Visualizations**: Creates word clouds and commemorative pages
- 🏠 **Local Processing**: Uses local Ollama for AI analysis (no cloud dependencies)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analysis
python cmdchronicle.py analyze

# Generate insights
python cmdchronicle.py insights

# Create visualizations
python cmdchronicle.py visualize
```

## Project Structure

```
CmdChronicle/
├── cmdchronicle.py          # Main CLI application
├── src/
│   ├── collectors/          # Command history collectors
│   ├── analyzers/           # Pattern analysis and AI processing
│   ├── visualizers/         # Visualization and reporting
│   └── utils/              # Utility functions
├── data/                   # Collected and processed data
├── reports/                # Generated reports and visualizations
├── config/                 # Configuration files
└── tests/                  # Test suite
```

## Requirements

- Python 3.8+
- Ollama (local LLM)
- Shell access (bash/zsh)