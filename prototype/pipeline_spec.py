from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any
from pydantic import BaseModel, Field
from rich.console import Console
from rich.pretty import Pretty

from .column_spec import ColumnSpec, id_column, status_column
from .formatting import entry_metrics_default, format_entry_default, format_journal_default, format_summary_default
from .journal import HasUUID, Journal, JournalEntry, Processor

"""
PipelineSpec Design
===================

A PipelineSpec defines everything the framework needs to run a pipeline:
metadata (name, description), configuration defaults, processing logic,
and formatting/summarization behavior.

Key design decisions:

1. ABC with default implementations: Users subclass PipelineSpec and override
   only what they need. Abstract methods must be implemented; optional methods
   have sensible defaults.

2. Registry holds instances: The framework maintains a dict[str, PipelineSpec]
   mapping names to pipeline instances. This allows generic methods to access
   bound type parameters (CONFIG, INPUT, OUTPUT).

3. Three levels of customization for formatting/summarization:
   - Use defaults: Do nothing
   - Configure defaults: Set formatter_config/summarizer_config class attributes
   - Replace entirely: Override format_entry()/summarize() methods

4. Configuration merging: PipelineSpec.default_config provides defaults. The
   framework merges these with CLI overrides and environment secrets to produce
   the runtime config passed to create_processor().

5. Typed journal entries: Formatters receive JournalEntry[INPUT, OUTPUT], a
   discriminated union of JournalEntrySuccess and JournalEntryError. This
   enables smart defaults that handle UUIDs, timestamps, and errors without
   user customization.

Example:

    class ScoringPipeline(PipelineSpec[MyConfig, MyInput, MyOutput]):
        name = "scoring"
        description = "Score LLM responses"
        default_config = MyConfig(model="gpt-4")

        def create_processor(self, config: MyConfig) -> Processor[...]:
            async def process(input: MyInput) -> MyOutput:
                return await score(config.model, input.prompt)
            return process
"""

class PipelineSpec[ConfigT, InputT: HasUUID, OutputT](ABC):
    """
    Base class for pipeline specifications.
    
    Subclass and implement abstract members. Override optional methods
    only if you need custom behavior.
    """
    
    name: str
    description: str
    default_config: ConfigT

    column_specs: tuple[ColumnSpec[InputT, OutputT], ...] = (id_column, status_column)
    
    @abstractmethod
    def create_processor(self, config: ConfigT) -> Processor[InputT, OutputT]:
        """
        Create processor that uses the merged runtime config.
        The runtime config is produced by merging PipelineSpec.default_config
        with CLI overrides (e.g. model.name=gptp5)and environment secrets.
        The values in the configuration hold for all invokations of the
        Processor.
        """
        ...

    def entry_metrics(self, entry: JournalEntry[InputT, OutputT]) -> dict[str, bool | int | float]:
        """
        Extract metrics from a journal entry for summarization.
        Metrics include facts about the entry (e.g. whether it succeeded,
        whether it was evaluated as passing, etc.) and numerical values (e.g.
        a score, the number of tokens in the output, the number of user toruns,
        etc.) that can be aggregated in the summary or used for conditional
        formatting (e.g. color rows red if score < 0.5).
        """
        return entry_metrics_default(entry)
    
    def format_entry(
        self,
        console: Console,
        entry: JournalEntry[InputT, OutputT],
    ) -> None:
        format_entry_default(console, entry)

    def format_journal(
        self,
        console: Console,
        journal: Journal[ConfigT, InputT, OutputT],
    ) -> None:
        format_journal_default(console, journal)

    def format_summary(
        self,
        console: Console,
        journal: Journal[ConfigT, InputT, OutputT],
    ) -> None:
        format_summary_default(console, journal)

