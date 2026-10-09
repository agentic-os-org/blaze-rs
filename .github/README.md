# GitHub merge gates

[中文说明](README_zh.md)

This directory adapts the useful merge checks from `alibaba/anolisa` to the
standalone Blaze repository. The workflows use GitHub-hosted Linux runners,
run from the repository root, and follow the Rust 1.88 and commit conventions
defined in `AGENTS.md`.

## Required checks

| Check | What it proves |
| --- | --- |
| `Rust gate` | Formatting, Clippy with warnings denied, workspace tests, and rustdoc all succeed on Linux with the pinned toolchain. |
| `Documentation gate` | English and Chinese document trees stay paired and relative Markdown links resolve. |
| `Pull request policy gate` | Every commit follows the repository subject format and contains a `Signed-off-by` trailer. |

The pull request title, branch name, and issue reference produce guidance but
do not block merging. This preserves the parent repository's distinction
between correctness gates and contribution guidance.

## Branch protection

Workflow files do not protect a branch by themselves. After these workflows
have run once on GitHub, configure a rule for `main` that:

1. requires a pull request before merging;
2. requires `Rust gate`, `Documentation gate`, and
   `Pull request policy gate` to pass;
3. requires review conversations to be resolved;
4. blocks force pushes and branch deletion.

Do not require code-owner approval while the repository has only one active
maintainer: a pull request author cannot approve their own change. Enable it
after a second maintainer can review changes.

## Deliberately excluded automation

The parent repository's label, notification, issue-management, merge-message,
and Qoder workflows are not merge correctness checks. They also depend on
Anolisa-specific labels, secrets, or self-hosted runners. They must not be
copied into this repository until those dependencies are provisioned and the
workflow is adapted and tested here.
