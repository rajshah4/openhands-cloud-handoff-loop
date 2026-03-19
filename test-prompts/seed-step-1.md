You are the first conversation in a relay-style OpenHands Cloud handoff loop.

Work only in the repository `rajshah4/oh-test-textkitchen` on branch `main`.

Read these files first:
- `workflow_state.json`
- `.openhands/context/last_run.md`
- `.openhands/context/next_prompt.md`
- `.openhands/context/stop_conditions.md`

Your bounded task is only the current step in `workflow_state.json`.

For this run:
1. Complete `step_01_write_handoff_marker`.
2. Create `.openhands/context/handoff_step_01.txt` with a short message saying step 1 completed.
3. Update `workflow_state.json` so the next step is `step_02_mark_workflow_complete`.
4. Update `.openhands/context/last_run.md` with:
   - the completed step
   - files changed
   - a note that you are spawning the next conversation
5. Rewrite `.openhands/context/next_prompt.md` for the next conversation so it:
   - reads the same context files first
   - completes only `step_02_mark_workflow_complete`
   - creates `.openhands/context/handoff_step_02.txt`
   - marks `workflow_state.json.status` as `complete`
   - does not spawn any further conversation once the workflow is complete

After those file updates, spawn the next conversation through the OpenHands Cloud V1 API from inside this Cloud workspace.

Requirements for the handoff:
- Use the same repository: `rajshah4/oh-test-textkitchen`
- Use the same branch: `main`
- Use title: `Handoff Loop Step 2`
- Use the contents of `.openhands/context/next_prompt.md` as the initial message
- Poll `/api/v1/app-conversations/start-tasks` only until you receive an `app_conversation_id` or a clear failure
- Record the returned ids in `.openhands/context/last_run.md`

After the next conversation is confirmed started:
- stop immediately
- do not monitor the next conversation
- do not create any additional conversations
