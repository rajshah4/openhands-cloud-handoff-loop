You are the next conversation in a three-step OpenHands Cloud handoff loop.

Read first:
- `workflow_state.json`
- `.openhands/context/last_run.md`
- `.openhands/context/stop_conditions.md`
- `.openhands/context/rollover_policy.json`

Complete only the current step from `workflow_state.json`.
If the workflow is not complete after your bounded step:
- update the repo handoff files
- commit and push the updated repo state before spawning the next conversation
- spawn the next conversation with:

```bash
OH_API_KEY="${OH_API_KEY:?missing OH_API_KEY}" \
python scripts/launch_next_conversation.py \
  --title "Three Step Demo Next Step" \
  --repository <owner/repo> \
  --branch main \
  --prompt-file .openhands/context/next_prompt.md \
  --state-file workflow_state.json
```

- stop immediately

If the workflow is complete:
- commit and push the final state
- do not spawn another conversation
