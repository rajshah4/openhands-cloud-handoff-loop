from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_CLOUD_URL = "https://app.all-hands.dev"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the next OpenHands Cloud V1 conversation and stop after startup succeeds.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--state-file")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--poll-interval", type=float, default=3.0)
    return parser.parse_args()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def cloud_api_url() -> str:
    return os.getenv("OPENHANDS_CLOUD_API_URL", DEFAULT_CLOUD_URL)


def cloud_api_key() -> str:
    return os.getenv("OPENHANDS_API_KEY") or os.getenv("OH_API_KEY") or require_env("OH_API_KEY")


def cloud_request(
    path: str,
    *,
    method: str = "GET",
    params: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
) -> Any:
    url = f"{cloud_api_url().rstrip('/')}{path}"
    if params:
        url = f"{url}?{urlencode(params, doseq=True)}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        method=method,
        data=body,
        headers={
            "Authorization": f"Bearer {cloud_api_key()}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=30.0) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Cloud API request failed: {exc.code} {detail}") from exc


def create_app_conversation(title: str, repository: str, branch: str, prompt_text: str) -> dict[str, Any]:
    return cloud_request(
        "/api/v1/app-conversations",
        method="POST",
        payload={
            "title": title,
            "selected_repository": repository,
            "selected_branch": branch,
            "initial_message": {
                "role": "user",
                "content": [{"type": "text", "text": prompt_text}],
                "run": True,
            },
        },
    )


def get_start_tasks(ids: list[str]) -> list[dict[str, Any]]:
    return cloud_request("/api/v1/app-conversations/start-tasks", params={"ids": ids})


def get_app_conversations(ids: list[str]) -> list[dict[str, Any]]:
    return cloud_request("/api/v1/app-conversations", params={"ids": ids})


def wait_for_start(start_task_id: str, *, timeout: float, poll_interval: float) -> dict[str, Any]:
    started = time.monotonic()
    while time.monotonic() - started <= timeout:
        tasks = get_start_tasks([start_task_id])
        task = tasks[0] if tasks else {}
        if task.get("app_conversation_id"):
            return task
        status = str(task.get("status", "")).upper()
        if status in {"FAILED", "ERROR", "STOPPED"}:
            return task
        time.sleep(poll_interval)
    raise TimeoutError(f"Timed out waiting for start task {start_task_id}")


def read_state(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def should_skip_spawn(state: dict[str, Any]) -> str | None:
    if state.get("status") == "complete":
        return "workflow is already complete"
    if not state.get("next_step"):
        return "next_step is empty"
    relay = state.get("relay", {})
    if relay.get("pending_conversation_id"):
        return "a pending conversation is already recorded"
    if relay.get("pending_start_task_id"):
        return "a pending start task is already recorded"
    return None


def record_spawn_metadata(state: dict[str, Any], *, title: str, start_task_id: str, app_conversation_id: str) -> dict[str, Any]:
    relay = state.setdefault("relay", {})
    relay["pending_start_task_id"] = start_task_id
    relay["pending_conversation_id"] = app_conversation_id
    relay["last_spawned_title"] = title
    relay["last_spawned_at"] = now_iso()
    state["updated_at"] = now_iso()
    return state


def main() -> int:
    args = parse_args()
    prompt_text = Path(args.prompt_file).read_text(encoding="utf-8")
    state_path = Path(args.state_file).resolve() if args.state_file else None
    state: dict[str, Any] | None = None
    if state_path:
        state = read_state(state_path)
        reason = should_skip_spawn(state)
        if reason:
            print(json.dumps({"skipped": True, "reason": reason}, indent=2))
            return 0
    created = create_app_conversation(args.title, args.repository, args.branch, prompt_text)
    start_task_id = created["id"]
    task = wait_for_start(start_task_id, timeout=args.timeout, poll_interval=args.poll_interval)
    app_conversation_id = task.get("app_conversation_id")

    result = {
        "start_task_id": start_task_id,
        "status": task.get("status"),
        "app_conversation_id": app_conversation_id,
    }

    if app_conversation_id:
        conversations = get_app_conversations([app_conversation_id])
        if conversations:
            result["conversation_url"] = conversations[0].get("conversation_url")
            result["execution_status"] = conversations[0].get("execution_status")
        if state_path and state is not None:
            updated = record_spawn_metadata(
                state,
                title=args.title,
                start_task_id=start_task_id,
                app_conversation_id=app_conversation_id,
            )
            write_state(state_path, updated)
        print(json.dumps(result, indent=2))
        return 0

    print(json.dumps(result, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
