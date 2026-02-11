# Runner

Runner is an experimental suite of tools for accelerating the applied science inner loop during the early stages of developing ML systems.

## Goals/Princples
- Ability to prototype, demo, and refine a simple idea in 20 minutes while participating in a design/ideation workshop.
- Cost/friction of creating an experiment is very low.
- Friction for installing tool chain is very low.

## Release Philosoophy

`Runner` is experimental software targeting the leading edge of a rapidly moving frontier.
For this reason, much of the development for `runner` is also experimental and involves breaking changes and adding and removing functionality.

To avoid being pinned to a single point in history, `runner` consists of a series of overlapping toolsets, each of which targeted the frontier at a particular point in time. In general, we will develop and refine one of these toolsets in the context of a real set of applied science problem we're working on. At some point,  frontier technologies will have changed enough that the cost of retrofitting the existing toolset and fixing code the depends on it will be too high and we will freeze the current toolset and start another one, from scracth, although heavily borrowing and cherry picking code and concepts from earlier versions.

To disambiguate the progression of `runner` toolsets from release versions, we assign toolsets names like `runner red` or `runner blue` or `runner green`. Think of these as completely independent toolsets that draw inspiration from each other. Our expectation is the in general, all but one of the `runner` toolsets will be frozen. It is possible that we simultaneously develop two `runner` variants simultaneosly for very differnt domains (e.g. chatbots vs computational fluid dynamics vs sensor fusion).

The intention of each `runner` varient is to be a small, clean, parsimoneous set of tools that target a particular set of applied science scenarios at a point in time.

Our expectation is that a `runner` variant will have a lifetime from start of development until freeze of about six months.

Here are some examples of rapidly shifting trends in LLM systems over the past three years
- completions-style API
- API key authentication
- custom orchestrators
- RAG systems that use two chained LLMs, one to generate a grounding query, and one to summarize results
- responses-style API
- structured output
- OAuth authentication
- support for tools
- concepts like MCP
- reasoning models
- agents
- availability of markets like Azure Foundry
- multi agent systems
- multi modal (e.g. text, voice, image, video)

### Rover is Not
Rover is not
- a kitchen sink, a jack-of-all-trades, a set of all tools for all people
- maintained
- a heavyweight install with unstable or unreliable or non-performant dependencies