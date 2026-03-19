# Next Steps

Use this guide to evolve the three-step demo into a more capable relay workflow.

## 1. Move From Fixed Steps To A Plan

Replace the simple three-step sequence with a plan in `workflow_state.json`.

Recommended step shape:

```json
{
  "id": "step_02_build_cli",
  "title": "Build CLI command",
  "status": "pending",
  "acceptance_criteria": [
    "Command parses arguments",
    "Tests cover success and failure cases"
  ],
  "last_result": ""
}
```

Recommended statuses:

- `pending`
- `in_progress`
- `done`
- `blocked`

Keep one `current_step` and one `next_step`. Mark a step `done`, advance the pointer, push, then spawn the next conversation.

## 2. Add A Planner Conversation

For larger workflows, add an explicit planning step before execution.

Recommended pattern:

1. planner conversation creates the initial step list
2. execution conversations only complete one existing step at a time
3. replanning is a separate, explicit action

Do not let every execution step casually rewrite the whole plan. That creates drift.

## 3. Keep Two Views Of State

Use both:

- `workflow_state.json` for machine-readable orchestration
- `TASKS.md` for a human-readable checklist

The JSON file should drive the relay. The markdown file should help humans inspect progress quickly.

## 4. Add Richer Step Contracts

For software tasks, each step should record:

- files changed
- tests run
- blockers
- follow-up risks
- recommended next step

That information can live in `last_result` or in a separate artifact file under `.openhands/context/`.

## 5. Allow Replanning Safely

If a step is blocked, do not silently improvise a new workflow. Use one of these rules:

- mark the step `blocked` and stop
- spawn a dedicated planner conversation
- split the blocked step into smaller steps only when the plan explicitly allows it

The key is to keep replanning deliberate.

## 6. Add Verification Gates

Before a conversation is allowed to spawn the next one, require:

- working tree committed
- changes pushed to the remote branch
- acceptance criteria updated
- relay state cleared and rewritten correctly

For the final step, require:

- `status: "complete"`
- `next_step: ""`
- relay ids cleared
- final commit pushed

## 7. Introduce Generic Roles

If the workflow grows beyond one generic worker, add roles such as:

- `planner`
- `builder`
- `reviewer`
- `tester`
- `researcher`

Keep the role set small. The relay pattern works best when each conversation still has one bounded responsibility.

## 8. Decide When To Roll Over

The best rollover point is usually the end of a bounded step, not an arbitrary token threshold.

Use thresholds only as safety rails:

- max turns
- max files reviewed
- max notes size

Prefer step-boundary rollover over emergency condensation.

## 9. Build A Reusable Test Harness

Once the relay pattern is stable, create one or two reusable test repos:

- a tiny Python CLI repo
- a tiny frontend repo

Use them to prove:

- plan creation
- multi-step execution
- blocked-step handling
- final completion behavior

## 10. Recommended Next Evolution

The most useful next version is:

1. planner writes a 5-10 step plan
2. each execution conversation checks off exactly one step
3. each step pushes before spawning
4. final step pushes a terminal `complete` state

That gives you a practical repo-improvement loop without needing one huge long-lived conversation.
