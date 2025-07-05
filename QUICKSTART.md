# CmdChronicle Quick Start Guide

## 🚀 Quick Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd CmdChronicle
   ```

2. **Run the installation script**
   ```bash
   ./install.sh
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

## 🎯 Quick Usage

### Basic Analysis
```bash
# Run complete analysis pipeline
python cmdchronicle.py full_analysis

# Or run individual steps
python cmdchronicle.py collect
python cmdchronicle.py analyze
python cmdchronicle.py insights
python cmdchronicle.py visualize
```

### Check Status
```bash
python cmdchronicle.py status
```

### Demo Mode
```bash
python demo.py
```

## 📊 What You'll Get

After running the analysis, you'll find:

- **`data/`** - Raw data files (commands, patterns, insights)
- **`reports/`** - Generated visualizations and reports
  - `command_wordcloud.png` - Word cloud of your commands
  - `commemorative_page.html` - Beautiful summary page
  - `comprehensive_report.html` - Detailed analysis report

## 🤖 AI Insights Requirements

For AI-powered insights, you need:

1. **Ollama installed** - Visit https://ollama.ai
2. **A model downloaded** - Run `ollama pull llama3.2`
3. **Ollama running** - Run `ollama serve`

## 🛠️ Configuration

Edit `config/config.json` to customize:
- Ollama settings
- Command collection preferences
- Analysis parameters
- Visualization options

## 📝 Example Output

The tool will generate insights like:
- **Workflow Type**: "Frontend Development Wizard"
- **Primary Focus**: "JavaScript/Node.js development"
- **Automation Opportunities**: "Create aliases for git commands"
- **Personality Traits**: "Version control conscious", "Automation-minded"

## 🎨 Fun Features

- **Word Clouds**: Visual representation of your command patterns
- **Commemorative Pages**: Beautiful HTML summaries
- **Automation Suggestions**: Specific recommendations for improving workflow
- **Skill Progression**: Track your command-line expertise over time

## 🔧 Troubleshooting

### Common Issues

1. **"Ollama connection failed"**
   - Make sure Ollama is installed and running
   - Check if the model is downloaded: `ollama list`

2. **"No commands found"**
   - Check your shell history file exists
   - Try different shell types: `--shell zsh` or `--shell bash`

3. **"Import errors"**
   - Make sure you're in the virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

```bash
# See all available commands
python cmdchronicle.py --help

# Get help for specific command
python cmdchronicle.py collect --help
```

## 🎉 Next Steps

1. **Customize your workflow** - Edit configuration files
2. **Create automation scripts** - Use the suggested aliases and scripts
3. **Share your insights** - The HTML reports are shareable
4. **Track progress** - Run analysis regularly to see improvements

Happy command-line analyzing! 🎯 