#!/usr/bin/env python3
"""Mod-Directory 可复用 GitHub 增量扫描工具。

基于 README.md / projects/*.md 中的已收录仓库，以及本地 .scan-state.json 状态文件，
增量发现与《学园偶像大师》PC DMM 模组生态相关的新仓库、活跃 Fork 及重点仓库动态。
本工具仅输出审阅报告，不直接修改 README.md。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import urllib.request

SEARCH_QUERIES = [
    ("gakumas", 100),
    ("gkms", 50),
    ("gakuen-idolmaster", 50),
    ("gakuen-imas", 30),
    ("gaku-mod-tools", 30),
    ("gaku", 100),
]

WATCHED_OWNERS = [
    ("orgs", "Gaku-Mod-Tools"),
    ("users", "chihya72"),
]

WATCHED_UPSTREAMS = [
    "Gaku-Mod-Tools/GakuLoader",
    "crested-ezios/GakuMotion",
    "KagaminTheMirror/gakumas-VRify",
    "54yq/GakuActors",
    "chihya72/gkms-localify-dmm-RE",
    "chihya72/gakumas-mod-runtime",
    "chihya72/gakumas-modding",
    "deadpixel134/gakumas-vr",
]

RELEVANCE_KEYWORDS = [
    "gakumas",
    "gkms",
    "gakuen",
    "idolmaster",
    "gakuloader",
    "gakumotion",
    "gakuactors",
    "gakuburst",
    "gaku-mod",
    "kinetexture",
    "vrify",
    "hatsuboshi",
    "localify",
    "学园偶像大师",
    "学園アイドルマスター",
    "学マス",
]

GITHUB_REPO_RE = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
ROW_URL_RE = re.compile(r"^\|\s*\[[^\]]+\]\((https?://[^)]+)\)\s*\|")
LAST_MAINT_RE = re.compile(r"(最后维护时间：)\d{4}-\d{2}-\d{2}")
TZ_CN = timezone(timedelta(hours=8))


def to_cn_date(iso_str: str) -> str:
    """将 ISO 8601 时间戳转换为东八区 YYYY-MM-DD 日期。"""
    normalized = iso_str.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(TZ_CN).strftime("%Y-%m-%d")


def fetch_json_url(url: str) -> Any:
    """通过 HTTP GET 拉取 JSON 数据。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mod-Directory-Sweep/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_latest_branch_date(repo_url: str) -> str | None:
    """获取仓库所有分支中最新的提交日期（YYYY-MM-DD，东八区）。"""
    clean_url = repo_url.rstrip("/")
    gh_match = re.match(r"^https?://github\.com/([^/]+)/([^/]+)$", clean_url, re.I)
    if gh_match:
        owner, name = gh_match.group(1), gh_match.group(2)
        query = (
            f'query {{ repository(owner: "{owner}", name: "{name}") {{ '
            'refs(refPrefix: "refs/heads/", first: 100) { '
            'nodes { target { ... on Commit { committedDate } } } } } }'
        )
        data = run_gh(["api", "graphql", "-f", f"query={query}"])
        nodes = (((data.get("data") or {}).get("repository") or {}).get("refs") or {}).get("nodes") or []
        dates = [
            n["target"]["committedDate"]
            for n in nodes
            if isinstance(n, dict) and isinstance(n.get("target"), dict) and n["target"].get("committedDate")
        ]
        if not dates:
            return None
        return max(to_cn_date(d) for d in dates)

    gitea_match = re.match(r"^https?://git\.chinosk6\.cn/([^/]+)/([^/]+)$", clean_url, re.I)
    if gitea_match:
        owner, name = gitea_match.group(1), gitea_match.group(2)
        branches = fetch_json_url(f"https://git.chinosk6.cn/api/v1/repos/{owner}/{name}/branches")
        dates: list[str] = []
        for b in branches:
            commit = b.get("commit") or {}
            ts = commit.get("timestamp") or (commit.get("committer") or {}).get("date")
            if ts:
                dates.append(to_cn_date(ts))
        return max(dates) if dates else None

    gitee_match = re.match(r"^https?://gitee\.com/([^/]+)/([^/]+)$", clean_url, re.I)
    if gitee_match:
        owner, name = gitee_match.group(1), gitee_match.group(2)
        branches = fetch_json_url(f"https://gitee.com/api/v5/repos/{owner}/{name}/branches")
        dates = []
        for b in branches:
            commit = b.get("commit") or {}
            c_url = commit.get("url")
            ts = ((commit.get("commit") or {}).get("committer") or {}).get("date")
            if not ts and c_url:
                detail = fetch_json_url(c_url)
                ts = ((detail.get("commit") or {}).get("committer") or {}).get("date")
            if ts:
                dates.append(to_cn_date(ts))
        return max(dates) if dates else None

    return None


def update_readme_dates(
    repo_root: Path, state: dict[str, Any]
) -> tuple[int, list[str]]:
    """更新 README.md 中的最后维护时间与每个项目条目的全分支最新更新时间。"""
    readme_path = repo_root / "README.md"
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    today_cn = datetime.now(TZ_CN).strftime("%Y-%m-%d")

    repo_dates: dict[str, str] = dict(state.get("repo_latest_dates") or {})
    warnings: list[str] = []
    updated_rows = 0
    new_lines: list[str] = []

    for line in lines:
        if LAST_MAINT_RE.search(line):
            line = LAST_MAINT_RE.sub(rf"\g<1>{today_cn}", line)
            new_lines.append(line)
            continue

        if line.strip() == "| 项目 | 定位与关系 | 详情 | 状态 |":
            new_lines.append("| 项目 | 定位与关系 | 详情 | 最新更新时间 |")
            continue

        match = ROW_URL_RE.match(line)
        if match:
            url = match.group(1)
            try:
                latest_date = get_latest_branch_date(url)
            except Exception as exc:
                latest_date = None
                warnings.append(f"获取 `{url}` 最新分支时间失败: {exc}")

            if latest_date:
                repo_dates[url] = latest_date
                parts = line.split("|")
                if len(parts) >= 6:
                    parts[-2] = f" {latest_date} "
                    line = "|".join(parts)
                    updated_rows += 1
        new_lines.append(line)

    readme_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    state["repo_latest_dates"] = repo_dates
    state["last_dates_updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return updated_rows, warnings


def run_gh(args: list[str]) -> Any:
    """执行 gh CLI 命令并解析 JSON 输出。"""
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"gh {' '.join(args)} 失败 (exit {proc.returncode})")
    return json.loads(proc.stdout)


def extract_indexed_repos(repo_root: Path) -> set[str]:
    """从 README.md 和 projects/*.md 中提取已收录的 GitHub owner/repo（小写）。"""
    files = [repo_root / "README.md"]
    projects_dir = repo_root / "projects"
    if projects_dir.is_dir():
        files.extend(sorted(projects_dir.glob("*.md")))

    indexed: set[str] = set()
    for path in files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in GITHUB_REPO_RE.findall(text):
            slug = match.rstrip(").,").lower()
            for suffix in ("/issues", "/pulls", "/releases", "/actions", "/discussions"):
                if slug.endswith(suffix):
                    slug = slug[: -len(suffix)]
            if slug.count("/") == 1:
                indexed.add(slug)
    return indexed


def load_state(state_path: Path) -> dict[str, Any]:
    """加载本地增量扫描状态。"""
    if not state_path.is_file():
        return {"last_scan_at": None, "ignored_repos": [], "watched_snapshots": {}}
    return json.loads(state_path.read_text(encoding="utf-8"))


def save_state(state_path: Path, state: dict[str, Any]) -> None:
    """保存本地增量扫描状态。"""
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def search_github_repos() -> tuple[dict[str, dict[str, Any]], list[str]]:
    """执行多关键词搜索并合并去重。"""
    found: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []

    for query, limit in SEARCH_QUERIES:
        try:
            items = run_gh([
                "search", "repos", query,
                "--sort", "updated",
                "--limit", str(limit),
                "--json", "fullName,description,url,stargazersCount,updatedAt,isFork",
            ])
            for item in items:
                key = item["fullName"].lower()
                found[key] = {
                    "full_name": item["fullName"],
                    "description": item.get("description") or "",
                    "url": item["url"],
                    "stars": item.get("stargazersCount", 0),
                    "updated_at": item.get("updatedAt", ""),
                    "is_fork": item.get("isFork", False),
                }
        except RuntimeError as exc:
            warnings.append(f"搜索关键词 `{query}` 失败: {exc}")

    for kind, owner in WATCHED_OWNERS:
        try:
            items = run_gh(["api", f"{kind}/{owner}/repos?per_page=100&sort=pushed"])
            for item in items:
                key = item["full_name"].lower()
                found[key] = {
                    "full_name": item["full_name"],
                    "description": item.get("description") or "",
                    "url": item["html_url"],
                    "stars": item.get("stargazers_count", 0),
                    "updated_at": item.get("pushed_at", ""),
                    "is_fork": item.get("fork", False),
                    "archived": item.get("archived", False),
                }
        except RuntimeError as exc:
            warnings.append(f"拉取 {kind}/{owner} 仓库列表失败: {exc}")

    return found, warnings


def check_active_forks(indexed: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    """检查核心上游仓库是否存在领先主线且未归档的活跃 Fork。"""
    active_forks: list[dict[str, Any]] = []
    warnings: list[str] = []

    for upstream in WATCHED_UPSTREAMS:
        try:
            upstream_info = run_gh(["api", f"repos/{upstream}"])
            upstream_branch = upstream_info.get("default_branch", "main")
            forks = run_gh(["api", f"repos/{upstream}/forks?per_page=100"])
        except RuntimeError as exc:
            warnings.append(f"检查 `{upstream}` Fork 失败: {exc}")
            continue

        for fk in forks:
            slug = fk["full_name"].lower()
            if fk.get("archived") or slug in indexed:
                continue
            owner = fk["full_name"].split("/", 1)[0]
            fk_branch = fk.get("default_branch", "main")
            try:
                cmp_data = run_gh(["api", f"repos/{upstream}/compare/{upstream_branch}...{owner}:{fk_branch}"])
                ahead_by = cmp_data.get("ahead_by", 0)
            except RuntimeError:
                ahead_by = 0

            if ahead_by > 0:
                active_forks.append({
                    "full_name": fk["full_name"],
                    "upstream": upstream,
                    "ahead_by": ahead_by,
                    "stars": fk.get("stargazers_count", 0),
                    "pushed_at": fk.get("pushed_at", ""),
                    "description": fk.get("description") or "",
                    "url": fk["html_url"],
                })

    return active_forks, warnings


def check_watched_updates(
    prev_snapshots: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    """检查重点上游仓库的最近推送与 Release 变更。"""
    updates: list[dict[str, Any]] = []
    new_snapshots: dict[str, Any] = {}
    warnings: list[str] = []

    for repo in WATCHED_UPSTREAMS:
        try:
            info = run_gh(["api", f"repos/{repo}"])
            releases = run_gh(["api", f"repos/{repo}/releases?per_page=1"])
            latest_tag = releases[0]["tag_name"] if releases else None
            snap = {
                "pushed_at": info.get("pushed_at", ""),
                "stars": info.get("stargazers_count", 0),
                "latest_release": latest_tag,
            }
            new_snapshots[repo] = snap
            old = prev_snapshots.get(repo)
            if old and (old.get("pushed_at") != snap["pushed_at"] or old.get("latest_release") != latest_tag):
                updates.append({"repo": repo, "old": old, "new": snap})
        except RuntimeError as exc:
            warnings.append(f"检查重点仓库 `{repo}` 动态失败: {exc}")

    return updates, new_snapshots, warnings


def is_relevant_repo(item: dict[str, Any]) -> bool:
    """粗筛可能与学马仕相关的仓库，排除纯同名噪音。"""
    text = f"{item['full_name']} {item.get('description', '')}".lower()
    return any(k in text for k in RELEVANCE_KEYWORDS)


def format_report(
    now_iso: str,
    last_scan_at: str | None,
    indexed_count: int,
    new_repos: list[dict[str, Any]],
    active_forks: list[dict[str, Any]],
    watched_updates: list[dict[str, Any]],
    warnings: list[str],
) -> str:
    """生成人类可读的 Markdown 增量扫描报告。"""
    lines = [
        "# Mod-Directory GitHub 增量扫描报告",
        "",
        f"- **扫描时间**：`{now_iso}`",
        f"- **上次扫描**：`{last_scan_at or '首次基线扫描'}`",
        f"- **已收录 GitHub 仓库数**：{indexed_count}",
        "",
    ]

    lines.append(f"## 1. 新发现的相关仓库（{len(new_repos)} 项）")
    lines.append("")
    if not new_repos:
        lines.append("本次无新增待审阅仓库。")
    else:
        lines.append("| 仓库 | Stars | 最近更新 | 简介 |")
        lines.append("| :--- | ---: | :--- | :--- |")
        for r in new_repos:
            desc = (r.get("description") or "—").replace("|", "\\|").replace("\n", " ")
            updated = (r.get("updated_at") or "")[:10]
            lines.append(f"| [{r['full_name']}]({r['url']}) | {r.get('stars', 0)} | {updated} | {desc} |")
    lines.append("")

    lines.append(f"## 2. 未收录的活跃 Fork（{len(active_forks)} 项）")
    lines.append("")
    if not active_forks:
        lines.append("本次无新增领先主线的活跃 Fork。")
    else:
        lines.append("| Fork | 上游 | 领先提交 | 最近推送 | 简介 |")
        lines.append("| :--- | :--- | ---: | :--- | :--- |")
        for fk in active_forks:
            desc = (fk.get("description") or "—").replace("|", "\\|").replace("\n", " ")
            pushed = (fk.get("pushed_at") or "")[:10]
            lines.append(
                f"| [{fk['full_name']}]({fk['url']}) | `{fk['upstream']}` | +{fk['ahead_by']} | {pushed} | {desc} |"
            )
    lines.append("")

    lines.append(f"## 3. 重点关注仓库变更（{len(watched_updates)} 项）")
    lines.append("")
    if not watched_updates:
        lines.append("自上次扫描以来无推送或 Release 变更（或首次建立基线）。")
    else:
        for upd in watched_updates:
            old_rel = upd["old"].get("latest_release") or "无"
            new_rel = upd["new"].get("latest_release") or "无"
            lines.append(
                f"- `{upd['repo']}`：推送 `{upd['old'].get('pushed_at')}` → `{upd['new'].get('pushed_at')}`，"
                f"Release `{old_rel}` → `{new_rel}`"
            )
    lines.append("")

    if warnings:
        lines.append("## 4. 扫描警告")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    default_state_path = repo_root / ".scan-state.json"

    parser = argparse.ArgumentParser(description="Mod-Directory GitHub 增量扫描工具")
    parser.add_argument("--state", type=Path, default=default_state_path, help="增量状态文件路径")
    parser.add_argument("--out", type=Path, default=None, help="可选：输出 Markdown 报告文件路径")
    parser.add_argument("--ignore", nargs="+", default=[], help="将指定 owner/repo 加入忽略清单并退出")
    parser.add_argument("--include-ignored", action="store_true", help="包含已忽略的仓库")
    parser.add_argument("--reset-state", action="store_true", help="重置本地扫描状态后重新扫描")
    parser.add_argument("--init-state", action="store_true", help="仅将当前搜索结果写入状态基线，不输出旧仓库告警")
    parser.add_argument("--update-dates", action="store_true", help="更新 README.md 顶部最后维护时间及各项目的全分支最新更新时间")
    args = parser.parse_args()

    state = {"last_scan_at": None, "ignored_repos": [], "watched_snapshots": {}}
    if not args.reset_state:
        state = load_state(args.state)

    if args.update_dates:
        updated_rows, date_warnings = update_readme_dates(repo_root, state)
        save_state(args.state, state)
        print(f"已更新 README.md 最后维护时间与 {updated_rows} 个项目的最新分支更新时间。")
        for w in date_warnings:
            print(f"警告: {w}", file=sys.stderr)
        return 0

    ignored_set = {s.lower() for s in state.get("ignored_repos", [])}
    if args.ignore:
        for item in args.ignore:
            ignored_set.add(item.lower())
        state["ignored_repos"] = sorted(ignored_set)
        save_state(args.state, state)
        print(f"已更新忽略清单（共 {len(ignored_set)} 项）：{args.state}")
        return 0

    indexed = extract_indexed_repos(repo_root)
    found, search_warnings = search_github_repos()
    active_forks, fork_warnings = check_active_forks(indexed)
    watched_updates, new_snapshots, watch_warnings = check_watched_updates(
        state.get("watched_snapshots", {})
    )
    warnings = search_warnings + fork_warnings + watch_warnings

    new_repos: list[dict[str, Any]] = []
    for slug, item in found.items():
        if slug in indexed:
            continue
        if not args.include_ignored and slug in ignored_set:
            continue
        if item.get("archived") or item.get("is_fork"):
            continue
        if not is_relevant_repo(item):
            continue
        new_repos.append(item)

    new_repos.sort(key=lambda r: (-r.get("stars", 0), r["full_name"].lower()))
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.init_state:
        for item in new_repos:
            ignored_set.add(item["full_name"].lower())
        state["ignored_repos"] = sorted(ignored_set)
        state["last_scan_at"] = now_iso
        state["watched_snapshots"] = new_snapshots
        save_state(args.state, state)
        print(f"已初始化基线状态至 {args.state}（已忽略未收录候选 {len(new_repos)} 项）。")
        return 0

    report = format_report(
        now_iso=now_iso,
        last_scan_at=state.get("last_scan_at"),
        indexed_count=len(indexed),
        new_repos=new_repos,
        active_forks=active_forks,
        watched_updates=watched_updates,
        warnings=warnings,
    )

    state["last_scan_at"] = now_iso
    state["watched_snapshots"] = new_snapshots
    save_state(args.state, state)

    if args.out:
        args.out.write_text(report, encoding="utf-8")
        print(f"扫描完成，报告已写入：{args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
