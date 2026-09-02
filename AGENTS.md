# AGENTS.md — Agente Investigador

## Project Overview

Backend FastAPI that turns a plain-text query into an academic report by orchestrating a multi-agent pipeline built on **Google ADK** (`SequentialAgent`: Investigador → Editor). Designed as Clean Architecture MVP. All user-facing strings, prompts, comments and logs are in **Spanish**.

## Tech Stack

| Layer | Tech |
|---|---|
| Runtime | Python 3.13 (no pinning; only `requirements.txt`) |
| API | FastAPI + Uvicorn (ASGI) |
| Agents | `google-adk` (`LlmAgent`, `SequentialAgent`, `Runner`) |
| LLM | Gemini via `google-genai`; model chosen with env `IA_MODEL` |
| Config | `pydantic-settings` (reads `.env`) |
| Other | `python-dotenv`, PyYAML (prompts) |

**Critical**: `requirements.txt` lists only `google-adk`, `fastapi`, `uvicorn`, `python-dotenv`. Directly-used packages `google-genai`, `PyYAML`, `pydantic` arrive transitively via `google-adk`. **`pydantic-settings` is imported in `app/core/config.py` but is NOT in `requirements.txt` nor a declared dep of `google-adk`** — in a clean venv, `pip install -r requirements.txt` may not install it.

## Architecture

Clean Architecture layered as: `api → application → services/agents → domain → infrastructure`.

```
app/api/v1/                        HTTP entry (FastAPI routers)
app/application/research/          Use cases + orchestration (agent_runner, run_investigation)
app/services/agents/               ADK layer: agent builders, tools, YAML prompts
app/domain/research/               Pure models + repository abstraction (no external deps)
app/infrastructure/repositories/   Implementations (in-memory, tracing)
```

- Routes registered in `app/main.py:15-16` under `/api/v1`.
- **Async request → poll**: `POST /api/v1/chat` returns `202 ACCEPTED`; work runs in FastAPI `BackgroundTasks`; client polls `GET /api/v1/status/{session_id}`. No WebSocket/SSE.
- **Multi-agent pipeline**: `SequentialAgent` runs Investigador → Editor. Investigator owns `google_search` tool; Editor has none. Output flows via `output_key`: `investigacion_resultado` → `reporte_final`.
- **Prompts in YAML**: agent behavior lives in `app/services/agents/prompts/*.yaml`, not in Python. Edit those files to change agent personality.
- **Tracing**: `AgentTracer` (`app/infrastructure/repositories/observability/tracing.py`) maps ADK events to structured logs + `last_step` progress. Passed as `tracer` in run calls.
- **Repository pattern**: `ResearchSessionRepository` ABC (`app/domain/research/repository_base.py`); only impl is `InMemorySessionRepository`. Singleton `session_repository` in `app/infrastructure/repositories/memory/session_repository.py`.

## Directory Structure

Only files that matter for working on the project:

```
app/main.py                          App factory, router registration
app/core/config.py                   Settings (env-driven) — gotcha: google_api_key x2
app/core/logging.py                  get_logger() → structured JSON logs
app/core/security.py                 EMPTY placeholder — no auth
app/api/v1/chat.py                   POST /chat (202 + BackgroundTasks)
app/api/v1/status.py                 GET /status/{session_id}
app/schemas/chat_request.py          Pydantic request/response models
app/application/research/run_investigation.py   Use case: session lifecycle
app/application/research/get_history.py         EMPTY placeholder
app/application/research/services/agent_runner.py  ADK Runner event loop
app/application/research/services/history_manager.py EMPTY placeholder
app/domain/research/models.py        ResearchSession, ResearchStatus, ResearchReport
app/domain/research/repository_base.py           ABC for session repo
app/domain/research/entities.py      EMPTY placeholder
app/services/agents/team.py          build_research_team() → SequentialAgent
app/services/agents/investigator.py  build_investigator() → LlmAgent + google_search
app/services/agents/editor.py        build_editor() → LlmAgent (no tools)
app/services/agents/prompts/*.yaml   Agent instructions & output format
app/services/agents/tools/search/search_web.py   google_search tool
app/services/agents/tools/export/export_pdf.py   EMPTY placeholder
app/services/agents/tools/utils/format_text.py    UNUSED helpers (clean/extract json)
app/infrastructure/repositories/memory/session_repository.py  Dict-backed repo
app/infrastructure/repositories/observability/tracing.py     AgentTracer
app/infrastructure/repositories/firestore/chat_repository.py EMPTY placeholder
app/models/database_models.py        EMPTY placeholder
scripts/test_team.py                 Manual end-to-end team smoke test
scripts/test_gemini.py               Manual Gemini connection test
scripts/test_models.py               Manual model listing test
```

## Development Workflow

```bash
pip install -r requirements.txt
cp .env.example .env   # fill GOOGLE_API_KEY, IA_MODEL, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
uvicorn app.main:app --reload
```

The app requires a valid `.env`. Agent builders read `IA_MODEL` via `os.getenv` (not through `Settings`). `GOOGLE_API_KEY` is required by `google-genai` and ADK's `google_search`.

## Commands

Verified commands (no test/lint/format/typecheck/build tooling exists — do not invent any):

| Action | Command |
|---|---|
| Install deps | `pip install -r requirements.txt` |
| Run server | `uvicorn app.main:app --reload` |
| Team end-to-end smoke test | `python -m scripts.test_team` |
| Gemini connection smoke test | `python -m scripts.test_gemini` |
| List available models | `python -m scripts.test_models` |
| Verify app imports | `python -c "import app.main"` |

There is **no** test framework, linter, formatter, type checker, build step, or CI configured.

## Coding Conventions

- **Language**: Spanish for comments, docstrings, log messages, prompts and user-facing strings.
- **Async-first**: endpoints, repository methods, and run functions are `async def`. Blocking work goes in `BackgroundTasks`.
- **Structured logging**: obtain loggers via `get_logger("<hierarchical.module.name>")` from `app.core.logging`; attach context via `extra={"session_id": ..., "agent": ..., "step": ..., "tool": ...}`.
- **Agent factory pattern**: each agent is built by a `build_*()` function that loads its prompt from YAML. Keep this pattern when adding agents.
- **Type hints** throughout; Pydantic `BaseModel` for schemas/domain models; `Enum` for statuses.
- **Repository abstraction**: data access goes through the `ResearchSessionRepository` ABC; implementations live in `app/infrastructure/repositories/`.
- **Error handling** currently uses bare `except Exception` — keep that consistent unless explicitly asked to improve granularity.

## Architecture Rules

- Keep dependency direction `api → application → services/agents → domain → infrastructure`. `domain/` must stay pure (no ADK/HTTP/DB imports).
- Agent behavior must stay in YAML prompts, not inline Python.
- When wiring new sub-agents into the `SequentialAgent`, connect them via `output_key` (in → next agent's context).
- Always thread the `AgentTracer` through run calls and use the `on_progress` callback to persist session progress.
- New storage backends must implement `ResearchSessionRepository` and swap the singleton in `session_repository`.
- Do not change the async request → poll contract without a stated reason (no WebSocket/SSE).

## Testing

No automated tests and no test framework exist. The only verification is the manual smoke scripts in `scripts/` (run via `python -m scripts.<name>`), which require a valid `GOOGLE_API_KEY`. After changes, at minimum run `python -c "import app.main"` and the relevant smoke script, and note that module-level singletons (`session_repository`, `_session_service`) share state between runs — if you add tests, they must reset this state.

## External Services

- **Gemini API** (`google-genai`): requires `GOOGLE_API_KEY`. Used indirectly by ADK agents and directly by the `scripts/test_*.py`.
- **Google Search** (ADK built-in `google_search`): the only external data source. Without it the investigator is blind.
- **Vertex AI**: `GOOGLE_GENAI_USE_VERTEXAI`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` exist in config/.env.example, but nothing in code uses Vertex — scripts and ADK use the API key directly.
- **Cloud Logging**: structured JSON logs are formatted for it (`StructuredFormatter`), but no exporter is wired.
- **No database**: all state is in a `Dict`; `DB_BACKEND` setting defaults to `"firestore"` but no Firestore code is implemented (placeholder only).

## Important Constraints

- **No authentication** on any endpoint. Do not add auth without explicit instruction.
- The **8 empty placeholder files** (`entities.py`, `get_history.py`, `history_manager.py`, `security.py`, `database_models.py`, `export_pdf.py`, `firestore/chat_repository.py`, `observability/logger.py`) signal unimplemented features. Don't delete them without checking intent.
- `user_id="api-user"` is hardcoded in `agent_runner.py`. Multi-user support would require extracting this.
- `tools/utils/format_text.py` (`clean_llm_output`, `extract_json_from_text`) and `AgentTracer.on_thought`/`on_error` exist but are not called anywhere — reuse them before writing duplicates, don't treat them as dead by design.

## Known Gotchas

- **`google_api_key` declared twice** in `app/core/config.py:9` and `:13`. The second overrides the first; only line 13 matters at runtime. Remove line 9 if you edit this file.
- **`requirements.txt` is a stub**: directly-used packages (`pydantic-settings`, and transitively `google-genai`, `PyYAML`, `pydantic`) are not pinned. A fresh `pip install -r requirements.txt` may lack `pydantic-settings`.
- **Singleton globals**: `session_repository` and `_session_service` are module-level singletons. Tests/share state unless explicitly reset.
- **No real DB**: `InMemorySessionRepository` stores a `Dict`; all state is lost on restart.
- Agents read `IA_MODEL` via `os.getenv` in `investigator.py`/`editor.py`, bypassing `Settings` — model config lives in the env var, not in `Settings`.
- `pydantic-settings` `Settings.Config` block (legacy style) is used instead of `model_config`; pydantic v2 still supports it but it's deprecated.

## Security

- `.env` is gitignored and contains `GOOGLE_API_KEY`. Never commit `.env` or any secret; never log full API keys or large LLM outputs (`tracing.py` truncates previews to 200 chars — keep that behavior).
- `.gitignore` also excludes credentials/service-account files (`credentials.json`, `service-account-file.json`).
- Endpoints are unauthenticated by design at this stage — do not weaken or add auth without instruction.

## Current State

Early-stage MVP. No tests, no DB (in-memory only), no auth, no CI, no lint/format/typecheck. Most `except` clauses are bare `except Exception`. Before production use: add a real database (Firestore is the intended backend per `db_backend` setting), automated tests, and auth. The report is returned as raw markdown string; the structured `ResearchReport` domain model exists but is not produced yet.

## Agent Workflow

- Inspect the relevant code before modifying; prefer the existing abstractions (repository ABC, factory builders, YAML prompts, `get_logger`).
- Do not introduce new dependencies without justification — especially anything already available transitively.
- Do not change the architecture (layering, request→poll contract, output_key linking) without a clear reason.
- After changes, run `python -c "import app.main"` and the relevant `scripts/` smoke test; reset module-level singletons if you touch state.
- Never modify `.env` or expose secrets; never commit `AGENTS.md`-adjacent secrets.
- Don't delete apparently-unused code (placeholders, `format_text.py`, `on_thought`/`on_error`) without verifying intent first.
