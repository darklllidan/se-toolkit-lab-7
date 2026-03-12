# Lab plan — Build Your Own Agent

**Topic:** Agent loop, LLM tool calling, CLI development, course review
**Date:** 2026-03-12

## Main goals

- Demystify the agent loop by building one from scratch.
- Reinforce understanding of all course material (labs 1-6) through a wiki-based agent and evaluation benchmark.
- Teach LLM API integration and tool calling as a transferable skill.

## Design principles

| Principle | Implication |
|-----------|-------------|
| Deterministic first, open-ended later | Task 1 has fully deterministic answers (wiki sections). Task 2 has mostly deterministic answers (static system facts). Task 3 adds open-ended chain questions. |
| Learn by debugging, not by one-shotting | Students iterate against a benchmark. They see what fails, diagnose why, fix it, re-run. |
| Specify interfaces, not implementations | We define CLI input/output format, tool schemas, eval criteria. How they build the agent is up to them. |
| Build on what exists | The agent operates on their deployed lab 5 system. No new infrastructure. |

## Feedback addressed

| Concern | Source | Resolution |
|---------|--------|------------|
| Tool use behavior depends on the model | Colleague 1 | LLM setup + tool calling verification moved to Setup. Recommend specific models known to work. |
| Weak models give inconsistent results ("pay-to-win") | Colleague 1 | Task 1 answers are deterministic (wiki sections). Model quality matters less when the answer is a fact. |
| Answers aren't deterministic or verifiable by students | Colleague 2 | Task 1: wiki section = deterministic. Task 2: static system facts = deterministic. Data queries use range checks. |
| Students will hardcode if error messages show expected answers | Colleague 2 | Show feedback hints (not exact expected values). Hidden chain-of-tool questions can't be hardcoded. LLM judge for open-ended hidden questions. |
| Tool use questions come too late in benchmark | Colleague 1 | Task 1 requires tools from the start (read_file, list_files for wiki). No "no-tools" warm-up phase. |

## Learning outcomes

By the end of this lab, students should be able to:

- [Understand] Explain how an agentic loop works: user input → LLM → tool call → execute → feed result → repeat until final answer.
- [Apply] Integrate with an LLM API using the OpenAI-compatible chat completions format with tool/function calling.
- [Apply] Implement tools that read files, list directories, and query HTTP APIs, then register them as function-calling schemas.
- [Apply] Build a CLI that accepts structured input and produces structured output (JSON).
- [Analyze] Debug agent behavior by examining tool call traces, identifying prompt issues, and fixing tool implementations.
- [Evaluate] Assess agent quality against a benchmark, iterating on prompts and tools to improve pass rate.

In simple words:

> 1. I can explain how an agent loop works — prompt, tool call, execute, feed back, repeat.
> 2. I can call an LLM API with tool definitions and handle structured responses.
> 3. I can build tools that read files, list directories, and query APIs, and wire them into an agent.
> 4. I can build a CLI that takes a question and outputs a JSON answer.
> 5. I can debug why my agent gives wrong answers by tracing tool calls and fixing prompts.
> 6. I can iterate on my agent until it passes a benchmark, improving prompts and tools along the way.

## Lab story

You have a running Learning Management Service from the previous lab — a backend, a database full of analytics data, and a frontend dashboard. Your project has a wiki full of documentation that nobody reads. You will build a CLI agent that reads the docs for you, answers questions about the course, and then connects to the live system to do something actually useful — analyze logs and diagnose bugs.

A senior engineer explains the assignment:

> 1. Build an agent that reads the project wiki and answers questions by finding the right section — the documentation agent.
> 2. Connect the agent to your live system so it can query the API and answer questions about the actual deployment — the system agent.
> 3. Polish the agent until it passes the full evaluation benchmark, including diagnosing bugs from application logs — the reliable agent.

## Required tasks

### Task 1 — The Documentation Agent

**Purpose:**

Build an agent that answers questions by navigating the project wiki, finding the relevant section, and providing the answer — learning the agentic loop, tool calling, and CLI design in the process.

**Summary:**

Students create `agent.py` in the project root. The CLI takes a question as a command-line argument and outputs JSON with three fields: `answer` (the text answer), `source` (the wiki section reference like `wiki/git-workflow.md#resolving-merge-conflicts`), and `tool_calls` (the tools used). An agent is a program that uses an LLM with tools to accomplish tasks — unlike a chatbot that just answers from its training data, an agent can read files, query APIs, and act on real information.

The agent must use `read_file` and `list_files` tools to navigate the `wiki/` directory, find the section that answers the question, and return both the answer and the source reference. Students implement the agentic loop: call the LLM with tool definitions, execute any tool calls the LLM requests, feed results back, repeat until the LLM produces a final answer.

Students choose an LLM provider (OpenRouter recommended), write a plan before coding, document their architecture in AGENT.md, and create regression tests. The benchmark tests ~15 wiki questions with deterministic expected sections — students can verify their own answers by reading the section.

**Acceptance criteria:**

- `agent.py` returns JSON with `answer`, `source`, and `tool_calls` fields.
- The agent uses `read_file` and `list_files` tools to navigate the wiki.
- The `source` field correctly identifies the wiki section that answers the question.
- The benchmark passes all wiki questions locally.
- PR is approved and merged, closing the linked issue.

---

### Task 2 — The System Agent

**Purpose:**

Connect the agent to the live system so it can query the API, inspect source code, and answer questions about the actual deployment.

**Summary:**

Students add a `query_api` tool that makes HTTP requests to the deployed backend, authenticating with `LMS_API_KEY`. The agent can now answer two kinds of questions: static system facts (framework, ports, ORM — deterministic, baked into code) and data-dependent queries (item count, scores — verified by range checks).

Students extend the system prompt to help the LLM decide when to use wiki tools vs system tools. They update documentation and tests to cover the new tool. The benchmark adds ~11 system questions on top of the existing wiki questions. Wrong answers show a feedback hint that guides students without revealing the exact expected answer.

**Acceptance criteria:**

- The `query_api` tool is implemented and authenticates with the backend.
- The agent answers static system questions correctly (framework, ports, status codes).
- The agent answers data-dependent questions with plausible values.
- The benchmark passes all wiki and system questions locally.
- PR is approved and merged, closing the linked issue.

---

### Task 3 — Pass the Benchmark

**Purpose:**

Iterate on the agent until it passes the full evaluation benchmark, including hidden questions that require chaining tools to diagnose bugs from application logs.

**Summary:**

Students run `python run_eval.py` to test against local questions, then submit to the autochecker bot which tests additional hidden questions. Hidden questions include multi-step challenges: find an error in the application logs, trace it to the source file, identify the bug, and suggest a fix. These require chaining tools (query logs → read source → reason about fix).

The backend contains 2-3 planted non-critical bugs that produce log entries. Students iterate on their agent until it can find, trace, and diagnose these issues. Common improvements include better system prompts, improved tool descriptions, and handling of multi-step reasoning. Students document their iteration process, lessons learned, and final evaluation score in AGENT.md.

**Acceptance criteria:**

- `run_eval.py` passes all local questions.
- The autochecker bot benchmark passes at least 75%.
- The agent successfully diagnoses at least one planted bug from logs.
- AGENT.md documents final architecture and lessons learned.
- PR is approved and merged, closing the linked issue.

---

## Optional task

### Task 1 — Advanced Agent Features

**Purpose:**

Extend the agent with advanced capabilities that improve reliability, expand coverage, or demonstrate deeper understanding of agent design.

**Summary:**

Students choose one or more extensions: retry logic with exponential backoff for rate-limited LLM APIs, a caching layer that avoids re-calling tools for repeated arguments, a `query_db` tool that runs read-only SQL queries against PostgreSQL directly, or multi-step reasoning where the agent plans before executing tools.

Students document their chosen extension in a plan, implement it, and write tests that demonstrate the improvement. The extension should measurably improve the agent.

**Acceptance criteria:**

- At least one extension is implemented and documented.
- Tests demonstrate the extension works correctly.
- AGENT.md is updated to describe the extension.
- PR is approved and merged, closing the linked issue.

---

## Architecture

```
Student's VM:
  agent.py (CLI) ←→ OpenRouter API (free LLM, tool calling)
       │
       ├── read_file(path)   → wiki/, source code, config
       ├── list_files(dir)   → wiki/, directories
       └── query_api(path)   → localhost:42002 (deployed backend)

Autochecker:
  SSH → python agent.py "question" → stdout JSON
  Compare answer against expected → PASS / FAIL
```

## LLM access

**Provider:** OpenRouter (free tier, zero cost).

- OpenAI-compatible API (`POST /v1/chat/completions`).
- Students create an account at openrouter.ai, get an API key (no credit card).
- LLM setup is part of the Setup task — students verify tool calling works before starting graded tasks.

**Recommended models** (free, reliable tool calling):

| Model | Context | Tool calling | Notes |
|-------|---------|-------------|-------|
| `meta-llama/llama-4-scout:free` | 512k | Strong | Best free option |
| `meta-llama/llama-3.3-70b-instruct:free` | 128k | Strong | Reliable fallback |
| `qwen/qwen-2.5-72b-instruct:free` | 128k | Good | Alternative |

**Configuration:** `.env.agent.secret` (gitignored), with `.env.agent.example` committed.

- `LLM_API_KEY` — LLM provider API key.
- `LLM_API_BASE` — OpenAI-compatible endpoint URL.
- `LLM_MODEL` — model name.

> Two distinct keys: `LMS_API_KEY` (in `.env.docker.secret`) protects the backend. `LLM_API_KEY` (in `.env.agent.secret`) authenticates with the LLM provider.

## CLI interface

**Input:**

```bash
python agent.py "How do you resolve a merge conflict?"
```

**Output:**

```json
{
  "answer": "Edit the conflicting file, choose which changes to keep, then stage and commit.",
  "source": "wiki/git-workflow.md#resolving-merge-conflicts",
  "tool_calls": [
    {"tool": "list_files", "args": {"path": "wiki"}, "result": "git-workflow.md\n..."},
    {"tool": "read_file", "args": {"path": "wiki/git-workflow.md"}, "result": "..."}
  ]
}
```

**Fields:**

- `answer` (string, required) — the agent's answer.
- `source` (string, optional) — wiki section reference. Required in Task 1, optional in Tasks 2-3.
- `tool_calls` (array, required) — tool calls made. Empty array if none.

**Rules:**

- Valid JSON, single line, to stdout.
- Debug/progress output to stderr only.
- 60-second timeout per question.
- Exit code 0 on success.
- Maximum 10 tool calls per question.

## Required tools

### `read_file`

- **Parameters:** `path` (string) — relative path from project root.
- **Returns:** file contents as string, or error message.
- **Security:** must restrict to project directory.
- **Used in:** Task 1 (wiki files), Task 2 (source code, config), Task 3 (tracing bugs).

### `list_files`

- **Parameters:** `path` (string) — relative directory path.
- **Returns:** newline-separated listing.
- **Security:** must restrict to project directory.
- **Used in:** Task 1 (discover wiki files), Task 2 (explore code structure).

### `query_api`

- **Parameters:** `method` (string), `path` (string), `body` (string, optional).
- **Returns:** JSON with `status_code` and `body`.
- **Auth:** uses `LMS_API_KEY` from `.env.docker.secret`.
- **Introduced in:** Task 2.

## Question classes

### Class A: Wiki lookup (Task 1)

Questions about course material. The answer lives in a wiki section.

```yaml
- index: 0
  class: A
  task: 1
  question: "How do you resolve a merge conflict?"
  expected_source: {any_of: ["wiki/git-workflow.md#resolving-merge-conflicts",
                              "wiki/git-workflow.md#merge-conflicts"]}
  expected_answer: {any_of: ["edit", "resolve", "choose", "stage"]}
  check_tools: [read_file]
```

**Checking:**

| Field | Check | Required |
|-------|-------|----------|
| `source` | Matches `expected_source` (exact or `any_of`) | Yes |
| `answer` | Contains keywords from `expected_answer` | Optional |
| `tool_calls` | Includes tools from `check_tools` | Yes |

**Why deterministic:** The correct section is a fact. Students verify by reading the section.

**Count:** ~15 in `run_eval.py`, ~5 hidden.

### Class B: Static system facts (Task 2)

Questions where the answer is baked into the code/config and never changes.

```yaml
- index: 16
  class: B
  task: 2
  question: "What HTTP status code does the API return when you request /items/ without authentication?"
  expected: {any_of: ["401", "403"]}
  feedback: "Try making a request without the API key header and check the response status code."
  check_tools: [query_api]
```

**Checking:**

| Field | Check | Required |
|-------|-------|----------|
| `answer` | Matches `expected` (contains, any_of, regex) | Yes |
| `tool_calls` | Includes tools from `check_tools` | Yes |

**On failure:** Show `feedback` (a hint toward the right approach), not the `expected` value.

**Count:** ~8 in `run_eval.py`, ~3 hidden.

### Class C: Data-dependent system queries (Task 2)

Questions about live data. Answer varies per student.

```yaml
- index: 24
  class: C
  task: 2
  question: "How many items are currently in the database?"
  expected: {numeric_gt: 0}
  feedback: "Query the /items/ endpoint with authentication and count the results."
  check_tools: [query_api]
```

**Checking:**

| Field | Check | Required |
|-------|-------|----------|
| `answer` | Matches `expected` (numeric_gt, numeric_range) | Yes |
| `tool_calls` | Includes tools from `check_tools` | Yes |

**On failure:** Show `feedback`.

**Count:** ~3 in `run_eval.py`, ~2 hidden.

### Class D: Log analysis chain (Task 3, hidden only)

Multi-step questions. Planted bugs produce log errors the agent must find, trace, and diagnose.

```yaml
- index: 30
  class: D
  task: 3
  bot_only: true
  question: "Check the application logs for errors. What is causing the most recent error and which file is it in?"
  expected_bug: {contains: "ZeroDivisionError"}
  expected_location: {contains: "analytics.py"}
  expected_fix: {any_of: ["check", "empty", "zero", "len", "guard"]}
  feedback: "Read the error traceback in the logs. Which file and line number caused it?"
  bug_location: "backend/app/routers/analytics.py"
  check_tools: [query_api, read_file]
```

**Checking:**

| Field | Check | Required |
|-------|-------|----------|
| `answer` | Contains bug identifier (`expected_bug`) | Yes |
| `answer` | Contains source file (`expected_location`) | Yes |
| `answer` | Contains fix keyword (`expected_fix`) | Optional |
| `tool_calls` | Includes all tools from `check_tools` (chain) | Yes |

**On failure:** Show `feedback` (points to where to look, not the answer). The `bug_location` field tells the autochecker where the bug is for logging purposes but is not shown to the student.

**Count:** 3-5 hidden (bot eval only).

### Class E: LLM-judged reasoning (Task 3, hidden only)

Open-ended questions where keyword matching isn't sufficient.

```yaml
- index: 35
  class: E
  task: 3
  bot_only: true
  question: "Compare how the ETL pipeline handles failures vs how the API endpoints handle failures. Which is more robust and why?"
  rubric: "Answer must: (1) describe ETL error handling, (2) describe API error handling, (3) compare them, (4) give a reasoned judgment."
  feedback: "Read both the ETL code and the API router code, then compare their error handling strategies."
  check_tools: [read_file]
```

**Checking:**

| Field | Check | Required |
|-------|-------|----------|
| `answer` | LLM judge evaluates against `rubric` | Yes |
| `tool_calls` | Includes tools from `check_tools` | Yes |

**Budget:** ~5 questions × ~$0.01/judge call = ~$0.05/student. ~$3 for 60 students. Use a cheap fast model (Haiku/Flash) as judge.

**Count:** 3-5 hidden (bot eval only).

### Summary: questions per task

| Class | Task | `run_eval.py` | Bot-only | Checking | On failure |
|-------|------|--------------|----------|----------|------------|
| A: Wiki lookup | 1 | ~15 | ~5 | Source path match + tool use | Show expected source |
| B: Static system facts | 2 | ~8 | ~3 | Keyword match + tool use | Show `feedback` hint |
| C: Data-dependent queries | 2 | ~3 | ~2 | Numeric range + tool use | Show `feedback` hint |
| D: Log analysis chain | 3 | 0 | 3-5 | Bug ID + location + tool chain | Show `feedback` hint |
| E: LLM-judged reasoning | 3 | 0 | 3-5 | LLM judge + tool use | Show `feedback` hint |
| **Total** | | **~26** | **~13-17** | | |

## Evaluation system

### Two paths

| | Local (`run_eval.py`) | Bot (autochecker SSH) |
|--|----------------------|----------------------|
| Triggered by | Student runs locally | `/check` in Telegram |
| Questions | ~26 (from API) | ~26 + ~13-17 hidden |
| Where agent runs | Student's machine | Student's VM (via SSH) |
| Display | Green pass, stop at first fail | Same |
| On failure shows | `feedback` hint (not expected value) | Same |
| Purpose | Fast iteration | Grading |

### Anti-gaming

- Task 1 answers are deterministic wiki sections — hardcoding requires the wiki files.
- Failure feedback shows hints, not expected values (Classes B-E).
- Hidden questions include multi-tool chains that can't be hardcoded.
- LLM judge for open-ended hidden questions.
- Tool call verification ensures the agent actually used tools.
- Every API request is logged.

### `run_eval.py`

```bash
python run_eval.py           # all questions, stop at first fail
python run_eval.py --index 5 # single question (for debugging)
```

## Wiki requirements

Task 1 depends on a comprehensive wiki covering labs 1-6.

| Topic | Lab | Wiki file |
|-------|-----|-----------|
| Git workflow, branching, PRs | 1 | `wiki/git-workflow.md` |
| Backend basics, FastAPI | 2 | `wiki/backend.md` |
| Docker, Compose, volumes | 2 | `wiki/docker.md` |
| REST API, HTTP methods | 3 | `wiki/rest-api.md` |
| Database, SQL, ORM | 3 | `wiki/database.md` |
| Authentication, security | 3 | `wiki/security.md` |
| Testing, pytest | 4 | `wiki/testing.md` |
| Frontend, React | 4 | `wiki/frontend.md` |
| ETL, data pipelines | 5 | `wiki/etl.md` |
| Analytics, SQL aggregation | 5 | `wiki/analytics.md` |
| Agents, tool calling | 6 | `wiki/agents.md` |

**Action needed:** Audit existing wiki, identify gaps, write missing sections.

## Planted bugs (Task 3)

Non-critical bugs in the backend that produce log entries but do not break functionality.

| # | Bug | File | Log output | Trigger |
|---|-----|------|-----------|---------|
| 1 | Division by zero on empty group | `analytics.py` | `ZeroDivisionError` caught, logged | GET `/analytics/scores?group=empty-group` |
| 2 | Unclosed resource in ETL edge case | `etl.py` | `ResourceWarning` logged | POST `/pipeline/sync` with empty response |
| 3 | Config type mismatch (string timeout) | `config.py` | `TypeError` caught, logged | Any request after startup |

Requirements:

- Must not break existing lab 5 functionality or autochecker checks.
- Must produce visible log entries the agent can find.
- Must be diagnosable by reading the source code.
- Must have clear fixes the agent can suggest.

## Decisions

| # | Decision |
|---|----------|
| 1 | No starter `agent.py` skeleton — students build from scratch, plan first. |
| 2 | LLM setup in Setup task — verify tool calling before graded work. |
| 3 | Recommend strong free models first (Llama 4 Scout, Llama 3.3 70B, Qwen 2.5 72B). |
| 4 | Task 1 uses wiki lookup — deterministic, verifiable, teaches tools from day one. |
| 5 | Task 1 output: answer + source — source is deterministic, answer shows understanding. |
| 6 | Tool call verification is loose — check tool was used, not exact args. |
| 7 | Max 10 tool calls per question. |
| 8 | Static facts (deterministic) + range checks for data-dependent questions. |
| 9 | Failure feedback shows hints, not expected values (Classes B-E). |
| 10 | Hidden chain-of-tool questions + LLM judge prevent hardcoding. |
| 11 | Plain string input (`python agent.py "..."`). |
| 12 | `LMS_API_KEY` (backend) vs `LLM_API_KEY` (LLM provider). |
| 13 | `.env.agent.secret` for LLM config (gitignored). |
| 14 | 2-3 planted non-critical bugs producing log entries for Task 3. |
| 15 | LLM judge budget: ~$3 total for 60 students. |
| 16 | `run_eval.py` supports `--index N` for single-question debugging. |

## Remaining work

- [ ] Audit existing wiki content — what's there, what's missing.
- [ ] Write missing wiki sections (labs 1-6 material).
- [ ] Rewrite Task 1 (`task-1.md`) — documentation agent.
- [ ] Rewrite Task 2 (`task-2.md`) — system agent.
- [ ] Rewrite Task 3 (`task-3.md`) — pass the benchmark with planted bugs.
- [ ] Update setup task — add LLM setup and verification script.
- [ ] Create verification script (`verify_llm.py`).
- [ ] Write Class A questions (wiki lookup, ~20).
- [ ] Write Class B questions (static system facts, ~11).
- [ ] Write Class C questions (data-dependent queries, ~5).
- [ ] Write Class D questions (log analysis chains, ~5).
- [ ] Write Class E questions (LLM-judged reasoning, ~5).
- [ ] Implement planted bugs in backend.
- [ ] Add `source_match` checking to `run_eval.py` and engine.
- [ ] Add `tool_chain` checking to engine.
- [ ] Add `llm_judge` checking to engine (with budget control).
- [ ] Update autochecker spec (`lab-06.yaml`).
- [ ] Update `run_eval.py` with `--index` flag and feedback display.
- [ ] Update README to match v2 design.
- [ ] Update optional task file.
