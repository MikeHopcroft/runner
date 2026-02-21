# Questions

### Scale and robustness targets for the runner.

### Should we consider batch APIs?

### Should uuids be content hashes or UUID v4 values? If content hashes, how do we indicate which fields participate in the hashing?

### Should a workflow be a first class concept of `runner` vs it's just something the user implements in the `process()` function they supply?

- If it was a core concept, what services or values would `runner` provide?

### Should the `runner` provide an abstraction that unifies the view of models with diffent APIs, or is the `runner` mainly concerned with ensuring test-case level tasks are run, and the implementation should use the SDK for the model they want?

- The abstraction allows one to easily matrix runs across models from different vendors that use different SDKs, but can be configured to the same semantics. Can reference by name, not implementation.

### If a runlog/journal can now be ammended over multiple runs to fill in data about missing runs (network errors, transient server errors, etc.), what does a runlog id correspond to?

- Original invocation build list of all expected records.
- Subseuent runs generate missing processed records.
- How do we edit the file?
  - Don't - just transact on in-memory data structure
  - Create an appendable file format that has two sections: a sealed list of cases and an appendable list of case results.
- Rename file once complete?
- Dealing with multiple writers/appenders. Don't want duplicate records - or can filter dupes out later.