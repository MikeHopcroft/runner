type JournalGlobalMetadata = {
  timestamp: number;
  // TBD: add other fields like command line arguments, environment variables, etc.
};

type JournalEntryMetadata = {
  timestamp: number;
  // TBD: add other fields like processing time, etc.
};

type JsonPrimitive = string | number | boolean | null;
type JsonValue = JsonPrimitive | JsonObject | JsonArray;
type JsonObject = { [key: string]: JsonValue };
type JsonArray = JsonValue[];

type ProcessorError = {
  message: string;
  details?: JsonValue;
};

type UUID = string;
type HasUUID = {
  id: UUID;
};

// DESIGN NOTE: when the Runner applies a processor to an input, it results
// in the creation of a JournalEntry. The JournalEntry captures the input,
// the output (if successful), and any error that occurred during processing.
// This allows us to have a complete record of the processing history, which
// can be useful for debugging, auditing, and analysis.
// The JournalEntry also includes metadata such as timestamps, which can help
// us understand the timing and performance of the processing.
type JournalEntry<INPUT extends HasUUID, OUTPUT> =
  | {
      metadata: JournalEntryMetadata;
      input: INPUT;
      output: OUTPUT;
    }
  | {
      metadata: JournalEntryMetadata;
      input: INPUT;
      error: ProcessorError;
    };

type JournalEntryTransformer<
  INPUT extends HasUUID,
  OUTPUT,
  RESULT extends HasUUID,
> = (entry: JournalEntry<INPUT, OUTPUT>) => Promise<RESULT | null>;

// // DESIGN NOTE: when the Runner applies a processor to an input, it results
// // in the creation of a JournalEntry. The JournalEntry captures the input,
// // the output (if successful), and any error that occurred during processing.
// // This allows us to have a complete record of the processing history, which
// // can be useful for debugging, auditing, and analysis.
// // The JournalEntry also includes metadata such as timestamps, which can help
// // us understand the timing and performance of the processing.
// type JournalEntry<INPUT extends HasUUID, OUTPUT> = {
//   metadata: JournalEntryMetadata;
//   input: INPUT;
//   // DESIGN NOTE: the output is optional because a processor errors might
//   // result in a situation where we have no output to record. Note also that
//   // the implementor of the processor may define OUTPUT with optional properties,
//   // so the presence of an output does not necessarily indicate a successful
//   // processing. The presence or absence of an error is the definitive
//   // indicator of whether the processing was successful or not.
//   // This design allows us to capture as much information as possible about
//   // the processing, even in cases where it fails, which can be invaluable for
//   // troubleshooting and improving our processors over time.
//   output?: OUTPUT;
//   error?: ProcessorError;
// };

// // DESIGN NOTE: JournalEntry2 uses a discriminated union to express the
// // relationship between output and error more precisely:
// // - When processing succeeds (no error), output is guaranteed to be present
// //   and fully populated (OUTPUT).
// // - When processing fails (error present), output is optional and may be
// //   partially populated (Partial<OUTPUT>), capturing whatever information
// //   was available before the failure.
// type JournalEntry2<INPUT extends HasUUID, OUTPUT> =
//   | {
//       metadata: JournalEntryMetadata;
//       input: INPUT;
//       output: OUTPUT;
//       error?: never;
//     }
//   | {
//       metadata: JournalEntryMetadata;
//       input: INPUT;
//       output?: Partial<OUTPUT>;
//       error: ProcessorError;
//     };

type Journal<CONFIG, INPUT extends HasUUID, OUTPUT> = {
  id: UUID;
  metadata: JournalGlobalMetadata;
  config: CONFIG;
  entries: JournalEntry<INPUT, OUTPUT>[];

  // DESIGN NOTE: the transform method allows us to create the input for a
  // subsequence runner invocation by filtering and transforming journal
  // entries. This is a powerful mechanism for building complex processing
  // pipelines, where the output of one processor can be used as the input for
  // another processor. By providing a flexible transformation mechanism, we can
  // enable a wide range of use cases and allow users to customize their processing
  // pipelines in a way that best suits their needs.
  //
  // The transform method is also useful for extracting tabular representations
  // a Journal.
  transform: <RESULT extends HasUUID>(
    transformer: JournalEntryTransformer<INPUT, OUTPUT, RESULT>
  ) => Generator<RESULT>;
};

type Processor<INPUT extends HasUUID, OUTPUT> = (
  input: INPUT,
) => Promise<OUTPUT>;

// DESIGN NOTE: the factory pattern reinforced the notion that there is onee
// configuration that is used by all invokations of a processor. The intention
// is that invoking a Runner will perform one processor invokcation per input,
// and that all invocations will share the same configuration.
//
// This is a common pattern in data processing pipelines, where you have a set
// of transformations that you want to apply to a stream of data, and you want
// to be able to configure those transformations in a consistent way.
//
// The alternative would be to have some mechanism to route a configuration to
// a processor on a per-invocation basis, but that would add complexity and make
// it harder to reason about the system. By using a factory pattern, we can
// ensure that all invocations of a processor are consistent and share the same
// configuration.
type ProcessorFactory<CONFIG, INPUT extends HasUUID, OUTPUT> = (
  config: CONFIG,
) => Processor<INPUT, OUTPUT>;

type Processors<INPUT extends HasUUID, OUTPUTS extends any[]> = {
  [K in keyof OUTPUTS]: Processor<INPUT, OUTPUTS[K]>;
};

type Runner<CONFIG, INPUT extends HasUUID, OUTPUTS extends any[]> = (
  config: CONFIG,
  processors: Processors<INPUT, OUTPUTS>,
  inputs: AsyncGenerator<INPUT> | Generator<INPUT>,
) => Promise<Journal<CONFIG, INPUT, OUTPUTS>>;
