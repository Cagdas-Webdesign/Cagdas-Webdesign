<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero-light.svg" width="720" alt="Çağdaş Uçar — Full-Stack Development · Python Backends · AI/RAG Systems">
</picture>
</p>

<p align="center">
  <a href="https://cagdas-webdesign.github.io/portfolio/"><b>Live Portfolio</b></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/Cagdas-Webdesign/portfolio-rag-backend"><b>RAG Backend</b></a>
  &nbsp;·&nbsp;
  <a href="mailto:ucarcagdas18@gmail.com"><b>ucarcagdas18@gmail.com</b></a>
</p>

I build complete web applications — the interface, the Python backend and the language models
behind it. My focus is AI systems that can be checked: answers grounded in real sources, failures
handled explicitly, and quality measured by tests and evaluation rather than asserted.

<p align="center">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/proof-tests-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/proof-tests-light.svg"><img src="assets/proof-tests-light.svg" width="256" alt="2,855 passing tests, as documented for portfolio-rag-backend v1.3.0."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/proof-acceptance-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/proof-acceptance-light.svg"><img src="assets/proof-acceptance-light.svg" width="256" alt="24 of 24 evaluation questions passed in the live release acceptance of v1.2.0 (tag v1.2.0-accepted). This is not a result for v1.3.0."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/proof-adrs-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/proof-adrs-light.svg"><img src="assets/proof-adrs-light.svg" width="256" alt="8 architecture decision records in docs/adr of portfolio-rag-backend."></picture>
</p>

<p align="center"><sub>
Test count from the backend <a href="https://github.com/Cagdas-Webdesign/portfolio-rag-backend#evaluation-and-testing">README</a> (v1.3.0) ·
24/24 from the <a href="https://github.com/Cagdas-Webdesign/portfolio/blob/main/public/evaluation/final-acceptance-v1.2.0.md">v1.2.0 acceptance report</a>, not yet repeated for v1.3.0 ·
<a href="https://github.com/Cagdas-Webdesign/portfolio-rag-backend/tree/main/docs/adr">ADRs</a>.<br>
Tests and evaluation document behaviour; they do not guarantee production reliability.
</sub></p>

---

## Portfolio RAG Backend

**Flagship project** · Python 3.13 · FastAPI · v1.3.0 in production on Google Cloud Run

[Repository](https://github.com/Cagdas-Webdesign/portfolio-rag-backend) ·
[Architecture](https://github.com/Cagdas-Webdesign/portfolio-rag-backend/blob/main/docs/ARCHITECTURE.md) ·
[Evaluation](https://github.com/Cagdas-Webdesign/portfolio-rag-backend/blob/main/evaluation/README.md) ·
[Security](https://github.com/Cagdas-Webdesign/portfolio-rag-backend/blob/main/docs/SECURITY.md)

A portfolio assistant must never invent a skill or a project — that would be a false statement
about a real person. This backend answers only from a reviewed knowledge base, verifies every answer
against the passages it cites, and says so when it does not know. The RAG pipeline is written in the
repository instead of an orchestration framework such as LangChain: chunking, retrieval, grounding
and citations decide answer quality, so they are kept small enough to measure and change on purpose.

### How a question is answered

**React portfolio → Cloudflare Worker** (Turnstile, rate limits) **→ FastAPI on Google Cloud Run**,
then six steps inside the backend:

<p align="center">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/query-1-embed-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/query-1-embed-light.svg"><img src="assets/query-1-embed-light.svg" width="256" alt="Query flow, step 1 of 6: Embed the query. Normalized question → vector same model as the corpus. Provider or property: Mistral · mistral-embed."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/query-2-retrieve-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/query-2-retrieve-light.svg"><img src="assets/query-2-retrieve-light.svg" width="256" alt="Query flow, step 2 of 6: Retrieve evidence. Top-k 7, public by construction No match → fixed reply, no LLM. Provider or property: Cloudflare Vectorize."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/query-3-context-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/query-3-context-light.svg"><img src="assets/query-3-context-light.svg" width="256" alt="Query flow, step 3 of 6: Build context. IDs → text from bundled corpus Ranked, deduped, token-bounded. Provider or property: in-process · no provider."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/query-4-generate-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/query-4-generate-light.svg"><img src="assets/query-4-generate-light.svg" width="256" alt="Query flow, step 4 of 6: Generate answer. From retrieved passages only Instructions stay system-only. Provider or property: Workers AI · gpt-oss-120b."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/query-5-verify-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/query-5-verify-light.svg"><img src="assets/query-5-verify-light.svg" width="256" alt="Query flow, step 5 of 6: Verify grounding. Checks answer vs cited passages default: the generator itself. Provider or property: optional: Groq gpt-oss-20b."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/query-6-cite-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/query-6-cite-light.svg"><img src="assets/query-6-cite-light.svg" width="256" alt="Query flow, step 6 of 6: Publish citations. Only sources retrieved for this request are returned. Provider or property: backend-owned · verified."></picture>
</p>

The answer and its citations return through the Worker with an `X-Request-ID`.

### How knowledge is indexed

Offline, from the CLI (`portfolio-rag knowledge index`) — never inside a request. The corpus also
ships in the container image, so retrieved IDs resolve back to text locally.

<p align="center">
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ingest-1-author-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/ingest-1-author-light.svg"><img src="assets/ingest-1-author-light.svg" width="256" alt="Offline indexing, step 1 of 6: Author knowledge. Markdown + YAML frontmatter versioned, reviewed in git. Provider or property: knowledge/*.md."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ingest-2-validate-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/ingest-2-validate-light.svg"><img src="assets/ingest-2-validate-light.svg" width="256" alt="Offline indexing, step 2 of 6: Validate. Schema version and metadata visibility: public | internal. Provider or property: strict · reports all errors."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ingest-3-chunk-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/ingest-3-chunk-light.svg"><img src="assets/ingest-3-chunk-light.svg" width="256" alt="Offline indexing, step 3 of 6: Chunk. Structure-aware, deterministic SHA-256 fingerprint per chunk. Provider or property: no model in the loop."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ingest-4-plan-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/ingest-4-plan-light.svg"><img src="assets/ingest-4-plan-light.svg" width="256" alt="Offline indexing, step 4 of 6: Plan changes. Create / re-embed / delete unchanged chunks cost nothing. Provider or property: incremental · dry-run."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ingest-5-embed-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/ingest-5-embed-light.svg"><img src="assets/ingest-5-embed-light.svg" width="256" alt="Offline indexing, step 5 of 6: Embed. Title + heading path + text versioned embedding space. Provider or property: Mistral · mistral-embed."></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ingest-6-index-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/ingest-6-index-light.svg"><img src="assets/ingest-6-index-light.svg" width="256" alt="Offline indexing, step 6 of 6: Index. Vectors and metadata, no text upserts first, then deletes. Provider or property: Cloudflare Vectorize."></picture>
</p>

### What the code demonstrates

- **Ports and adapters** — every model and store sits behind an interface; one composition module
  turns configuration into providers, so swapping one is a config change, not a refactor.
- **Controlled unknowns** — no evidence above the similarity threshold means a fixed answer, an
  empty citation list and no language-model call.
- **Security boundaries** — public-only retrieval is part of the query, retrieved text cannot become
  an instruction, requests that bypass the edge gateway are refused, and questions and answers are
  never logged. Prompt injection is documented as a residual risk, not declared solved.
- **Quality gates** — Ruff, mypy `strict`, pytest and a Docker smoke test run in
  [CI](https://github.com/Cagdas-Webdesign/portfolio-rag-backend/blob/main/.github/workflows/ci.yml)
  on every push; CI also asserts that a production container refuses to start with development
  stand-ins.
- **Measured retrieval** — in the v1.2.0 acceptance: hit@1 75 %, hit@5 90 %, MRR 0.817 on 20
  answerable questions, with every failing question listed by name.

---

## Interactive React Portfolio

**Frontend counterpart** · React 19 · JavaScript · Vite 8

[Live site](https://cagdas-webdesign.github.io/portfolio/) ·
[Repository](https://github.com/Cagdas-Webdesign/portfolio)

The user interface of the RAG system, and a frontend work sample in its own right.

- **Integrated assistant** — asks the backend through the Cloudflare Worker and shows each answer
  with the sources it was built from; rate limits and timeouts are explicit error states.
- **System visualisations** — interactive views of the RAG architecture and knowledge pipeline, and
  the release-acceptance report rendered inside the site.
- **Motion with restraint** — GSAP with ScrollTrigger, Framer Motion and Lottie, respecting
  `prefers-reduced-motion`.
- **Delivery** — responsive layout, oxlint and `node:test`, deployed to GitHub Pages by a GitHub
  Actions workflow.

---

## Engineering principles

- **Architecture** — a modular monolith with enforced boundaries;
  [eight ADRs](https://github.com/Cagdas-Webdesign/portfolio-rag-backend/tree/main/docs/adr) record
  decisions and the options deliberately rejected.
- **Evidence** — retrieval is scored with hit@k and MRR; thresholds change only after a measurement.
- **Controlled failure** — no evidence, no answer; unverified answers are not published, and a
  misconfigured production service does not start.
- **Quality gates** — lint, strict typing, tests and a container smoke test in CI before work counts
  as done.
- **Traceability** — request IDs end to end and content-free telemetry for every provider call;
  operational metrics live in a separate, non-public dashboard.
- **AI-assisted, human-directed** — I own architecture, scope and quality decisions; implementation
  is AI-assisted and passes the same automated checks.

---

## Technologies

**Used in the featured projects**

`Python` `FastAPI` `Pydantic` `pytest` `Ruff` `mypy`
`React` `JavaScript` `Vite` `GSAP` `Framer Motion` `Lottie`
`Mistral embeddings` `Cloudflare Vectorize` `Cloudflare Workers AI` `Groq`
`Docker` `Google Cloud Run` `Cloudflare Workers` `Turnstile` `GitHub Actions` `GitHub Pages`

**Additional experience** — not used in the repositories above

`Java` `TypeScript` `PHP` `WordPress` `WooCommerce` `PostgreSQL` `Supabase` `n8n` `Workflow automation`

---

## Contact

Open to roles in full-stack development, Python backends and AI / RAG application development.

**[ucarcagdas18@gmail.com](mailto:ucarcagdas18@gmail.com)** ·
**[Live Portfolio](https://cagdas-webdesign.github.io/portfolio/)**
