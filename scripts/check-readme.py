#!/usr/bin/env python3
"""scripts/check-readme.py — stdlib-only python3 static probe for README governance.

Seven static checks:
1. dead local links (markdown links & <a> tags pointing to missing local files, including badge
   link targets) and broken fragments (same-file '#anchor' and 'file.md#anchor' resolved
   against the target's heading-derived and explicit anchors)
2. missing image paths (markdown images, <img> tags, and <source> srcset)
3. code-fence imbalance (unclosed or mismatched backtick/tilde code fences)
4. badge URL domain sanity (valid hosts, flags placeholders e.g. TODO, example.com, username/repo)
5. boundary-phrase duplicate counting (ensures boundaries & disclaimers are stated at most once)
6. honest-gap signal presence (detects suspicious completeness when limitations/caveats/gaps are absent)
7. --repo-set cross-repo README skeleton diff (detects cross-repo skeleton isomorphism)

CLI contract:
    python3 scripts/check-readme.py <readme> [--repo-root <dir>] [--repo-set <manifest>]
                                           [--checks dead-links,missing-images,...]
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
class RepoSkeleton:
    label: str
    path: Path
    headings: List[Tuple[int, str]]


@dataclass
class ProbeReport:
    readme_path: Path
    repo_root: Path
    findings: List[Finding] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    skeleton_info: Optional[str] = None
    selected_checks: Optional[List[str]] = None

    @property
    def has_blocking_findings(self) -> bool:
        return any(f.blocking for f in self.findings)


def _match_fence_open(line: str) -> Optional[Tuple[str, int]]:
    """Match opening of a code fence (``` or ~~~)."""
    m = re.match(r"^(`{3,}|~{3,})", line.strip())
    if m:
        return m.group(1)[0], len(m.group(1))
    return None


def _match_fence_close(line: str, fence_char: str, fence_len: int) -> bool:
    """Check if line closes current code fence."""
    m = re.match(r"^(`{3,}|~{3,})\s*$", line.strip())
    return bool(m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len)


def strip_code_fences(content: str) -> str:
    """Return content with all fenced code blocks replaced by blank lines (preserving line count)."""
    lines = content.splitlines(keepends=True)
    out = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in lines:
        if not in_fence:
            fence = _match_fence_open(line)
            if fence:
                in_fence = True
                fence_char, fence_len = fence
                out.append("\n")
                continue
            out.append(line)
        else:
            if _match_fence_close(line, fence_char, fence_len):
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
        if not in_fence:
            fence = _match_fence_open(line)
            if fence:
                in_fence = True
                fence_char, fence_len = fence
                start_line = i
        else:
            if _match_fence_close(line, fence_char, fence_len):
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


def _resolve_local_path(target: str, readme_dir: Path, repo_root: Path) -> Optional[Path]:
    """Resolve and verify existence of a local target path against readme_dir or repo_root, ensuring containment."""
    raw = target.strip()
    if not raw:
        return None
    if raw.startswith("<") and ">" in raw:
        raw = raw[1:raw.find(">")].strip()
    if raw.startswith(("#", "http://", "https://", "mailto:", "data:", "ftp:", "javascript:", "tel:", "//")):
        return None
    title = re.match(
        r"""^(\S+)\s+(?:"(?:\\.|[^"])*"|'(?:\\.|[^'])*'|\((?:\\.|[^)])*\))\s*$""",
        raw,
    )
    clean = title.group(1) if title else raw
    clean = clean.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean or clean.startswith("//"):
        return None

    is_root_relative = clean.startswith("/")
    decoded = urllib.parse.unquote(clean.lstrip("/"))
    if not decoded and not is_root_relative:
        return None

    p_root = repo_root.resolve()
    p_base = p_root if is_root_relative else readme_dir.resolve()
    p_resolved = (p_base / decoded).resolve() if decoded else p_root

    # Containment check: path must be strictly contained within repo_root
    try:
        p_resolved.relative_to(p_root)
    except ValueError:
        return None

    return p_resolved if p_resolved.exists() else None


def extract_all_link_targets(line: str) -> List[str]:
    """Extract link targets from markdown links (including nested badge links) and HTML <a> tags."""
    targets = []
    # Nested markdown link regex: matches [text](target), allowing nested [alt](img) in text
    md_link_re = re.compile(r"(?<!!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]+)\)")
    html_link_re = re.compile(r"""<a\s+[^>]*?href=["']([^"']+)["']""", re.IGNORECASE)

    for m in md_link_re.finditer(line):
        targets.append(m.group(2).strip())
    for m in html_link_re.finditer(line):
        targets.append(m.group(1).strip())
    return targets


def _github_slug(heading: str) -> str:
    """Derive a GitHub-style fragment anchor from a heading line body."""
    t = re.sub(r"`+([^`]*)`+", r"\1", heading)          # inline code
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)    # links/images -> text
    t = re.sub(r"[*~]", "", t)                           # *, ~ emphasis markers
    # Paired leading/trailing underscores are emphasis; interior ones stay
    # (my_func, _private keep their underscores like GitHub's renderer).
    t = re.sub(r"^_+(.+?)_+$", r"\1", t)
    t = t.lower()
    t = re.sub(r"[^\w\- ]", "", t)                       # keep word chars (incl. CJK), hyphens, spaces
    return t.replace(" ", "-")


def _code_span_end(text: str, start: int) -> Optional[int]:
    """If a backtick code span opens at `start`, return the index just past its
    closing run. GFM: the closing run must be exactly the opening length; an
    unmatched opener is literal text, so return None."""
    tick_end = start
    while tick_end < len(text) and text[tick_end] == "`":
        tick_end += 1
    tlen = tick_end - start
    k = text.find("`", tick_end)
    while k != -1:
        k2 = k
        while k2 < len(text) and text[k2] == "`":
            k2 += 1
        if k2 - k == tlen:
            return k2
        k = text.find("`", k2)
    return None


def _strip_html_comments(text: str) -> str:
    """Remove HTML comment spans so commented-out markup never registers as
    real, while keeping rendered text around inline comments. Code-span aware:
    `<!--` inside backticks is literal text, not a comment. Newlines inside
    comments are preserved to keep line numbers stable; an unclosed comment
    swallows the rest of the document, like the renderer."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        cstart = text.find("<!--", i)
        tstart = text.find("`", i)
        if cstart == -1 and tstart == -1:
            out.append(text[i:])
            break
        if tstart != -1 and (cstart == -1 or tstart < cstart):
            # A backtick run comes first — emit the whole code span (or the
            # literal unmatched run) so `<!--` inside it stays text.
            span_end = _code_span_end(text, tstart)
            if span_end is None:
                run_end = tstart
                while run_end < n and text[run_end] == "`":
                    run_end += 1
                out.append(text[i:run_end])
                i = run_end
                continue
            out.append(text[i:span_end])
            i = span_end
            continue
        out.append(text[i:cstart])
        end = text.find("-->", cstart + 4)
        if end == -1:
            out.append("\n" * text[cstart:].count("\n"))
            break
        out.append("\n" * text[cstart:end + 3].count("\n"))
        i = end + 3
    return "".join(out)


def _strip_inline_code(text: str) -> str:
    """Blank the contents of inline code spans (fences already stripped), so
    markup shown inside backticks is never treated as rendered. Newlines are
    preserved to keep line numbers stable; an unmatched backtick run is
    literal text per GFM and is left alone."""
    out = []
    i = 0
    while True:
        start = text.find("`", i)
        if start == -1:
            out.append(text[i:])
            break
        end = _code_span_end(text, start)
        if end is None:
            out.append(text[i:])
            break
        out.append(text[i:start])
        out.append("".join("\n" if c == "\n" else " " for c in text[start:end]))
        i = end
    return "".join(out)


def _markdown_anchor_ids(path: Path) -> Optional[set]:
    """Collect valid fragment anchors in a markdown file: rendered id/name
    attributes on HTML tags and GitHub-slugified heading anchors (indented
    ATX, Setext, duplicate-suffixed). Returns None on read error."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    # Anchors only from rendered content: fenced code stripped first (an
    # unclosed comment inside a fence is just code), then comment spans
    # removed — code-span aware, so a `<!--` inside backticks is literal.
    visible = _strip_html_comments(strip_code_fences(text))
    lines = visible.splitlines()

    # Explicit anchors: parse each HTML tag attribute-by-attribute so id=
    # inside another attribute's value cannot fake an anchor (e.g.
    # <span title='id="ghost"'>). Any tag's `id` counts; `name` only on <a>.
    attr_re = re.compile(
        r"""([^\s=/>]+)\s*(?:=\s*("[^"]*"|'[^']*'|[^\s>]+))?"""
    )
    ids = set()
    for tag in re.findall(r"<[^>]+>", _strip_inline_code(visible)):
        m = re.match(r"</?\s*([a-zA-Z][^\s/>]*)", tag)
        if not m:
            continue
        tag_name = m.group(1).lower()
        for attr in attr_re.finditer(tag, m.end()):
            attr_name = attr.group(1).lower()
            attr_val = (attr.group(2) or "").strip("\"'")
            if attr_name == "id" and attr_val:
                ids.add(attr_val)
            elif attr_name == "name" and tag_name == "a" and attr_val:
                ids.add(attr_val)
    slug_counts: dict = {}
    generated: set = set()

    def _register(heading: str) -> None:
        slug = _github_slug(heading)
        if not slug:
            return
        n = slug_counts.get(slug, 0)
        candidate = slug if n == 0 else f"{slug}-{n}"
        while candidate in generated or candidate in ids:
            n += 1
            candidate = f"{slug}-{n}"
        slug_counts[slug] = n + 1
        generated.add(candidate)
        ids.add(candidate)

    for i, line in enumerate(lines):
        # ATX heading (0-3 leading spaces per GFM)
        m = re.match(r"^ {0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            _register(m.group(1))
            continue
        # Setext heading: plain text line followed by === or --- underline.
        # Only real block markers are excluded — "> " blockquote, "# " ATX,
        # "* " / "+ " / "- " unordered markers, "1. " ordered markers, and
        # thematic-break-only lines. Marker chars inside text (**Note**,
        # 2026 Overview, -foo) stay valid heading text.
        if (
            line.strip()
            and re.match(
                r"^ {0,3}(?!>|#{1,6}(?:\s|$)|[*+\-](?:\s|$)|"
                r"\d{1,9}[.)](?:\s|$)|[*\-_ ]*$)\S",
                line,
            )
            and i + 1 < len(lines)
            and re.match(r"^ {0,3}(=+|-+)\s*$", lines[i + 1])
        ):
            _register(line.strip())
    return ids


def _extract_fragment(target: str) -> Optional[str]:
    """Return the URL fragment of a link target (without '#'), or None."""
    t = target.strip()
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1].strip()
    # Drop an optional title ("..." / '...' / (...) after whitespace)
    t = re.split(r"\s", t, 1)[0]
    if "#" not in t:
        return None
    frag = t.split("#", 1)[1]
    frag = urllib.parse.unquote(frag)
    return frag if frag else None


def check_dead_links(content: str, readme_path: Path, repo_root: Path) -> List[Finding]:
    """Check 1: Dead local links and broken fragments."""
    findings = []
    # Rendered content only: links inside fenced code, inline code, or HTML
    # comments are not clickable and never resolve.
    text_no_fences = _strip_inline_code(
        _strip_html_comments(strip_code_fences(content))
    )
    lines = text_no_fences.splitlines()
    readme_dir = readme_path.parent.resolve()
    own_anchors: Optional[set] = None

    for line_idx, line in enumerate(lines, start=1):
        targets = extract_all_link_targets(line)
        for target in targets:
            if not target:
                continue
            clean_target = target.strip()
            if clean_target.startswith("<") and clean_target.endswith(">"):
                clean_target = clean_target[1:-1].strip()

            # Ignore external schemes; anchor-only links get fragment validation below
            if clean_target.startswith(("http://", "https://", "mailto:", "data:", "ftp:", "javascript:", "tel:", "//")):
                continue

            fragment = _extract_fragment(target)

            if clean_target.startswith("#"):
                # Same-document fragment: validate against this file's anchors
                if fragment:
                    if own_anchors is None:
                        own_anchors = _markdown_anchor_ids(readme_path)
                    if own_anchors is not None and fragment not in own_anchors:
                        findings.append(
                            Finding(
                                check_name="dead-links",
                                line=line_idx,
                                message=f"Broken fragment link: '{target}' (no anchor '#{fragment}' in this file)",
                            )
                        )
                continue

            resolved = _resolve_local_path(target, readme_dir, repo_root)
            if resolved is None:
                findings.append(
                    Finding(
                        check_name="dead-links",
                        line=line_idx,
                        message=f"Dead local link: '{target}' (file not found under repo root)",
                    )
                )
                continue

            # File resolves — validate the fragment against the target's anchors
            if fragment and resolved.is_file() and resolved.suffix.lower() in (".md", ".markdown"):
                target_anchors = _markdown_anchor_ids(resolved)
                if target_anchors is not None and fragment not in target_anchors:
                    findings.append(
                        Finding(
                            check_name="dead-links",
                            line=line_idx,
                            message=f"Broken fragment link: '{target}' (no anchor '#{fragment}' in {resolved.name})",
                        )
                    )
    return findings


def parse_srcset_urls(raw_srcset: str) -> List[str]:
    """Parse candidate image URLs from a srcset attribute following WHATWG HTML rules."""
    urls = []
    i = 0
    n = len(raw_srcset)

    while i < n:
        # Skip leading whitespace
        while i < n and raw_srcset[i].isspace():
            i += 1
        if i >= n:
            break

        # Collect URL characters until whitespace
        url_start = i
        while i < n and not raw_srcset[i].isspace():
            i += 1
        url = raw_srcset[url_start:i]

        # If URL ends with comma, it was comma-delimited without descriptors
        if url.endswith(","):
            urls.append(url[:-1])
            continue

        urls.append(url)

        # Skip descriptor(s) until next unparenthesized comma or EOF
        in_paren = False
        while i < n:
            ch = raw_srcset[i]
            if ch == "(":
                in_paren = True
            elif ch == ")":
                in_paren = False
            elif ch == "," and not in_paren:
                i += 1
                break
            i += 1

    return urls


def check_missing_images(content: str, readme_path: Path, repo_root: Path) -> List[Finding]:
    """Check 2: Missing local image paths."""
    findings = []
    text_no_fences = _strip_inline_code(
        _strip_html_comments(strip_code_fences(content))
    )
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
            raw_srcset = m.group(1).strip()
            for candidate_url in parse_srcset_urls(raw_srcset):
                if candidate_url:
                    sources.append(candidate_url)

        for src in sources:
            if not src:
                continue
            clean_src = src.strip()
            if clean_src.startswith("<") and clean_src.endswith(">"):
                clean_src = clean_src[1:-1].strip()

            if clean_src.startswith(("http://", "https://", "data:", "//")):
                continue

            resolved = _resolve_local_path(src, readme_dir, repo_root)
            if resolved is None:
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

    badge_md_re = re.compile(r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)")
    badge_html_re = re.compile(
        r"""<a\s+[^>]*?href=["']([^"']+)["'][^>]*?>\s*<img\s+[^>]*?src=["']([^"']+)["']""",
        re.IGNORECASE,
    )
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

        for raw_url in badge_urls:
            url = raw_url.strip()
            if url.startswith("<") and url.endswith(">"):
                url = url[1:-1].strip()
            if not url:
                continue

            test_url = f"https:{url}" if url.startswith("//") else url
            # Check for placeholder patterns
            for pat in PLACEHOLDER_DOMAIN_PATTERNS:
                if re.search(pat, test_url, re.IGNORECASE):
                    findings.append(
                        Finding(
                            check_name="badge-domains",
                            line=line_idx,
                            message=f"Badge URL '{raw_url}' contains invalid or placeholder domain",
                        )
                    )
                    break
            else:
                # Validate URL syntax and host if it is an http(s) URL or scheme-relative // URL
                if test_url.startswith(("http://", "https://")):
                    parsed = urllib.parse.urlparse(test_url)
                    host = parsed.netloc or ""
                    if not host or "." not in host or host.lower() == "localhost":
                        findings.append(
                            Finding(
                                check_name="badge-domains",
                                line=line_idx,
                                message=f"Badge URL '{raw_url}' has malformed or unresolvable host '{host}'",
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
            for _ in re.finditer(pattern, line_lower):
                phrase_matches[phrase].append(line_idx)

    for phrase, matched_lines in phrase_matches.items():
        if len(matched_lines) > 1:
            line_list = ", ".join(str(line_no) for line_no in matched_lines)
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
            clean_title = re.sub(r"[`*_{}[\]()#+\-.!~]", "", clean_title)
            clean_title = re.sub(r"\s+", " ", clean_title).strip().lower()
            if clean_title:
                headings.append((level, clean_title))
    return headings


def compute_skeleton_similarity(
    headings_a: List[Tuple[int, str]], headings_b: List[Tuple[int, str]]
) -> float:
    """Compute structural similarity between two heading skeletons.

    Considers both hierarchy structure (levels) and normalized section topics,
    catching skeleton isomorphism even when exact titles are lightly varied.
    """
    if not headings_a and not headings_b:
        return 1.0
    if not headings_a or not headings_b:
        return 0.0

    seq1_full = [f"H{lvl}:{title}" for lvl, title in headings_a]
    seq2_full = [f"H{lvl}:{title}" for lvl, title in headings_b]
    matcher_full = difflib.SequenceMatcher(None, seq1_full, seq2_full)
    ratio_full = matcher_full.ratio()

    # Also compare structural level skeleton
    seq1_lvl = [f"H{lvl}" for lvl, _ in headings_a]
    seq2_lvl = [f"H{lvl}" for lvl, _ in headings_b]
    matcher_lvl = difflib.SequenceMatcher(None, seq1_lvl, seq2_lvl)
    ratio_lvl = matcher_lvl.ratio()

    # High full similarity indicates verbatim skeleton isomorphism
    if ratio_full >= 0.85:
        return ratio_full
    # Identical level structure with high topic overlap indicates skeleton isomorphism
    if ratio_lvl >= 0.95 and ratio_full >= 0.60:
        return max(ratio_full, 0.85)

    return ratio_full


def check_repo_set(
    manifest_path: Path, current_readme: Optional[Path] = None, repo_root: Optional[Path] = None
) -> Tuple[List[Finding], str]:
    """Check 7: --repo-set cross-repo README skeleton diff."""
    findings = []
    summary_lines = []

    if not manifest_path.is_file():
        return [Finding(check_name="repo-set", message=f"Manifest file not found: {manifest_path}")], ""

    entries: List[Path] = []
    manifest_dir = manifest_path.parent.resolve()
    with manifest_path.open("r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    raw_items: List[str] = []
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

    # Resolve README skeletons
    resolved_readmes: List[RepoSkeleton] = []
    seen_paths = set()
    for entry in entries:
        readme_candidate = entry if entry.is_file() else entry / "README.md"
        if readme_candidate.is_file():
            res_path = readme_candidate.resolve()
            if res_path in seen_paths:
                continue
            seen_paths.add(res_path)
            label = entry.parent.name if entry.is_file() else entry.name
            headings = extract_headings(res_path.read_text(encoding="utf-8", errors="ignore"))
            resolved_readmes.append(RepoSkeleton(label=label, path=res_path, headings=headings))
        else:
            findings.append(
                Finding(check_name="repo-set", message=f"Manifest entry has no README: {entry}")
            )

    # Include target CLI README if not already in manifest
    if current_readme and current_readme.is_file():
        cur_res = current_readme.resolve()
        if cur_res not in seen_paths:
            seen_paths.add(cur_res)
            cur_label = cur_res.parent.name
            headings = extract_headings(cur_res.read_text(encoding="utf-8", errors="ignore"))
            resolved_readmes.insert(0, RepoSkeleton(label=cur_label, path=cur_res, headings=headings))

    if len(resolved_readmes) < 2:
        findings.append(
            Finding(
                check_name="repo-set",
                message=f"At least 2 valid READMEs required for repo-set comparison, found {len(resolved_readmes)}",
            )
        )
        return findings, ""

    summary_lines.append(f"[check-readme] Repo-set skeleton analysis ({len(resolved_readmes)} repos):")
    for skeleton in resolved_readmes:
        summary_lines.append(f"  - {skeleton.label} ({skeleton.path.name}): {len(skeleton.headings)} headings")

    summary_lines.append("  Pairwise skeleton isomorphism:")

    # Compare pairwise
    for i in range(len(resolved_readmes)):
        for j in range(i + 1, len(resolved_readmes)):
            skeleton_a = resolved_readmes[i]
            skeleton_b = resolved_readmes[j]
            similarity = compute_skeleton_similarity(skeleton_a.headings, skeleton_b.headings)
            status_str = "ISOMORPHIC" if similarity >= 0.85 else "DIVERGENT"
            summary_lines.append(f"  - {skeleton_a.label} vs {skeleton_b.label}: {status_str} (similarity: {similarity:.2f})")

            if similarity >= 0.85:
                findings.append(
                    Finding(
                        check_name="skeleton-isomorphism",
                        message=f"Repositories '{skeleton_a.label}' and '{skeleton_b.label}' have isomorphic README skeletons (similarity: {similarity:.2f})",
                    )
                )

    return findings, "\n".join(summary_lines)


ALL_CHECKS = [
    "dead-links",
    "missing-images",
    "code-fences",
    "badge-domains",
    "boundary-duplicates",
    "honest-gaps",
]


def run_checks(
    readme_path: Path,
    repo_root: Path,
    repo_set_manifest: Optional[Path] = None,
    checks: Optional[List[str]] = None,
) -> ProbeReport:
    """Run the selected static checks on the target README (default: all)."""
    selected = checks if checks is not None else list(ALL_CHECKS)
    report = ProbeReport(readme_path=readme_path, repo_root=repo_root)
    report.selected_checks = list(selected)

    if not readme_path.is_file():
        report.findings.append(Finding(check_name="cli", message=f"README file not found: {readme_path}"))
        return report

    content = readme_path.read_text(encoding="utf-8", errors="replace")

    # 1. Dead links
    if "dead-links" in selected:
        dead_link_findings = check_dead_links(content, readme_path, repo_root)
        if dead_link_findings:
            report.findings.extend(dead_link_findings)
        else:
            report.passed_checks.append("dead-links")

    # 2. Missing images
    if "missing-images" in selected:
        missing_image_findings = check_missing_images(content, readme_path, repo_root)
        if missing_image_findings:
            report.findings.extend(missing_image_findings)
        else:
            report.passed_checks.append("missing-images")

    # 3. Code fence balance
    if "code-fences" in selected:
        code_fence_findings = check_code_fences(content)
        if code_fence_findings:
            report.findings.extend(code_fence_findings)
        else:
            report.passed_checks.append("code-fences")

    # 4. Badge URL domain sanity
    if "badge-domains" in selected:
        badge_findings = check_badge_domains(content)
        if badge_findings:
            report.findings.extend(badge_findings)
        else:
            report.passed_checks.append("badge-domains")

    # 5. Boundary phrase duplicates
    if "boundary-duplicates" in selected:
        boundary_findings = check_boundary_duplicates(content)
        if boundary_findings:
            report.findings.extend(boundary_findings)
        else:
            report.passed_checks.append("boundary-duplicates")

    # 6. Honest-gap presence
    if "honest-gaps" in selected:
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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="check-readme.py — stdlib-only python3 static probe for README governance."
    )
    parser.add_argument("readme", nargs="?", default=None, help="Path to README file to verify")
    parser.add_argument("--repo-root", default=None, help="Root directory of repository (default: README parent dir)")
    parser.add_argument("--repo-set", default=None, help="Manifest file for cross-repo skeleton diff")
    parser.add_argument(
        "--checks",
        default=None,
        help="Comma-separated subset of checks to run (default: all). "
        f"Names: {', '.join(ALL_CHECKS)}. Used by VERIFY to scope probes, "
        "e.g. --checks dead-links,missing-images on docs/ migration destinations.",
    )

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

    if repo_set_manifest and not repo_set_manifest.is_file():
        print(f"Error: Manifest file '{repo_set_manifest}' does not exist.", file=sys.stderr)
        return 2

    selected_checks: Optional[List[str]] = None
    if args.checks is not None:
        # An explicit --checks whose normalized selection is empty — whether
        # "" or ",," — is rejected; an omitted flag means "all checks".
        selected_checks = []
        for name in args.checks.split(","):
            name = name.strip()
            if name and name not in selected_checks:
                selected_checks.append(name)
        if not selected_checks:
            print(
                "Error: --checks was given but selects no checks "
                f"(valid: {', '.join(ALL_CHECKS)})",
                file=sys.stderr,
            )
            return 2
        unknown = [c for c in selected_checks if c not in ALL_CHECKS]
        if unknown:
            print(
                f"Error: unknown check name(s): {', '.join(unknown)} "
                f"(valid: {', '.join(ALL_CHECKS)})",
                file=sys.stderr,
            )
            return 2

    report = run_checks(readme_path, repo_root, repo_set_manifest, checks=selected_checks)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print(f"[check-readme] Target: {report.readme_path.name} (repo root: {report.repo_root})")
    if report.skeleton_info:
        print(report.skeleton_info)

    if report.selected_checks is not None and report.selected_checks != ALL_CHECKS:
        skipped = [c for c in ALL_CHECKS if c not in report.selected_checks]
        if skipped:
            print(f"[check-readme] Checks not selected: {', '.join(skipped)}")

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
