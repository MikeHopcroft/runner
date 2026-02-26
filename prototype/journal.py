"""
Design Goals
- Pydantic model for a Journal that was made by a specific processor. This allows schema validation on load and provides for static type checking features.
- Provide a structured way to record the processing history of a set of inputs through a series of processors.
- Allow for flexible transformation of journal entries to create new inputs for subsequent processing steps.
- Enable the extraction of tabular representations of the journal for analysis and debugging.
- Explicitly capture both successful and failed processing attempts, along with relevant metadata, to facilitate debugging and auditing.
- Put complex asynchronous run logic (RPC retries, batching, rate limiting, etc.)
  in the Runner, which is separate from the processor logic. This way the user can 
  focus on the processor logic and not worry about the complexities of running it at 
  scale.
"""

from typing import Any, AsyncGenerator, Awaitable, Callable, Generator, Literal
from uuid import UUID

from pydantic import BaseModel, Field, JsonValue


class JournalGlobalMetadata(BaseModel):
    """Global metadata for a journal."""

    timestamp: float
    # TBD: add other fields like command line arguments, environment variables, etc.


class JournalEntryMetadata(BaseModel):
    """Metadata for a journal entry."""

    timestamp: float
    # TBD: add other fields like processing time, etc.


class ProcessorError(BaseModel):
    """Error that occurred during processing."""

    message: str
    exception_type: str | None = None
    traceback: str | None = None
    details: JsonValue | None = None


class HasUUID(BaseModel):
    """Base model for objects that have a UUID."""

    id: UUID


class JournalEntryBase[INPUT: HasUUID](BaseModel):
    """Common fields for all journal entries."""

    run_id: UUID  # unique per attempt, distinct from input.id
    metadata: JournalEntryMetadata
    input: INPUT


class JournalEntrySuccess[INPUT: HasUUID, OUTPUT](JournalEntryBase[INPUT]):
    """A successful journal entry with output."""

    status: Literal["success"] = "success"
    output: OUTPUT


class JournalEntryError[INPUT: HasUUID](JournalEntryBase[INPUT]):
    """A failed journal entry with an error."""

    status: Literal["error"] = "error"
    error: ProcessorError


# DESIGN NOTE: when the Runner applies a processor to an input, it results
# in the creation of a JournalEntry. The JournalEntry captures the input,
# the output (if successful), and any error that occurred during processing.
# This allows us to have a complete record of the processing history, which
# can be useful for debugging, auditing, and analysis.
# The JournalEntry also includes metadata such as timestamps, which can help
# us understand the timing and performance of the processing.
type JournalEntry[INPUT: HasUUID, OUTPUT] = (
    JournalEntrySuccess[INPUT, OUTPUT] | JournalEntryError[INPUT]
)

type JournalEntryTransformer[INPUT: HasUUID, OUTPUT, RESULT] = Callable[
    [JournalEntry[INPUT, OUTPUT]], RESULT | None
]


class Journal[CONFIG, INPUT: HasUUID, OUTPUT](BaseModel):
    """A journal that records the processing history."""

    id: UUID
    metadata: JournalGlobalMetadata
    config: CONFIG

    # TODO: verify Pydantic resolves the type alias correctly with the Literal discriminator.
    # Otherwise consider inlining the JournalEntry type directly here.
    entries: list[JournalEntry[INPUT, OUTPUT]]

    # DESIGN NOTE: the transform method allows us to create the input for a
    # subsequent runner invocation by filtering and transforming journal
    # entries. This is a powerful mechanism for building complex processing
    # pipelines, where the output of one processor can be used as the input
    # for another processor. By providing a flexible transformation mechanism,
    # we can enable a wide range of use cases and allow users to customize
    # their processing pipelines in a way that best suits their needs.
    #
    # The transform method is also useful for extracting tabular
    # representations of a Journal.
    def transform[RESULT](
        self,
        transformer: JournalEntryTransformer[INPUT, OUTPUT, RESULT],
    ) -> Generator[RESULT]: 
        """Synchronously map/filter journal entries to produce new values.

        This is intended for lightweight, pure transformations — e.g., reshaping
        a successful output into the input for a subsequent Runner, or extracting
        tabular data for analysis.

        For anything involving I/O, retries, or concurrency, use a Runner instead.
        """
        ...
     

    def save(self, path: str) -> None: ...

    """
    TODO: Validate the save/load round-trip with generics.
    Pydantic's generic model serialization can be tricky when
    CONFIG, INPUT, and OUTPUT are arbitrary types.
    You may need to store type discriminator info in the serialized form,
    or require users to provide concrete types at load time.
    This is worth prototyping early.
    If it doesn't work cleanly, it could force structural changes.
    """
    @classmethod
    def load(cls, path: str) -> "Journal[CONFIG, INPUT, OUTPUT]":
        """Load a journal from disk.

        NOTE: Must be called on a concrete subclass or parameterized type
        so that Pydantic knows how to deserialize CONFIG, INPUT, and OUTPUT.
        E.g.: Journal[MyConfig, MyInput, MyOutput].load("path/to/journal.json")
        """
        ...


# Callable type aliases

type Processor[INPUT: HasUUID, OUTPUT] = Callable[[INPUT], Awaitable[OUTPUT]]

# DESIGN NOTE: the factory pattern reinforces the notion that there is one
# configuration that is used by all invocations of a processor. The intention
# is that invoking a Runner will perform one processor invocation per input,
# and that all invocations will share the same configuration.
#
# This is a common pattern in data processing pipelines, where you have a set
# of transformations that you want to apply to a stream of data, and you want
# to be able to configure those transformations in a consistent way.
type ProcessorFactory[CONFIG, INPUT: HasUUID, OUTPUT] = Callable[
    [CONFIG], Processor[INPUT, OUTPUT]
]

# # NOTE: TypeScript's mapped tuple type `{ [K in keyof OUTPUTS]: Processor<INPUT, OUTPUTS[K]> }`
# # does not have a direct equivalent in Python. Using a list of processors.
# type Processors[INPUT: HasUUID] = list[Processor[INPUT, Any]]

type Runner[CONFIG, INPUT: HasUUID, OUTPUT] = Callable[
    [CONFIG, ProcessorFactory[CONFIG,INPUT, OUTPUT], AsyncGenerator[INPUT] | Generator[INPUT]],
    Awaitable[Journal[CONFIG, INPUT, OUTPUT]],
]

class FormatterSpec(BaseModel):
    before_case: Callable[[Console, dict[str, Any]], None] | None = Field(
        default=None, description="Function to generate contents before each case"
    )
    after_case: Callable[[Console, dict[str, Any]], None] | None = Field(
        default=None, description="Function to generate contents after each case"
    )
    format_turn: Callable[[Console, int, dict[str, Any]], None] | None = Field(
        default=None, description="Function to generate contents for each turn"
    )

class PipelineSpec[CONFIG, INPUT: HasUUID, OUTPUT](BaseModel):
    name: str = Field(..., min_length=1, description="Pipeline name")
    description: str = Field(..., min_length=1, description="Pipeline description")
    configuration: dict[str, Any] = Field(..., description="Pipeline configuration")
    factory: ProcessorFactory[CONFIG, INPUT, OUTPUT] = Field(
        ..., description="Factory function to create the processor")
    formatter: FormatterSpec | Callable | None = Field(
        default=None, description="Optional formatter spec or function"
    )
    passed_predicate: Callable[[dict[str, Any]], bool] = Field(
        default=lambda result: False,
        description="Function to determine if the summarization passed",
    )
    summarizer: SummarizerSpec | Callable | None = Field(
        default=None, description="Optional summarizer spec or function"
    )

