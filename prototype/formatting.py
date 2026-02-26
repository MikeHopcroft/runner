from rich.console import Console
from rich.pretty import Pretty

from .journal import HasUUID, Journal, JournalEntry, Processor

def entry_metrics_default[InputT: HasUUID, OutputT](entry: JournalEntry[InputT, OutputT]) -> dict[str, bool | int | float]:
    """Extract metrics from a journal entry for summarization."""
    return {"complete": entry.status == "success"}

def format_entry_default[InputT: HasUUID, OutputT](
    console: Console,
    entry: JournalEntry[InputT, OutputT],
) -> None:
    """Format a single journal entry. Override for custom formatting."""
    # Default leverages the discriminated union
    uuid_short = str(entry.input.id)[:8]
    
    if entry.status == "success":
        console.print(f"[green]✓[/green] [dim]{uuid_short}[/dim] ", end="")
        console.print(Pretty(entry.output, max_length=3, max_string=80))
    else:
        console.print(f"[red]✗[/red] [dim]{uuid_short}[/dim] ", end="")
        console.print(f"[red]{entry.error.message}[/red]")
        if entry.error.traceback:
            console.print(f"[dim]{entry.error.traceback}[/dim]")

def format_journal_default[ConfigT, InputT: HasUUID, OutputT](
    console: Console,
    journal: Journal[ConfigT, InputT, OutputT],
) -> None:
    ...

def format_summary_default[ConfigT, InputT: HasUUID, OutputT](
    console: Console,
    journal: Journal[ConfigT, InputT, OutputT],
) -> None:
    ...
