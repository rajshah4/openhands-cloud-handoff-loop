---
name: wiggum-relay-loop
description: Run Ralph/Wiggum-style relay workflows in OpenHands Cloud where each conversation completes one bounded repo step, writes durable handoff files, proactively rolls over before context gets too large, spawns the next Cloud conversation, and stops immediately. Use for sequential repo-improvement loops that should rely on files instead of long-lived conversation memory.
---

# Wiggum Relay Loop

Use this skill when the workflow should proceed through a chain of fresh Cloud conversations.

## Core Pattern

1. Read durable repo context files.
2. Complete one bounded step only.
3. Update the repo handoff files.
4. If the workflow should continue, start the next Cloud conversation.
5. Stop immediately after startup succeeds.

## Required Files

- `workflow_state.json`
- `.openhands/context/last_run.md`
- `.openhands/context/next_prompt.md`
- `.openhands/context/stop_conditions.md`

Read [references/handoff-files.md](references/handoff-files.md) for the expected structure.

## Idempotency

Before spawning:

- re-read `workflow_state.json`
- do not spawn if `status` is `complete`
- do not spawn if `next_step` is empty
- do not spawn if relay pending ids are already set

Read [references/idempotency-and-locking.md](references/idempotency-and-locking.md).

## Rollover Instead Of Condensing

Do not wait for the conversation to hit a condensation path.

Use repo-defined rollover thresholds and hand off early.

Read [references/context-rollover.md](references/context-rollover.md).

## Spawning

Use the Cloud API helper skill or its script:

```bash
OH_API_KEY="${OH_API_KEY:?missing OH_API_KEY}" \
python skills/openhands-cloud-api/scripts/launch_next_conversation.py \
  --title "Next workflow step" \
  --repository owner/repo \
  --branch main \
  --prompt-file .openhands/context/next_prompt.md \
  --state-file workflow_state.json
```

Always pass `OH_API_KEY` explicitly on the command line like the example above.

Do not assume the runtime shell will automatically inject the secret into child commands unless the command references it directly.

## Final Step

If the workflow is complete:

- set `status` to `complete`
- set `next_step` to `""`
- clear relay pending ids
- commit the final state
- push the final state to the tracked remote branch
- do not spawn another conversation

Do not call the workflow complete until the final commit is visible on the remote branch.
