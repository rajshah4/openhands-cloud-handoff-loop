# Handoff Files

Use these files as durable state for the relay loop.

## `workflow_state.json`

Recommended fields:

```json
{
  "project_name": "string",
  "current_step": "string",
  "status": "active|blocked|complete",
  "next_step": "string",
  "updated_at": "ISO-8601 string",
  "conversation_limits": {
    "max_turns_before_rollover": 12,
    "max_files_reviewed_before_rollover": 20,
    "max_notes_bytes_before_rollover": 12000,
    "always_rollover_after_step": true
  },
  "relay": {
    "pending_conversation_id": "",
    "pending_start_task_id": "",
    "last_spawned_title": "",
    "last_spawned_at": "",
    "handoff_token": ""
  }
}
```

## `.openhands/context/last_run.md`

Include:

- completed step
- files changed
- verification performed
- spawn result or explicit no-spawn reason

## `.openhands/context/next_prompt.md`

Write this for the next conversation, not the current one.

Include:

- files to read first
- bounded next step
- acceptance criteria
- stop rules

## `.openhands/context/stop_conditions.md`

Keep stop conditions explicit and short.
