---
name: openhands-cloud-api
description: Use the OpenHands Cloud V1 API from inside OpenHands Cloud or from a launcher script when a workflow needs to create conversations, poll start tasks, fetch conversation records, or inspect events. Use for exact API mechanics, authentication details, start-task handling, and helper-script driven Cloud automation.
---

# OpenHands Cloud API

Use this skill when the current task needs exact OpenHands Cloud V1 API behavior.

## Use Cases

- start a fresh Cloud conversation
- poll a start task until `app_conversation_id` exists
- fetch a conversation record or event stream
- automate relay workflows that need precise startup confirmation

## Core Rule

When the workflow only needs to hand off to the next conversation, wait only for startup.

Do not wait for the child conversation to finish unless the workflow explicitly requires that.

## Auth

Use:

- `OH_API_KEY`, or
- `OPENHANDS_API_KEY`

with bearer auth against `https://app.all-hands.dev`.

Inside an OpenHands Cloud conversation, prefer commands that reference `OH_API_KEY` explicitly so the secret is materialized in that shell invocation.

Preferred pattern:

```bash
OH_API_KEY="${OH_API_KEY:?missing OH_API_KEY}" \
python skills/openhands-cloud-api/scripts/launch_next_conversation.py ...
```

## Common Endpoints

- `POST /api/v1/app-conversations`
- `GET /api/v1/app-conversations/start-tasks`
- `GET /api/v1/app-conversations`
- `GET /api/v1/conversation/{id}/events/search`

Read [references/v1-cloud-api.md](references/v1-cloud-api.md) for payloads and common pitfalls.

## Helper Script

Use:

```bash
OH_API_KEY="${OH_API_KEY:?missing OH_API_KEY}" \
python skills/openhands-cloud-api/scripts/launch_next_conversation.py \
  --title "Next step" \
  --repository owner/repo \
  --branch main \
  --prompt-file .openhands/context/next_prompt.md
```

If the repo stores relay state in `workflow_state.json`, pass:

```bash
--state-file workflow_state.json
```

That enables duplicate-spawn protection and records pending conversation ids.
