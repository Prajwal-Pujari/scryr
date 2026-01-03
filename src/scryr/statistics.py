"""Statistics collection and display for project analysis."""

from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass, field
from collections import defaultdict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text


@dataclass
class ProjectStats:
    """Container for project statistics."""
    
    # File counts
    total_files: int = 0
    total_dirs: int = 0
    
    # Language breakdown
    files_by_language: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Size metrics
    total_size: int = 0
    files_by_size: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Lines of code
    total_lines: int = 0
    lines_by_language: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # File categories
    code_files: int = 0
    config_files: int = 0
    doc_files: int = 0
    test_files: int = 0
    other_files: int = 0
    
    # Largest files
    largest_files: List[tuple] = field(default_factory=list)  # [(path, size), ...]
    
    # Deepest path
    max_depth: int = 0
    deepest_path: str = ""


# Language mappings
LANGUAGE_EXTENSIONS = {
    'Python': {'.py', '.pyw', '.pyx'},
    'JavaScript': {'.js', '.mjs', '.cjs', '.jsx'},
    'TypeScript': {'.ts', '.tsx'},
    'Go': {'.go'},
    'Rust': {'.rs'},
    'Java': {'.java'},
    'C/C++': {'.c', '.cpp', '.cc', '.cxx', '.h', '.hpp'},
    'Ruby': {'.rb', '.rake'},
    'PHP': {'.php'},
    'C#': {'.cs'},
    'Swift': {'.swift'},
    'Kotlin': {'.kt', '.kts'},
    'Scala': {'.scala'},
    'Shell': {'.sh', '.bash', '.zsh', '.fish'},
    'HTML': {'.html', '.htm'},
    'CSS': {'.css', '.scss', '.sass', '.less'},
    'SQL': {'.sql'},
    'R': {'.r', '.R'},
    'Dart': {'.dart'},
    'Lua': {'.lua'},
}

# Config file extensions
CONFIG_EXTENSIONS = {
    '.json', '.yaml', '.yml', '.toml', '.ini', '.conf', 
    '.env', '.properties', '.xml', '.config'
}

# Documentation extensions
DOC_EXTENSIONS = {
    '.md', '.txt', '.rst', '.adoc', '.tex'
}


def get_language(file_path: Path) -> str:
    """Determine programming language from file extension."""
    ext = file_path.suffix.lower()
    
    for lang, extensions in LANGUAGE_EXTENSIONS.items():
        if ext in extensions:
            return lang
    
    return 'Other'


def count_lines(file_path: Path) -> int:
    """Count lines in a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except (OSError, PermissionError):
        return 0


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    try:
        return file_path.stat().st_size
    except (OSError, PermissionError):
        return 0


def categorize_file(file_path: Path) -> str:
    """Categorize file type."""
    name = file_path.name.lower()
    ext = file_path.suffix.lower()
    
    # Test files
    if 'test' in name or name.startswith('test_') or name.endswith('_test'):
        return 'test'
    if ext in {'.spec.js', '.spec.ts', '.test.js', '.test.ts'}:
        return 'test'
    if any(part in file_path.parts for part in ['tests', 'test', '__tests__', 'spec']):
        return 'test'
    
    # Config files
    if ext in CONFIG_EXTENSIONS:
        return 'config'
    if name in {'dockerfile', 'makefile', 'rakefile', 'gemfile', 'pipfile'}:
        return 'config'
    
    # Documentation
    if ext in DOC_EXTENSIONS:
        return 'doc'
    if name in {'readme', 'license', 'changelog', 'contributing'}:
        return 'doc'
    
    # Code files
    lang = get_language(file_path)
    if lang != 'Other':
        return 'code'
    
    return 'other'


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def collect_statistics(node, stats: ProjectStats, depth: int = 0, root_path: Path = None) -> None:
    """Recursively collect statistics from directory tree."""
    if root_path is None:
        root_path = node.path
    
    # Track depth
    if depth > stats.max_depth:
        stats.max_depth = depth
        stats.deepest_path = str(node.path.relative_to(root_path))
    
    if node.is_dir:
        stats.total_dirs += 1
        for child in node.children:
            collect_statistics(child, stats, depth + 1, root_path)
    else:
        stats.total_files += 1
        
        # Get file size
        size = get_file_size(node.path)
        stats.total_size += size
        
        # Track largest files
        rel_path = str(node.path.relative_to(root_path))
        stats.largest_files.append((rel_path, size))
        
        # Language detection
        lang = get_language(node.path)
        stats.files_by_language[lang] += 1
        
        # Line counting for code files
        if lang != 'Other':
            lines = count_lines(node.path)
            stats.total_lines += lines
            stats.lines_by_language[lang] += lines
        
        # Categorize file
        category = categorize_file(node.path)
        if category == 'code':
            stats.code_files += 1
        elif category == 'config':
            stats.config_files += 1
        elif category == 'doc':
            stats.doc_files += 1
        elif category == 'test':
            stats.test_files += 1
        else:
            stats.other_files += 1


def render_statistics(stats: ProjectStats, console: Console) -> None:
    """Render beautiful statistics dashboard."""
    
    # Sort largest files
    stats.largest_files.sort(key=lambda x: x[1], reverse=True)
    
    # Header
    title = Text("📊 Project Statistics", style="bold cyan")
    console.print()
    console.print(Panel(title, border_style="cyan"))
    console.print()
    
    # Overview metrics - Create panels for key stats
    overview_panels = []
    
    # Files panel
    files_text = Text()
    files_text.append(f"{stats.total_files:,}", style="bold cyan")
    files_text.append(f"\n{stats.total_dirs:,} directories", style="dim")
    overview_panels.append(Panel(files_text, title="[bold]Files[/bold]", border_style="blue"))
    
    # Size panel
    size_text = Text()
    size_text.append(format_size(stats.total_size), style="bold cyan")
    size_text.append(f"\nTotal size", style="dim")
    overview_panels.append(Panel(size_text, title="[bold]Size[/bold]", border_style="blue"))
    
    # Lines panel
    lines_text = Text()
    lines_text.append(f"{stats.total_lines:,}", style="bold cyan")
    lines_text.append(f"\nLines of code", style="dim")
    overview_panels.append(Panel(lines_text, title="[bold]Lines[/bold]", border_style="blue"))
    
    # Depth panel
    depth_text = Text()
    depth_text.append(f"{stats.max_depth}", style="bold cyan")
    depth_text.append(f"\nMax depth", style="dim")
    overview_panels.append(Panel(depth_text, title="[bold]Depth[/bold]", border_style="blue"))
    
    console.print(Columns(overview_panels, equal=True, expand=True))
    console.print()
    
    # Language breakdown table
    if stats.files_by_language:
        lang_table = Table(title="[bold]Languages[/bold]", box=None, show_header=True, 
                          title_style="bold", padding=(0, 2))
        lang_table.add_column("Language", style="cyan")
        lang_table.add_column("Files", justify="right", style="yellow")
        lang_table.add_column("Lines", justify="right", style="green")
        lang_table.add_column("Percentage", justify="right", style="dim")
        
        # Sort by file count
        sorted_langs = sorted(stats.files_by_language.items(), 
                            key=lambda x: x[1], reverse=True)
        
        for lang, count in sorted_langs:
            if lang == 'Other':
                continue
            percentage = (count / stats.total_files) * 100
            lines = stats.lines_by_language.get(lang, 0)
            lines_str = f"{lines:,}" if lines > 0 else "-"
            lang_table.add_row(
                lang,
                f"{count:,}",
                lines_str,
                f"{percentage:.1f}%"
            )
        
        console.print(lang_table)
        console.print()
    
    # File categories table
    categories_table = Table(title="[bold]File Categories[/bold]", box=None, 
                            show_header=True, title_style="bold", padding=(0, 2))
    categories_table.add_column("Category", style="cyan")
    categories_table.add_column("Count", justify="right", style="yellow")
    categories_table.add_column("Percentage", justify="right", style="dim")
    
    categories = [
        ("Code", stats.code_files),
        ("Tests", stats.test_files),
        ("Config", stats.config_files),
        ("Documentation", stats.doc_files),
        ("Other", stats.other_files),
    ]
    
    for name, count in categories:
        if count > 0:
            percentage = (count / stats.total_files) * 100
            categories_table.add_row(name, f"{count:,}", f"{percentage:.1f}%")
    
    console.print(categories_table)
    console.print()
    
    # Largest files table
    if stats.largest_files:
        large_table = Table(title="[bold]Largest Files[/bold]", box=None, 
                          show_header=True, title_style="bold", padding=(0, 2))
        large_table.add_column("File", style="cyan", no_wrap=False)
        large_table.add_column("Size", justify="right", style="yellow")
        
        # Show top 10
        for path, size in stats.largest_files[:10]:
            large_table.add_row(path, format_size(size))
        
        console.print(large_table)
        console.print()
    
    # Additional insights
    insights = []
    
    # Test coverage estimate
    if stats.code_files > 0:
        test_ratio = (stats.test_files / stats.code_files) * 100
        if test_ratio < 20:
            insights.append(f"⚠️  Low test coverage: {test_ratio:.1f}% test files to code files")
        elif test_ratio > 50:
            insights.append(f"✅ Good test coverage: {test_ratio:.1f}% test files to code files")
    
    # Average file size
    if stats.total_files > 0:
        avg_size = stats.total_size / stats.total_files
        insights.append(f"📏 Average file size: {format_size(avg_size)}")
    
    # Average lines per file
    if stats.code_files > 0 and stats.total_lines > 0:
        avg_lines = stats.total_lines / stats.code_files
        insights.append(f"📝 Average lines per code file: {avg_lines:.0f}")
    
    # Deepest path
    if stats.deepest_path:
        insights.append(f"🔍 Deepest path ({stats.max_depth} levels): {stats.deepest_path}")
    
    if insights:
        console.print("[bold]Insights[/bold]")
        for insight in insights:
            console.print(f"  {insight}", style="dim")
        console.print()