You are the first conversation in a three-step OpenHands Cloud handoff loop.

Work in the current repository only.

Read first:
- `workflow_state.json`
- `.openhands/context/last_run.md`
- `.openhands/context/next_prompt.md`
- `.openhands/context/stop_conditions.md`
- `.openhands/context/rollover_policy.json`

Complete only `step_01_create_marker`.

Requirements:
- create `.openhands/context/step_01.txt`
- mark step 1 done in `workflow_state.json`
- set `current_step` and `next_step` to `step_02_create_marker`
- clear any stale relay fields before preparing the next prompt
- rewrite `.openhands/context/next_prompt.md` for step 2
- update `.openhands/context/last_run.md`
- spawn the next conversation with:

```bash
python scripts/launch_next_conversation.py \
  --title "Three Step Demo Step 2" \
  --repository <owner/repo> \
  --branch main \
  --prompt-file .openhands/context/next_prompt.md \
  --state-file workflow_state.json
```

- stop immediately after startup succeeds
