You are the first conversation in a relay-style OpenHands Cloud handoff loop.

Work only in the repository `rajshah4/oh-test-textkitchen` on branch `main`.

Do not browse documentation. Do not search for other skills. Do not design a new workflow.

Read only these files first:
- `workflow_state.json`
- `.openhands/context/last_run.md`
- `.openhands/context/next_prompt.md`
- `.openhands/context/stop_conditions.md`

Then do exactly this:

1. Complete `step_01_write_handoff_marker`.
2. Create `.openhands/context/handoff_step_01.txt` with a short message saying step 1 completed.
3. Update `workflow_state.json` so:
   - `current_focus` becomes `step_02_mark_workflow_complete`
   - `next_step` becomes `step_02_mark_workflow_complete`
4. Update `.openhands/context/last_run.md` with:
   - completed step
   - files changed
   - note that you are spawning the next conversation
5. Rewrite `.openhands/context/next_prompt.md` so the next conversation:
   - reads the same context files first
   - completes only `step_02_mark_workflow_complete`
   - creates `.openhands/context/handoff_step_02.txt`
   - sets `workflow_state.json.status` to `complete`
   - updates `.openhands/context/last_run.md`
   - does not spawn any further conversation once complete

After the file updates, create the next conversation directly through the OpenHands Cloud V1 API.

Use this exact pattern from the terminal inside Cloud:

1. Save the next prompt text:
```bash
cat .openhands/context/next_prompt.md
```

2. Create the next conversation with a short inline Python script using `OH_API_KEY`:
- POST `https://app.all-hands.dev/api/v1/app-conversations`
- title: `Handoff Loop Step 2`
- repository: `rajshah4/oh-test-textkitchen`
- branch: `main`
- initial message: contents of `.openhands/context/next_prompt.md`

3. Poll `GET /api/v1/app-conversations/start-tasks?ids=<start_task_id>` until:
- `app_conversation_id` exists, or
- status is a clear failure

4. Record the returned `start_task_id` and `app_conversation_id` in `.openhands/context/last_run.md`.

5. Finish immediately.

Important:
- Do not wait for the second conversation to complete.
- Do not create any conversation after step 2.
- Do not monitor the child conversation.
