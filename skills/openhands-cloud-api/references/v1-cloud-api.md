# OpenHands Cloud V1 API

Use these endpoints for Cloud-side automation:

- `POST /api/v1/app-conversations`
- `GET /api/v1/app-conversations/start-tasks`
- `GET /api/v1/app-conversations`
- `GET /api/v1/conversation/{app_conversation_id}/events/search`

## Reading child conversation messages

If you need `MessageEvent` output from a `V1` child conversation, query the SDK
agent server instead of the old `V0` events route.

Use:

`{agent_url}/api/conversations/{conversation_id}/events/search?limit=...`

Notes:

- the SDK agent server exposes `/events/search`, not `/events`
- `V1` child conversations are not stored in the `V0` ConversationStore
- `/api/v1/conversation/{app_conversation_id}/events/search` on the app server
  should not be treated as the source of child `MessageEvent` items

## Auth

Use `OH_API_KEY` or `OPENHANDS_API_KEY` as a bearer token.

## Create a conversation

```json
{
  "title": "Next workflow step",
  "selected_repository": "owner/repo",
  "selected_branch": "main",
  "initial_message": {
    "role": "user",
    "content": [
      {"type": "text", "text": "prompt text"}
    ],
    "run": true
  }
}
```

## Important distinction

`POST /api/v1/app-conversations` usually returns a start-task object.

- `id` is the `start_task_id`
- `app_conversation_id` may appear later

Poll:

- `GET /api/v1/app-conversations/start-tasks?ids=<start_task_id>`

until `app_conversation_id` exists or the status clearly failed.

## Relay guidance

For a relay workflow, stop after startup succeeds.

Do not wait for the child conversation to finish unless the workflow explicitly requires that.
