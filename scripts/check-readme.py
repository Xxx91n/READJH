#!/usr/bin/env python3
"""scripts/check-readme.py — stdlib-only python3 static probe for README governance.

Seven static checks:
1. dead local links (markdown links & <a> tags pointing to missing local files)
2. missing image paths (markdown images, <img> tags, and <source> srcset)
3. code-fence imbalance (unclosed or mismatched backtick/tilde code fences)
4. badge URL domain sanity (valid hosts, flags placeholders e.g. TODO, example.com, username/repo)
5. boundary-phrase duplicate counting (ensures boundaries & disclaimers are stated at most once)
6. honest-gap signal presence (detects suspicious completeness when limitations/caveats/gaps are absent)
7. --repo-set cross-repo README skeleton diff (detects cross-repo skeleton isomorphism)

CLI contract:
    python3 scripts/check-readme.py <readme> [--repo-root <dir>] [--repo-set <manifest>] [--json]
Exit codes:
    0: All checks passed (no blocking findings)
    1: One or more blocking findings detected
    2: Command-line or argument error
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set, Tuple

# Standard recognized boundary / disclaimer / self-attestation phrases
BOUNDARY_PHRASES = [
    "out of scope",
    "at your own risk",
    "does not support",
    "do not support",
    "not responsible",
    "no warranty",
    "without warranty",
    "compliance note",
    "compliance notice",
    "not intended for",
    "security boundary",
    "self-attestation",
    # Chinese equivalents
    "免责声明",
    "仅供参考",
    "风险自负",
    "不支持",
    "暂不支持",
    "局限性",
    "不保证",
    "非安全边界",
    "合规说明",
    "合规提示",
]

# Honest-gap signal keywords / patterns
HONEST_GAP_PATTERNS = [
    r"\blimitations?\b",
    r"\bknown\s+(?:issues?|limitations?|defects?)\b",
    r"\bcaveats?\b",
    r"\btrade-?offs?\b",
    r"\bnon-?goals?\b",
    r"\bout\s+of\s+scope\b",
    r"\bnot\s+(?:yet\s+)?supported\b",
    r"\bunsupported\b",
    r"\bwork\s+in\s+progress\b",
    r"\bwip\b",
    r"\broadmap\b",
    r"\bhonest[- ]gaps?\b",
    r"\bnot\s+implemented\b",
    r"\bprerequisites?\b",
    r"\bresidual\s+risk\b",
    r"\bpreview\s+disclosure\b",
    # Chinese equivalents
    r"局限",
    r"局限性",
    r"已知问题",
    r"已知缺陷",
    r"暂不支持",
    r"未支持",
    r"权衡",
    r"非目标",
    r"范围外",
    r"路线图",
    r"待办",
    r"在制品",
    r"诚实缺口",
    r"未完工",
    r"预览声明",
    r"残余风险",
]

# Placeholder patterns in badge URLs
PLACEHOLDER_DOMAIN_PATTERNS = [
    r"^https?://TODO\b",
    r"^https?://CHANGEME\b",
    r"^https?://example\.(?:com|org|net)\b",
    r"^https?://(?:www\.)?your-(?:org|username|repo|domain)\b",
    r"/username/repo(?:-name)?\b",
    r"/user/repo\b",
    r"/your-org/\b",
    r"/your-username/\b",
    r"/[<{][^>]+[>}]",
]


@dataclass
class Finding:
    check_name: str
    message: str
    line: Optional[int] = None
    blocking: bool = True

    def formatted(self) -> str:
        line_str = f"Line {self.line}: " if self.line is not None else ""
        return f"  - [{self.check_name}] {line_str}{self.message}"


@dataclass
class ProbeReport:
    readme_path: Path
    repo_root: Path
    findings: List[Finding] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    skeleton_info: Optional[str] = None

    @property
    def has_blocking_findings(self) -> bool:
        return any(f.blocking for f in self.findings)


def strip_code_fences(content: str) -> str:
    """Return content with all fenced code blocks replaced by blank lines (preserving line count)."""
    lines = content.splitlines(keepends=True)
    out = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in lines:
        stripped = line.strip()
        if not in_fence:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                in_fence = True
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                out.append("\n")
                continue
            out.append(line)
        else:
            m = re.match(r"^(`{3,}|~{3,})\s*$", stripped)
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len:
                in_fence = False
            out.append("\n")
    return "".join(out)


def check_code_fences(content: str) -> List[Finding]:
    """Check 3: Detect unclosed code fences."""
    findings = []
    lines = content.splitlines()
    in_fence = False
    fence_char = ""
    fence_len = 0
    start_line = 0

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_fence:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                in_fence = True
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                start_line = i
        else:
            m = re.match(r"^(`{3,}|~{3,})\s*$", stripped)
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len:
                in_fence = False

    if in_fence:
        findings.append(
            Finding(
                check_name="code-fences",
                line=start_line,
                message=f"Unclosed code fence (opened with {fence_char * fence_len} at line {start_line}, reached EOF without closing)",
            )
        )
    return findings


def check_dead_links(content: str, readme_path: Path, repo_root: Path) -> List[Finding]:
    """Check 1: Dead local links."""
    findings = []
    text_no_fences = strip_code_fences(content)
    lines = text_no_fences.splitlines()

    # Markdown links [text](target) and <a href="target">
    md_link_re = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
    html_link_re = re.compile(r"""<a\s+[^>]*?href=["']([^"']+)["']""", re.IGNORECASE)

    readme_dir = readme_path.parent.resolve()

    for line_idx, line in enumerate(lines, start=1):
        targets = []
        for m in md_link_re.finditer(line):
            targets.append(m.group(2).strip())
        for m in html_link_re.finditer(line):
            targets.append(m.group(1).strip())

        for target in targets:
            if not target:
                continue
            # Ignore external schemes or anchor-only links
            if target.startswith(("#", "http://", "https://", "mailto:", "data:", "ftp:", "javascript:", "tel:", "<")):
                continue
            # Strip anchor and query parameters
            clean = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not clean:
                continue
            # Normalize path
            # Test resolution relative to repo_root, and also relative to readme_dir
            path_repo = (repo_root / clean).resolve()
            path_readme = (readme_dir / clean).resolve()
            if not path_repo.exists() and not path_readme.exists():
                findings.append(
                    Finding(
                        check_name="dead-links",
                        line=line_idx,
                        message=f"Dead local link: '{target}' (file not found under repo root)",
                    )
                )
    return findings


def check_missing_images(content: str, readme_path: Path, repo_root: Path) -> List[Finding]:
    """Check 2: Missing local image paths."""
    findings = []
    text_no_fences = strip_code_fences(content)
    lines = text_no_fences.splitlines()

    md_img_re = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    html_img_re = re.compile(r"""<img\s+[^>]*?src=["']([^"']+)["']""", re.IGNORECASE)
    html_source_re = re.compile(r"""<source\s+[^>]*?srcset=["']([^"']+)["']""", re.IGNORECASE)

    readme_dir = readme_path.parent.resolve()

    for line_idx, line in enumerate(lines, start=1):
        sources = []
        for m in md_img_re.finditer(line):
            sources.append(m.group(2).strip())
        for m in html_img_re.finditer(line):
            sources.append(m.group(1).strip())
        for m in html_source_re.finditer(line):
            sources.append(m.group(1).strip())

        for src in sources:
            if not src:
                continue
            if src.startswith(("http://", "https://", "data:", "<")):
                continue
            clean = src.split("#", 1)[0].split("?", 1)[0].strip()
            if not clean:
                continue
            path_repo = (repo_root / clean).resolve()
            path_readme = (readme_dir / clean).resolve()
            if not path_repo.exists() and not path_readme.exists():
                findings.append(
                    Finding(
                        check_name="missing-images",
                        line=line_idx,
                        message=f"Missing local image: '{src}' (file not found under repo root)",
                    )
                )
    return findings


def check_badge_domains(content: str) -> List[Finding]:
    """Check 4: Badge URL domain sanity."""
    findings = []
    text_no_fences = strip_code_fences(content)
    lines = text_no_fences.splitlines()

    # Matches [![alt](img_url)](target_url) or <a href="target"><img src="img"></a>
    badge_md_re = re.compile(r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)")
    badge_html_re = re.compile(
        r"""<a\s+[^>]*?href=["']([^"']+)["'][^>]*?>\s*<img\s+[^>]*?src=["']([^"']+)["']""",
        re.IGNORECASE,
    )
    # Also standalone badge images (shields.io, badgen.net, etc.)
    standalone_badge_md_re = re.compile(r"!\[([^\]]*)\]\((https?://[^)]*(?:shields\.io|badgen\.net|badge\.svg)[^)]*)\)")

    for line_idx, line in enumerate(lines, start=1):
        badge_urls = []
        for m in badge_md_re.finditer(line):
            badge_urls.append(m.group(2).strip())  # img
            badge_urls.append(m.group(3).strip())  # link
        for m in badge_html_re.finditer(line):
            badge_urls.append(m.group(1).strip())  # link
            badge_urls.append(m.group(2).strip())  # img
        for m in standalone_badge_md_re.finditer(line):
            badge_urls.append(m.group(2).strip())

        for url in badge_urls:
            # Check for placeholder patterns
            for pat in PLACEHOLDER_DOMAIN_PATTERNS:
                if re.search(pat, url, re.IGNORECASE):
                    findings.append(
                        Finding(
                            check_name="badge-domains",
                            line=line_idx,
                            message=f"Badge URL '{url}' contains invalid or placeholder domain",
                        )
                    )
                    break
            else:
                # Validate URL syntax and host if it is an http(s) URL
                if url.startswith(("http://", "https://")):
                    parsed = urllib.parse.urlparse(url)
                    host = parsed.netloc or ""
                    if not host or "." not in host or host.lower() == "localhost":
                        findings.append(
                            Finding(
                                check_name="badge-domains",
                                line=line_idx,
                                message=f"Badge URL '{url}' has malformed or unresolvable host '{host}'",
                            )
                        )
    return findings


def check_boundary_duplicates(content: str) -> List[Finding]:
    """Check 5: Boundary-phrase duplicate counting."""
    findings = []
    text_no_fences = strip_code_fences(content)
    lines = text_no_fences.splitlines()

    phrase_matches: dict[str, list[int]] = {phrase: [] for phrase in BOUNDARY_PHRASES}

    for line_idx, line in enumerate(lines, start=1):
        line_lower = line.lower()
        for phrase in BOUNDARY_PHRASES:
            # Word boundary check for ASCII phrases, simple substring for Chinese
            if phrase.isascii():
                pattern = rf"\b{re.escape(phrase)}\b"
            else:
                pattern = re.escape(phrase)
            if re.search(pattern, line_lower):
                phrase_matches[phrase].append(line_idx)

    for phrase, matched_lines in phrase_matches.items():
        if len(matched_lines) > 1:
            line_list = ", ".join(str(l) for l in matched_lines)
            findings.append(
                Finding(
                    check_name="boundary-duplicates",
                    line=matched_lines[0],
                    message=f"Boundary phrase '{phrase}' appears {len(matched_lines)} times (lines {line_list}) — claims and boundaries must be stated at most once",
                )
            )
    return findings


def check_honest_gaps(content: str) -> List[Finding]:
    """Check 6: Honest-gap signal presence (detects suspicious completeness)."""
    findings = []
    text_no_fences = strip_code_fences(content)

    found_signals = []
    for pat in HONEST_GAP_PATTERNS:
        match = re.search(pat, text_no_fences, re.IGNORECASE)
        if match:
            found_signals.append(match.group(0))

    if not found_signals:
        findings.append(
            Finding(
                check_name="honest-gaps",
                line=None,
                message="No honest-gap signals found (suspicious completeness: README lacks limitations, caveats, non-goals, trade-offs, or known issues)",
            )
        )
    return findings


def extract_headings(content: str) -> List[Tuple[int, str]]:
    """Extract markdown headings as (level, normalized_title)."""
    headings = []
    text_no_fences = strip_code_fences(content)
    for line in text_no_fences.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if m:
            level = len(m.group(1))
            raw_title = m.group(2).strip()
            # Clean title: strip markdown links, formatting, punctuation
            clean_title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw_title)
            clean_title = re.sub(r"[`*_{}[\]()#+-.!]~", "", clean_title)
            clean_title = re.sub(r"\s+", " ", clean_title).strip().lower()
            if clean_title:
                headings.append((level, clean_title))
    return headings


def compute_skeleton_similarity(h1: List[Tuple[int, str]], h2: List[Tuple[int, str]]) -> float:
    """Compute structural similarity between two heading skeletons."""
    if not h1 and not h2:
        return 1.0
    if not h1 or not h2:
        return 0.0

    seq1 = [f"H{lvl}:{title}" for lvl, title in h1]
    seq2 = [f"H{lvl}:{title}" for lvl, title in h2]

    matcher = difflib.SequenceMatcher(None, seq1, seq2)
    return matcher.ratio()


def check_repo_set(manifest_path: Path, current_readme: Optional[Path] = None, repo_root: Optional[Path] = None) -> Tuple[List[Finding], str]:
    """Check 7: --repo-set cross-repo README skeleton diff."""
    findings = []
    summary_lines = []

    if not manifest_path.is_file():
        return [Finding(check_name="repo-set", message=f"Manifest file not found: {manifest_path}")], ""

    # Parse manifest
    entries: List[Path] = []
    manifest_dir = manifest_path.parent.resolve()
    with manifest_path.open("r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    raw_items: List[str] = []
    # Try JSON format first, then line-by-line
    try:
        data = json.loads(content)
        if isinstance(data, list):
            raw_items = [str(x) for x in data]
    except Exception:
        pass

    if not raw_items:
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            raw_items.append(line)

    for item in raw_items:
        p = Path(item)
        if p.is_absolute():
            entries.append(p)
        elif (manifest_dir / item).exists():
            entries.append((manifest_dir / item).resolve())
        elif repo_root and (repo_root / item).exists():
            entries.append((repo_root / item).resolve())
        elif p.exists():
            entries.append(p.resolve())
        else:
            entries.append((manifest_dir / item).resolve())

    # Resolve README paths
    resolved_readmes: List[Tuple[str, Path, List[Tuple[int, str]]]] = []
    for entry in entries:
        readme_candidate = entry if entry.is_file() else entry / "README.md"
        if readme_candidate.is_file():
            label = entry.parent.name if entry.is_file() else entry.name
            h = extract_headings(readme_candidate.read_text(encoding="utf-8", errors="ignore"))
            resolved_readmes.append((label, readme_candidate, h))

    if len(resolved_readmes) < 2:
        findings.append(
            Finding(
                check_name="repo-set",
                message=f"At least 2 valid READMEs required for repo-set comparison, found {len(resolved_readmes)}",
            )
        )
        return findings, ""

    summary_lines.append(f"[check-readme] Repo-set skeleton analysis ({len(resolved_readmes)} repos):")
    for label, r_path, headings in resolved_readmes:
        summary_lines.append(f"  - {label} ({r_path.name}): {len(headings)} headings")

    summary_lines.append("  Pairwise skeleton isomorphism:")

    # Compare pairwise
    isomorphic_pairs = []
    for i in range(len(resolved_readmes)):
        for j in range(i + 1, len(resolved_readmes)):
            label_a, path_a, h_a = resolved_readmes[i]
            label_b, path_b, h_b = resolved_readmes[j]
            similarity = compute_skeleton_similarity(h_a, h_b)
            status_str = "ISOMORPHIC" if similarity >= 0.85 else "DIVERGENT"
            summary_lines.append(f"  - {label_a} vs {label_b}: {status_str} (similarity: {similarity:.2f})")

            if similarity >= 0.85:
                isomorphic_pairs.append((label_a, label_b, similarity))
                findings.append(
                    Finding(
                        check_name="skeleton-isomorphism",
                        message=f"Repositories '{label_a}' and '{label_b}' have isomorphic README skeletons (similarity: {similarity:.2f})",
                    )
                )

    return findings, "\n".join(summary_lines)


def run_checks(readme_path: Path, repo_root: Path, repo_set_manifest: Optional[Path] = None) -> ProbeReport:
    """Run all applicable static checks on the target README."""
    report = ProbeReport(readme_path=readme_path, repo_root=repo_root)

    if not readme_path.is_file():
        report.findings.append(Finding(check_name="cli", message=f"README file not found: {readme_path}"))
        return report

    content = readme_path.read_text(encoding="utf-8", errors="replace")

    # 1. Dead links
    dead_link_findings = check_dead_links(content, readme_path, repo_root)
    if dead_link_findings:
        report.findings.extend(dead_link_findings)
    else:
        report.passed_checks.append("dead-links")

    # 2. Missing images
    missing_image_findings = check_missing_images(content, readme_path, repo_root)
    if missing_image_findings:
        report.findings.extend(missing_image_findings)
    else:
        report.passed_checks.append("missing-images")

    # 3. Code fence balance
    code_fence_findings = check_code_fences(content)
    if code_fence_findings:
        report.findings.extend(code_fence_findings)
    else:
        report.passed_checks.append("code-fences")

    # 4. Badge URL domain sanity
    badge_findings = check_badge_domains(content)
    if badge_findings:
        report.findings.extend(badge_findings)
    else:
        report.passed_checks.append("badge-domains")

    # 5. Boundary phrase duplicates
    boundary_findings = check_boundary_duplicates(content)
    if boundary_findings:
        report.findings.extend(boundary_findings)
    else:
        report.passed_checks.append("boundary-duplicates")

    # 6. Honest-gap presence
    honest_gap_findings = check_honest_gaps(content)
    if honest_gap_findings:
        report.findings.extend(honest_gap_findings)
    else:
        report.passed_checks.append("honest-gaps")

    # 7. Optional repo-set mode
    if repo_set_manifest:
        repo_set_findings, skeleton_info = check_repo_set(repo_set_manifest, readme_path, repo_root)
        report.skeleton_info = skeleton_info
        if repo_set_findings:
            report.findings.extend(repo_set_findings)
        else:
            report.passed_checks.append("repo-set")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="check-readme.py — stdlib-only python3 static probe for README governance."
    )
    parser.add_argument("readme", nargs="?", default=None, help="Path to README file to verify")
    parser.add_argument("--repo-root", default=None, help="Root directory of repository (default: README parent dir)")
    parser.add_argument("--repo-set", default=None, help="Manifest file for cross-repo skeleton diff")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")

    args = parser.parse_args()

    if not args.readme:
        parser.print_usage(sys.stderr)
        print("Error: Target README path is required.", file=sys.stderr)
        return 2

    readme_path = Path(args.readme).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else readme_path.parent.resolve()
    repo_set_manifest = Path(args.repo_set).resolve() if args.repo_set else None

    if not readme_path.is_file():
        print(f"Error: README file '{readme_path}' does not exist.", file=sys.stderr)
        return 2

    report = run_checks(readme_path, repo_root, repo_set_manifest)

    if args.json:
        data = {
            "target": str(report.readme_path),
            "repo_root": str(report.repo_root),
            "passed": not report.has_blocking_findings,
            "passed_checks": report.passed_checks,
            "findings": [
                {
                    "check": f.check_name,
                    "line": f.line,
                    "message": f.message,
                    "blocking": f.blocking,
                }
                for f in report.findings
            ],
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"[check-readme] Target: {report.readme_path.name} (repo root: {report.repo_root})")
        if report.skeleton_info:
            print(report.skeleton_info)

        if report.passed_checks:
            print("[check-readme] Checks evaluated:")
            for chk in report.passed_checks:
                print(f"  - {chk}: PASS")

        if report.findings:
            print(f"[check-readme] Findings ({len(report.findings)}):")
            for f in report.findings:
                print(f.formatted())
            print(f"[check-readme] Result: FAIL ({len(report.findings)} blocking findings)")
        else:
            print("[check-readme] Result: PASS (0 findings)")

    return 1 if report.has_blocking_findings else 0


if __name__ == "__main__":
    sys.exit(main())
