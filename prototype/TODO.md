# TODO List

- [ ] Design for mock models - perfect, flakey, 
- [ ] End-to-end samples
  - [ ] Single turn LLM + templated prompt
  - [ ] Single turn eval
  - [ ] Multi turn LLM + templated prompt
- [ ] Built-in pipelines
  - [ ] Single turn LLM + templated prompt + tools
  - [ ] Single turn agent + templated prompt + tools
- [ ] Figure out config Prompt feature
- [ ] Determine whether generic type composition works with Pydantic
- [x] Design for passed_predicate
- [x] Design for formatter
  - [x] Option: provide journal formatter
  - [x] Option: provide entry formatter
  - [x] Option: use default formatters
  - Details
    - [ ] Rich console setup for Markdown, console
    - [ ] Config diff summary
    - [ ] For-loop over cases
    - [ ] Case Summary
    - [ ] Before case
    - [ ] Body of case
      - [ ] For loop over turns
    - [ ] After Case
- [ ] Design for summarizer
  - [x] Option: Provide list of columnspecs for use with default formatter.
  - [x] Option: Provide function
  - [x] UUID shortener for id_column()
  - [ ] Solution for summarizing multi-turn scenarios.
    - Currently summarizer iterates over Journal entries. Want to somehow
      provide turns as rows in output.
- [ ] Design for compare


## Dimensions

- Dimensions
  - Single vs multi turn
  - Templated vs static prompt
  - LLM vs Agent vs Embedding
  - Tool vs none
