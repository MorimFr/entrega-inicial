"""Captura somente metadados públicos de governança; não cria/aprova/mergeia PRs."""

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

REPO = "MorimFr/entrega-inicial"
ROOT = Path(__file__).resolve().parents[1]


def gh(*args: str, optional: bool = False) -> object:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=False
    )
    if result.returncode:
        if optional:
            return None
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", type=int, default=27)
    parser.add_argument("--video-url")
    parser.add_argument("--video-seconds", type=int)
    parser.add_argument("--video-access-checked", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evidence/entrega3/github.json")
    args = parser.parse_args()
    if bool(args.video_url) != bool(args.video_seconds):
        parser.error("Informe juntos link e duração real do vídeo")
    if args.video_url and not args.video_url.startswith("https://"):
        parser.error("O link do vídeo deve usar HTTPS")
    if args.video_seconds and not 180 <= args.video_seconds <= 300:
        parser.error("O vídeo precisa ter entre 180 e 300 segundos")
    pr = gh(
        "pr",
        "view",
        str(args.pr),
        "--repo",
        REPO,
        "--json",
        "number,url,state,isDraft,baseRefName,headRefName,headRefOid,mergeCommit,"
        "reviewDecision,mergedAt,reviews,statusCheckRollup",
    )
    assert isinstance(pr, dict)
    branch = gh("api", f"repos/{REPO}/branches/main")
    assert isinstance(branch, dict)
    tag = gh("api", f"repos/{REPO}/git/ref/tags/v1.0.0", optional=True)
    tag_commit = None
    if isinstance(tag, dict):
        obj = tag["object"]
        while obj["type"] == "tag":
            annotated = gh("api", f"repos/{REPO}/git/tags/{obj['sha']}")
            assert isinstance(annotated, dict)
            obj = annotated["object"]
        tag_commit = obj["sha"]
    protection = gh("api", f"repos/{REPO}/branches/main/protection")
    runs = gh(
        "run",
        "list",
        "--repo",
        REPO,
        "--workflow",
        "ci.yml",
        "--limit",
        "30",
        "--json",
        "databaseId,url,headSha,headBranch,status,conclusion,event,createdAt",
    )
    snapshot = {
        "captured_at": datetime.now(UTC).isoformat(),
        "repository": f"https://github.com/{REPO}",
        "pr": pr,
        "main": {"sha": branch["commit"]["sha"], "protected": branch["protected"]},
        "protection": protection,
        "runs": runs,
        "open_prs": gh("pr", "list", "--repo", REPO, "--state", "open", "--json", "number,url"),
        "release": gh(
            "release",
            "view",
            "v1.0.0",
            "--repo",
            REPO,
            "--json",
            "tagName,url,targetCommitish,isDraft,publishedAt",
            optional=True,
        ),
        "tag_commit": tag_commit,
        "video": {
            "url": args.video_url,
            "seconds": args.video_seconds,
            "access_checked": args.video_access_checked,
            "source": "Informação do aluno; não é gravação produzida pelo agente",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"SNAPSHOT_OK: {args.output}")


if __name__ == "__main__":
    main()
