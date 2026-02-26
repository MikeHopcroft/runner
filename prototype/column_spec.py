from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field
from rich.console import RenderableType
from rich.text import Text

from .journal import HasUUID, JournalEntry


# Used to soecify the columns displayed by PipelineSpec.format_summary().
# The contents field is a function that takes a JournalEntry and produces the
# cell contents. The params field is a dict of rich library formatting
# parameters that are passed to the Rich Table.add_column() method when
# creating the summary table.
class ColumnSpec[InputT: HasUUID, OutputT](BaseModel):
    name: str = Field(..., min_length=1, description="Column name")
    params: dict[str, Any] = Field(
        {}, description="Rich formatting parameters for the column"
    )

    contents: Callable[[JournalEntry[InputT, OutputT]], RenderableType] = Field(
        ..., description="Function to create the cell contents"
    )


def column_spec[InputT: HasUUID, OutputT](
    name: str,
    contents: Callable[[JournalEntry[InputT, OutputT]], RenderableType],
    **kwargs: Any,
) -> ColumnSpec[InputT, OutputT]:
    """
    Convenience factory creates ColumnSpec for use in SummarizerSpec.
    Mainly exists to simplify passing Rich formatting parameters via kwargs.
    """
    return ColumnSpec[InputT, OutputT](name=name, contents=contents, params=kwargs)


# Using named functions instead of lambdas for better type safety with generics.
def _get_id(entry: JournalEntry[HasUUID, Any]) -> str:
    return str(entry.input.id)


def _get_status(entry: JournalEntry[HasUUID, Any]) -> Text:
    color = "green" if entry.status == "success" else "red"
    return Text(entry.status, style=color)


# Common column specs for summary tables.
id_column = column_spec("ID", _get_id)
status_column = column_spec("Status", _get_status)
