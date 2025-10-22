"""
Logging utilities for Content Researcher Agent
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown


console = Console()


def setup_logger(log_level: str = "INFO", log_file: str = None):
    """Setup structured logger"""
    logger = logging.getLogger("content_researcher")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


class AgentLogger:
    """Rich console logger for beautiful output"""
    
    def __init__(self):
        self.console = Console()
    
    def print_header(self, title: str):
        """Print fancy header"""
        self.console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        self.console.print(f"[bold cyan]{title.center(60)}[/bold cyan]")
        self.console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
    
    def print_section(self, title: str):
        """Print section divider"""
        self.console.print(f"\n[bold yellow]📊 {title}[/bold yellow]")
        self.console.print(f"[dim]{'-'*60}[/dim]")
    
    def print_topics_table(self, topics: list):
        """Print topics in a beautiful table"""
        table = Table(title="🎯 Researched Content Topics", show_header=True, header_style="bold magenta")
        
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Topic", style="white", width=35)
        table.add_column("Score", style="green", justify="center", width=8)
        table.add_column("Views Potential", style="yellow", justify="right", width=12)
        table.add_column("Category", style="blue", width=15)
        
        for i, topic in enumerate(topics[:20], 1):  # Show top 20
            score_style = "bold green" if topic['total_score'] >= 80 else "yellow" if topic['total_score'] >= 60 else "dim"
            table.add_row(
                str(i),
                topic['title'][:35],
                f"{topic['total_score']:.0f}",
                f"{topic.get('views_potential', 0):,}",
                topic.get('category', 'General')
            )
        
        self.console.print(table)
    
    def print_topic_detail(self, topic: dict):
        """Print detailed topic analysis"""
        self.console.print(Panel.fit(
            f"[bold]{topic['title']}[/bold]\n\n"
            f"[cyan]Total Score:[/cyan] {topic['total_score']:.0f}/100\n"
            f"[cyan]Importance:[/cyan] {topic['importance_score']:.0f}/100\n"
            f"[cyan]Watchability:[/cyan] {topic['watchability_score']:.0f}/100\n"
            f"[cyan]Monetization:[/cyan] {topic['monetization_score']:.0f}/100\n"
            f"[cyan]Popularity:[/cyan] {topic['popularity_score']:.0f}/100\n"
            f"[cyan]Innovation:[/cyan] {topic['innovation_score']:.0f}/100\n\n"
            f"[yellow]Category:[/yellow] {topic.get('category', 'General')}\n"
            f"[yellow]Competition:[/yellow] {topic.get('competition_level', 'N/A')}/10\n"
            f"[yellow]Keywords:[/yellow] {', '.join(topic.get('keywords', [])[:5])}\n\n"
            f"[dim]{topic.get('notes', 'No notes available')}[/dim]",
            title="📝 Topic Details",
            border_style="cyan"
        ))
    
    def print_research_summary(self, summary: dict):
        """Print research session summary"""
        self.console.print(Panel.fit(
            f"[bold green]✅ Research Session Complete![/bold green]\n\n"
            f"[cyan]Topics Researched:[/cyan] {summary.get('topics_researched', 0)}\n"
            f"[cyan]High Quality Topics:[/cyan] {summary.get('high_quality_count', 0)}\n"
            f"[cyan]Videos Analyzed:[/cyan] {summary.get('videos_analyzed', 0)}\n"
            f"[cyan]Competitors Checked:[/cyan] {summary.get('competitors_checked', 0)}\n"
            f"[cyan]Duration:[/cyan] {summary.get('duration_seconds', 0):.1f}s\n"
            f"[cyan]Success Rate:[/cyan] {summary.get('success_rate', 0):.1%}",
            title="📊 Session Summary",
            border_style="green"
        ))
    
    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"[bold red]❌ Error:[/bold red] {message}")
    
    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"[bold green]✅ {message}[/bold green]")
    
    def print_warning(self, message: str):
        """Print warning message"""
        self.console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    
    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"[cyan]ℹ️  {message}[/cyan]")
    
    def ask_confirmation(self, question: str) -> bool:
        """Ask user for yes/no confirmation"""
        response = self.console.input(f"[bold yellow]{question} (y/n):[/bold yellow] ").lower()
        return response in ['y', 'yes']
    
    def create_progress(self, description: str):
        """Create a progress bar"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        )

