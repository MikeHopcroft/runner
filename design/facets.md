# Facets

## High concurrancy for large suites
- multi-dimensional rate limiting (e.g. calls, tokens)
- connection pooling

## Robust completion for large suites
- Ability to restart to retry generation of missing results
- Ability to detect that a run is complete, with no missing results
- backoff and retry

## Explicit Error Handling

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

## Convenience Functions
These might be stable enough to go in a `runner.core` module that is shared by all of the `runner` variants.
- Handling unicode correctly for file operations
- File readers and writers with schema validation
- File locators
