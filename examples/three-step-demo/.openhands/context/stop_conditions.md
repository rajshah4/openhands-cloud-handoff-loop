# Stop Conditions

- Stop when `workflow_state.json.status` is `complete`.
- Stop when `next_step` is empty.
- Stop when `relay.pending_conversation_id` is already set.
- Stop if the next step is ambiguous.
- Stop if the spawn API call fails.
