# Idempotency And Locking

Before spawning, re-read `workflow_state.json` and stop if:

- `status` is `complete`
- `next_step` is empty
- `relay.pending_conversation_id` is already set
- `relay.pending_start_task_id` is already set

When startup succeeds, write these immediately:

- `relay.pending_start_task_id`
- `relay.pending_conversation_id`
- `relay.last_spawned_title`
- `relay.last_spawned_at`

On the final step:

- clear pending relay ids
- set `status` to `complete`
- do not spawn again
