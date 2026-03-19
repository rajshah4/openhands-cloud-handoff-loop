# OpenHands Cloud Handoff Loop

This repo now contains two related skills:

- `skills/openhands-cloud-api`
  General OpenHands Cloud V1 API usage, including how to create conversations and wait only for startup.
- `skills/wiggum-relay-loop`
  A Ralph/Wiggum-style relay workflow where each conversation completes one bounded step, writes durable handoff files, spawns the next Cloud conversation, and stops.

## Repo Layout

- `skills/openhands-cloud-api/`
- `skills/wiggum-relay-loop/`
- `examples/three-step-demo/`
- `test-prompts/`

## How They Fit Together

Use the API skill when a conversation needs the exact Cloud API mechanics.

Use the relay-loop skill when the workflow should:

- avoid one giant conversation
- keep state in repo files
- roll over to a new conversation before context gets too large
- stop immediately after spawning the next conversation

## Operational Rules

- Pass `OH_API_KEY` explicitly when invoking the handoff helper from inside Cloud conversations.
- Push each step's repo state before spawning the next conversation.
- Push the final completion commit before finishing the last conversation.

## Run The Three-Step Test

Use `examples/three-step-demo/` as the seed for a real GitHub test repo.

1. Create a fresh GitHub repo and copy the example files into it.
2. Copy `skills/openhands-cloud-api/scripts/launch_next_conversation.py` into that test repo as `scripts/launch_next_conversation.py`.
3. Replace `<owner/repo>` in:
   - `examples/three-step-demo/seed_prompt.md`
   - `examples/three-step-demo/.openhands/context/next_prompt.md`
   with your real `owner/repo`.
4. Commit and push the seeded repo to `main`.
5. Launch step 1 from a machine that has your OpenHands Cloud API key:

```bash
export OH_API_KEY="..."
python scripts/launch_next_conversation.py \
  --title "Three Step Demo Step 1" \
  --repository owner/repo \
  --branch main \
  --prompt-file seed_prompt.md
```

6. Wait for the Cloud chain to run:
   - step 1 pushes state, then spawns step 2
   - step 2 pushes state, then spawns step 3
   - step 3 pushes final state and stops without spawning again
7. Verify the repo on `main`:
   - `workflow_state.json` has `status: "complete"`
   - `.openhands/context/step_01.txt` exists
   - `.openhands/context/step_02.txt` exists
   - `.openhands/context/step_03.txt` exists

Important:

- The spawn command inside Cloud must reference `OH_API_KEY` explicitly.
- Each step must push before spawning the next conversation.
- The final step must push before finishing.

## Rollover

This repo uses proactive rollover instead of waiting for condensing:

- stop at bounded step boundaries
- use repo-defined thresholds such as turns, reviewed files, or note size
- write the next prompt into repo files
- spawn the next conversation
- finish immediately

## Next Evolution

If you want to turn the demo into a plan-driven workflow, read [references/next-steps.md](references/next-steps.md).
