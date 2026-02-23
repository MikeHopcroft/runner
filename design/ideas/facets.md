# Facets

## High concurrancy for large suites
- multi-dimensional rate limiting (e.g. calls, tokens)
- connection pooling

## Robust completion for large suites
- Ability to restart to retry generation of missing results
- Ability to detect that a run is complete, with no missing results
- backoff and retry

## Explicit Error Handling
- some errors are really part of the `journal`, rather than the log. For instance
  - LLM was supposed to produce JSON, but it made something else and the evaluator parser raised an error.
  - Correct LLM result surfaced a bug in the evaluator.

## Logging

## Multi-Modal (text, audio, images, video, data)

## Local tool development

## Fast Inner Loop
- No cloud deployment necessary for changes to logic.
- No container build necessary for changes to logic.
- Tools run locally
  - Can attach debugger
  - Can rapidy restart with bugfixes, changes to data, changes to configuration, etc.

## Configuration

## Repeatability

## Ease of Designing and Implementing New Experiments

## Clear Line Separating Runner Responsibilties from Experiment

## Structured Experiment File Algebra
Some options. A ==> A' where
* A' is just A, annotated with some new fields. This option is simple, but it bakes the workflow into the schema for A'. If you want to do a different workflow, you need a different A'. Formatters and analyzers are specialed to A'.
* A' is a container like a tuple or dict that contains the input, A, and and output, B.
* A' is the output, but it has a field that contains a reference to input A.
* Two lists - immutable, sealed list of inputs. Immutable, but appendable list of outputs.
* Do we rename and rewrite file once finished

## Convenience Functions
These might be stable enough to go in a `runner.core` module that is shared by all of the `runner` variants.
- Handling unicode correctly for file operations
- File readers and writers with schema validation
- File locators
