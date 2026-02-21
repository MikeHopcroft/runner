# Goals

Gotaglio is a set of composable building blocks and tools designed to reduce the time and friction in the Data Science inner loop. It minimizes the time to the first experiement and for each subsequent turn of the crank, while providing the foundation for a methodology that journals all experimental results to allow insights into root causes and provide the ability to reliably repeat historical experiments with updated configurations.

* Minimize time and friction to first data science experiment.
* Minimize time and friction for each subsequent turn of the crank.
* Repeatable experimental results.
* Rerun historical experiment with different configuration.
  * Rebaseline because of system evolution in order to see progress over time.
  * Try out new model, prompt, agent, etc.
* Provide diagnostic journalling that drives insights.
* Robust experiment running
  * Maximizes concurrency to reduce wall-clock time
  * Retries on transient errors
  * Respects rate limits
* Track progress over time
* Compare results across variants
* Composable building blocks for
  * Model and agent inference
  * Providing tools for use by models and agents
  * Computing and storing embeddings
  * Evaluation (including LLM as judge)
  * Data Cleaning and Enrichment
  * Data Analysis
  * Human labelling
  * Interactive grounding data explorer
  * Case storage/persistence
  * Reducing common mistakes (e.g. around utf-8 handling, schema validation, leaked secrets)
* All functionality seamlessly integrated with Jupyter notebooks.
* All functionality accessible via scriptable CLI.
* All functionality accessible via Python module.
* Lightweight installation.
* Runs equally well on workstation and in cloud.
* Runs equally well on Linux, OSX, and Windows.
* Support for containers-based development and GitHub code spaces.
* Authentication via key and OAuth. Secrets management.
