---
name: grill-u
description: Deeply interrogate a software program, agent, CLI, app, library, or developer tool to explain what it does, how it works, what advanced or hidden uses it has, and where it appears to be going. Use when the user asks to "grill" or deeply understand a program such as Codex, Claude Code, an SDK, CLI, installed binary, repository, or SaaS/devtool; when they want synthesis from public research, local execution, source inspection, docs, issues, changelogs, or direct interaction with the program.
---

# Grill U

Grill the program, not the user. The goal is to produce a deep, evidence-backed understanding of a target program by combining public research, local interrogation, source/code inspection, and controlled experiments.

## Operating Mode

Start by identifying the target, version, environment, and the user's practical purpose. Ask at most one clarifying question if the target or allowed access is ambiguous; otherwise proceed with reasonable assumptions and state them.

Treat each conclusion as a hypothesis until it has evidence. Prefer primary sources and direct observation over summaries. Separate confirmed facts, strong inferences, weak signals, and speculation.

Do not stop at surface-level documentation. Look for behavior that emerges from help output, configuration files, logs, source layout, tests, examples, release notes, issue discussions, and actual runs.

## Evidence Ladder

Use the strongest available evidence first, then broaden:

1. Direct execution: run safe commands such as `--help`, `--version`, config inspection, dry runs, example projects, read-only diagnostics, and small reversible experiments.
2. Local artifacts: inspect installed files, package metadata, manuals, completions, config schemas, cache directories, logs, tests, examples, and source if present.
3. Source repositories: read architecture, entry points, command implementations, tests, docs, roadmap files, releases, issues, discussions, and PRs.
4. Official public material: docs, changelogs, blog posts, announcements, API references, migration guides, pricing/plan pages, security docs, and support articles.
5. Community material: high-quality articles, forum threads, talks, examples, reverse engineering notes, benchmarks, and comparisons. Use as leads, not final authority.
6. Direct interrogation: if the program is interactive or agentic, ask it structured questions, compare answers against observed behavior, and test claims.

When information may be current or version-sensitive, browse the web and cite sources. Favor official sources, release notes, and repository history for claims about latest features or roadmap.

## Interrogation Workflow

1. Frame the target: name, version, installation/source location, product category, intended users, and the user's reason for caring.
2. Build a capability map: list top-level jobs, subcommands/features, extension points, integrations, supported inputs/outputs, automation surfaces, and boundaries.
3. Probe the live program: run non-destructive commands, create tiny throwaway examples, vary flags/configs, and record surprising behavior.
4. Inspect implementation: trace entry points to core modules, identify architectural seams, protocols, storage formats, permission model, network calls, and dependency choices.
5. Mine public signals: look for roadmap, recent releases, unresolved issues, experimental flags, deprecations, beta docs, job-to-be-done positioning, and ecosystem examples.
6. Challenge claims: for each notable capability, find at least one confirming source or experiment. Mark unsupported claims explicitly.
7. Synthesize into a user-facing field guide: explain what the program is for, how to use it well, where it is powerful, where it is fragile, and what to watch next.

## Direct Program Questioning

For an interactive program such as Claude Code, Codex, an agent runtime, REPL, or assistant CLI, question it in layers:

- Identity: "What problem are you optimized to solve? What are you not?"
- Interface: "What commands, modes, config files, hooks, prompts, and environment variables matter?"
- Power use: "What workflows do expert users chain together?"
- Failure: "Where do users overestimate you? What mistakes cause bad outcomes?"
- Internals: "What can you reveal about planning, tool use, memory, permissions, isolation, and context handling?"
- Roadmap signals: "What has recently changed? What docs or release notes should I read?"

Do not trust the program's self-description by default. Verify with docs, source, observed behavior, or reproducible experiments.

## Safety

Keep experiments read-only or throwaway unless the user authorizes side effects. Avoid destructive commands, credential exposure, telemetry opt-ins, paid operations, publishing, deployment, or modifying user config without clear need and permission.

If inspecting binaries or closed-source apps, stay within ordinary user-accessible behavior and files. Do not bypass access controls, license checks, authentication, or security boundaries.

## Output Shape

Return a concise but deep dossier:

1. One-sentence thesis: what the program really is.
2. Capability map: the major things it can do, grouped by user goal.
3. Mental model: how the program appears to work internally, with evidence labels.
4. High-leverage workflows: advanced or non-obvious usage patterns.
5. Hidden surfaces: config, flags, environment variables, hooks, APIs, plugins, protocols, file formats, or undocumented behaviors worth knowing.
6. Limits and failure modes: where it breaks, misleads, costs money/time, or requires caution.
7. Future direction: confirmed roadmap, recent trajectory, and clearly labeled inferences.
8. Experiments performed: commands, prompts, files, or source paths examined, with results.
9. Source trail: links and local file references sufficient for the user to continue investigating.

If the user wants an ongoing grilling session instead of a finished dossier, ask one investigative question at a time and include the recommended next probe. Still look up facts directly instead of asking the user for facts that can be discovered.
