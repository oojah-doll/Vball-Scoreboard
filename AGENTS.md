# Volleyball Scoreboard Codebase

For coding agents working in Volleyball scoreboard
This depot contains the SevenSegment, and CircuitPY
this is a small personal project.
The goal of this project is to display a digital scoreboard using a seven segment display on a physical LED scoreboard.
This codebase uses Git.
This codebase is in Python

# Personal vs Profressional Projects
This is a personal project. Do not use any of the Riot Games information for this project.
Do not use the Sentry or Notion MCPs.

## Line Endings
Need to figure this out :p

## Python
Current engineers are Prinicpal level C++ Game developers, who have no experience in python. Please explain things with this audience in mode

## Artifacts
When creating artifacts from investigations or compiling reports, place them in a top-level `Docs/` directory.

## Coding Standards

I am a C++ game programmer. When writing Python code for me, prefer a clear, strongly typed, C++-like style.

Guidelines:
- Use type hints for function parameters, return values, and important variables.
- Explicitly declare important instance members in the class body with their type when practical.
- Prefer explicit, readable code over clever or overly compact code.
- Keep functions small and focused.
- Use clear names that describe intent.
- Add comments where they help explain non-obvious logic.
- Write code for a technical audience, but do not assume deep Python-specific knowledge.
- Avoid unnecessary abstractions.
- Prefer simple control flow and straightforward data structures.
- When code is intended to run on the device, keep it compatible with CircuitPython.
- Treat CircuitPython compatibility as a design constraint for shared/runtime code, but not necessarily for host-only tools and tests.
- Prefer simple language features and data structures over advanced Python features when writing shared code.
- Be cautious with Python features that may not be supported consistently in CircuitPython; for example, enum support should not be assumed.
- Prefer explicit module names and direct submodule imports over broad package-level alias APIs.

## Planning and Permission Requirements

Before making any coding changes, always produce a planning section first.

The plan must include:
- The intended changes.
- The files or areas likely to be affected.
- Any risks, tradeoffs, or assumptions.
- Any ambiguities that need clarification.

Do not make assumptions when requirements are unclear. Ask questions about ambiguities during the planning phase before proceeding.

After presenting the plan, stop and wait for an explicit command to proceed. Do not edit files, generate patches, run formatting that modifies files, or otherwise make code changes until explicit permission is given.

Never run write-capable Git commands without explicit permission first. This includes commands such as `git add`, `git commit`, `git reset`, `git checkout`, `git switch`, `git rebase`, `git merge`, `git cherry-pick`, `git clean`, `git stash`, or any other Git command that modifies the working tree, index, branches, commits, or repository state.

Read-only inspection commands are allowed during planning, such as `git status`, `git diff`, `git log`, and `git show`, unless instructed otherwise.

Only proceed after receiving a clear go-ahead such as "go ahead," "apply the changes," "make the edit," or an equivalent explicit instruction.
