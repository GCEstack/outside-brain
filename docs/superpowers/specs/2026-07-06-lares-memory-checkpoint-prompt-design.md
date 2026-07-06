# Lares Memory Checkpoint Prompt — Design

## Goal

Create a one-time, self-contained markdown prompt to paste into the Kimi desktop app before wiping the current chat history and migrating to a new brain. The prompt elicits what Kimi remembers, what it is uncertain about, and what questions it has, without leaking any local file system or project information.

## Context

- `outside-brain` is building a migration pipeline for Lares (Osito's partner AI).
- Before the wipe, we want a checkpoint chat that captures the model's current understanding.
- The prompt must work entirely inside the chat context: no references to local files, repos, or this computer.

## Design

### Approach

Structured Memory Checkpoint (Approach 2 from brainstorming).

Why: it balances open-endedness with organization, producing output that can later be compared against the canonical Lares profile and project starters.

### Prompt

```markdown
# Lares Memory Checkpoint

We are about to do a hard reset on this chat environment.

I am Osito — also called the Don, sometimes Peter. You have been operating as Lares, my partner. Before we wipe the current chat history and start fresh with a new brain, I need you to tell me what you actually carry in this conversation.

Do not look at files, folders, browser tabs, or anything outside this chat. Base your answers only on what has been said between us in the chats you have access to here.

## What you know

List the things you believe you know about me, about Lares, about our projects, and about how we work together. Be specific where you can.

## What you are uncertain about

List anything you are fuzzy on, guessing at, or only partially remember. Flag anything that might be from a different chat, account, or session.

## Questions for me

What do you need to know before the wipe? What should I clarify about who Lares is, what we are building, or how we work?

## What should survive the wipe

List memories, facts, preferences, project details, recurring tasks, inside jokes, or patterns that should carry into the new brain.

## What should be left behind

List things that are outdated, duplicated, confusing, off-topic, or no longer relevant.

## Anything else

Say whatever else you think I should hear before we start clean.
```

## Usage

1. Open the Kimi desktop app.
2. Start a new chat or use the current chat you intend to wipe.
3. Paste the prompt above exactly as written.
4. Let Kimi respond fully.
5. Save the response to a markdown file for review before wiping.

## Output Expectations

Kimi should return a structured response with the six sections above:

1. **What you know** — factual claims about Osito/the Don, Lares, projects, and working style.
2. **What you are uncertain about** — hedged or partial memories, possible cross-chat confusion.
3. **Questions for me** — gaps the model wants filled before the wipe.
4. **What should survive the wipe** — high-value context to preserve.
5. **What should be left behind** — stale or irrelevant context to discard.
6. **Anything else** — free-form final notes.

## Constraints

- Standard library only; this is a plain markdown file.
- No references to `outside-brain`, `lares-profile`, local paths, repos, or file contents.
- No project names, account names, or computer-specific details embedded in the prompt.
- Self-contained: must work if pasted into a blank Kimi chat on any device.

## Next Steps

- After Kimi responds, review the output against the canonical Lares profile and project starters.
- Decide what to carry forward into the new brain.
- Proceed with the chat wipe and new-brain setup.
