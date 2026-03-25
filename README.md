# OpenHands Cloud Handoff Loop

This repository documents a relay-style OpenHands Cloud workflow where each conversation completes one bounded step, writes durable handoff files into the repo, starts the next conversation, and then stops.

The pattern is useful when you want a long-running workflow without depending on one large conversation context. Instead of condensing in place, the workflow rolls forward through fresh conversations with repo files as the source of truth.

## What Is In This Repo

The repo is centered on two related skills:

- `skills/openhands-cloud-api/`
  Exact OpenHands Cloud V1 API mechanics, including creating a conversation and waiting only until startup succeeds.
- `skills/wiggum-relay-loop/`
  A relay workflow pattern where each conversation completes one bounded unit of work, updates handoff files, spawns the next conversation, and exits.

For a better deeper dive on the subagents skills, check out the [full skill here](https://github.com/neubig/workflow/blob/main/skills/sub-agent-delegation/SKILL.md)

Supporting material:

- `examples/three-step-demo/`
  A minimal example workflow state and seed prompt for a three-conversation demo.
- `test-prompts/`
  Prompts you can use to exercise or evaluate the pattern.

## How The Two Skills Fit Together

Use `openhands-cloud-api` when you need the exact Cloud API behavior:

- create a fresh Cloud conversation
- poll the start task until `app_conversation_id` appears
- fetch conversation metadata
- automate startup from a helper script

### Reading V1 child conversation messages

If you need the output from a `V1` child conversation, use the SDK agent server
event search route:

`{agent_url}/api/conversations/{conversation_id}/events/search?limit=...`

That route returns SDK event objects under `items`, including `MessageEvent`
entries with `llm_message.role` and `llm_message.content`.

Do not use the old `V0` route `/api/conversations/{id}/events` for `V1`
children, and do not assume the app-server route
`/api/v1/conversation/{id}/events/search` will contain message events.

Use `wiggum-relay-loop` when the workflow should:

- avoid one long-lived conversation
- keep state in durable repo files
- roll over before context grows too large
- stop immediately after the next conversation has started

In practice, the relay-loop skill defines the workflow pattern and the Cloud API skill provides the concrete spawn mechanics.

## Example Workflow

The example in `examples/three-step-demo/` demonstrates a simple relay across three bounded conversations:

1. Conversation 1 completes step 1, updates the handoff files, commits and pushes, then starts conversation 2.
2. Conversation 2 completes step 2, updates the handoff files, commits and pushes, then starts conversation 3.
3. Conversation 3 finishes the workflow, marks the state complete, commits and pushes, and does not start another conversation.

The example `workflow_state.json` shows the rollover limits and relay metadata used to prevent duplicate spawns.

## Operational Rules

- Pass `OH_API_KEY` explicitly when invoking the helper from inside an OpenHands Cloud conversation.
- Treat repo files, not conversation memory, as the durable workflow state.
- Commit and push each completed step before starting the next conversation.
- On the final step, commit and push the completion state before exiting.
- Do not wait for the child conversation to finish when the workflow only needs startup confirmation.

## Launch Pattern

Use the helper script from the Cloud API skill:

```bash
OH_API_KEY="${OH_API_KEY:?missing OH_API_KEY}" \
python skills/openhands-cloud-api/scripts/launch_next_conversation.py \
  --title "Next workflow step" \
  --repository owner/repo \
  --branch main \
  --prompt-file .openhands/context/next_prompt.md \
  --state-file workflow_state.json
```

If `workflow_state.json` is supplied, the helper records the pending conversation metadata and skips duplicate spawns when the workflow is already complete or a child conversation is already pending.

## Verified E2E Result

This pattern was verified end to end against a disposable public repository:

- `rajshah4/oh-relay-e2e-20260319`

Observed sequence:

1. Step 1 conversation started, edited repo files, committed, and pushed.
2. Step 1 spawned step 2 through the Cloud V1 API and recorded the child ids in `.openhands/context/last_run.md`.
3. Step 2 started in a fresh conversation, completed the final workflow step, committed, pushed, and stopped without spawning another conversation.

The resulting repo state included:

- `.openhands/context/handoff_step_01.txt`
- `.openhands/context/handoff_step_02.txt`
- `workflow_state.json` with `status: "complete"`
- `last_run.md` showing the step 1 handoff ids and final step 2 completion

## Reproduce It

To replicate the verified flow with minimal surprises:

1. Create a fresh disposable GitHub repo with a normal `main` branch and push the seed files:
   - `workflow_state.json`
   - `.openhands/context/last_run.md`
   - `.openhands/context/next_prompt.md`
   - `.openhands/context/stop_conditions.md`
2. Start step 1 with a prompt like `test-prompts/seed-step-1-strict.md`, but replace the repository and branch names with your repo.
3. Make sure the step 1 prompt tells the Cloud conversation to spawn step 2 using Python standard library only.
4. Wait for step 1 to push its repo changes and record the spawned child ids.
5. Verify that step 2 finishes by checking the repo, not the parent conversation:
   - `workflow_state.json` is `complete`
   - `.openhands/context/handoff_step_02.txt` exists
   - `last_run.md` says this was the final step

Important replication notes:

- A fresh repo on `main` was more reliable than reusing a repo with leftover workflow state.
- The tested spawn path used the V1 API payload fields `title`, `selected_repository`, `selected_branch`, and `initial_message`.
- The prompt must not depend on `requests`; the verified path used `urllib.request`.

## Rollover Model

This repository uses proactive rollover instead of waiting for condensation. The intended flow is:

- stop at a bounded step boundary
- write updated handoff context into repo files
- start the next Cloud conversation
- confirm startup succeeded
- exit immediately

You can tune the rollover behavior through repo-defined state such as max turns, reviewed files, note size, or a policy to always roll over after each step.
