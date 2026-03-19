You are the next conversation in a three-step OpenHands Cloud handoff loop.

Read first:
- `workflow_state.json`
- `.openhands/context/last_run.md`
- `.openhands/context/stop_conditions.md`
- `.openhands/context/rollover_policy.json`

Complete only the current step from `workflow_state.json`.
If the workflow is not complete after your bounded step:
- update the repo handoff files
- spawn the next conversation with `scripts/launch_next_conversation.py --state-file workflow_state.json`
- stop immediately
