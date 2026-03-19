# OpenHands Cloud Handoff Loop

This repo now contains two related skills:

- `skills/openhands-cloud-api`
  General OpenHands Cloud V1 API usage, including how to create conversations and wait only for startup.
- `skills/wiggum-relay-loop`
  A Ralph/Wiggum-style relay workflow where each conversation completes one bounded step, writes durable handoff files, spawns the next Cloud conversation, and stops.

## Repo Layout

- `skills/openhands-cloud-api/`
- `skills/wiggum-relay-loop/`
- `examples/three-step-demo/`
- `test-prompts/`

## How They Fit Together

Use the API skill when a conversation needs the exact Cloud API mechanics.

Use the relay-loop skill when the workflow should:

- avoid one giant conversation
- keep state in repo files
- roll over to a new conversation before context gets too large
- stop immediately after spawning the next conversation

## Rollover

This repo uses proactive rollover instead of waiting for condensing:

- stop at bounded step boundaries
- use repo-defined thresholds such as turns, reviewed files, or note size
- write the next prompt into repo files
- spawn the next conversation
- finish immediately
