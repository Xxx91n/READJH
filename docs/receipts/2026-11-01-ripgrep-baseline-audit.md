# Audit — `BurntSushi/ripgrep` (Ticket #7, human baseline)

> `audit` mode (`ROUTE → TRUTH → RESTRUCTURE → VERIFY`, `SKILL.md` §3) on a
> shallow clone of `https://github.com/BurntSushi/ripgrep`. Role: **human
> baseline** — a widely-recognized human-written README used to show what the
> pipeline reports on human-authored prose. Diagnose-only: zero writes.

- **Run date:** 2026-11-01, Git Bash, Windows host.
- **Target:** `D:\Aworker\tmp\readjh-acceptance\ripgrep` — HEAD `91f5d22ef48bde459d90a8c7dbeab416e97d0f2b` (`master`), shallow clone (`--depth 1`; history truncated — tier evidence limited to this commit + repo docs).
- **Primary README:** `README.md` (541 lines, EN); **companion localized README:** none (translations live off-repo per `README.md:535-541`).
- **Run parameters:** mode `audit`; `--repo-set` not passed (check 7 `N/A`); **intensity tier `lite`** — verified author voice: the README itself is first-person-authored ("my blog", "my email address", candid N.B. notes like the Ubuntu-snap paragraph `:376-379`), and `AI_POLICY.md` + `CONTRIBUTING.md` carry the maintainer's voice; shallow history limits the sample to `91f5d22` + docs.

## 1. `ROUTE`

| Check | Result |
|---|---|
| Roots #1/#2 | `$AGENT_SKILLS_DIR` unset; `.agents/skills/` absent in target → trust gate not triggered |
| Root #3 `readme-crafter-skill` | canonical dir; frontmatter `name:` exact; 5/5 required files |
| README tracked/clean | `ls-files --error-unmatch` ok; `status --porcelain` empty |
| Baseline | `files=226 tree_sha256=b2e214e37e82790417d335c1354da860b44d196661889fd8fe3260d17ac25c0c`; `git status --porcelain --ignored` empty (clean shallow clone) |

## 2. `TRUTH`

```text
$ python -s -E -B -X utf8 ~/.agents/skills/readme-crafter-skill/scripts/scan-project.py "D:/Aworker/tmp/readjh-acceptance/ripgrep"
exit 0 — README INTEGRITY SIGNALS: 541 lines, 0 missing local refs (3 refs: CHANGELOG/FAQ/GUIDE);
LICENSE & TRUST: "License file: —";
RISK SUMMARY: "No obvious README-to-repo mismatches detected by the scanner".
```

- **Project type:** CLI Tool (Rust, `rg`). **Distribution posture:** Published Package (crates.io + every-OS package manager + GitHub binary archives).
- **Claim verification (verified):** `cargo install ripgrep` ↔ `Cargo.toml` name `ripgrep`; build/test commands real (`cargo build --release`, `cargo test --all` ↔ `crates/`, `tests/`); license claim "Dual-licensed under MIT or the UNLICENSE" (`:15`) ↔ `LICENSE-MIT` + `UNLICENSE` + `COPYING` present; `GUIDE.md`/`FAQ.md`/`CHANGELOG.md` resolve; binary name `rg` ↔ crate. External claims (crates.io, brew/ports registry entries, blog benchmarks) are registry-level facts marked verifiable-externally, not executed.
- **README commands not executed:** all install/build/test commands (`:246-513`) — `"needs manual verification"`.

### Findings (TRUTH)

| Severity | Finding | Receipt |
|---|---|---|
| LOW | Scanner "License file: —" — the repo ships `LICENSE-MIT` + `UNLICENSE` + `COPYING` (unconventional naming), so the scanner's exact-name check misses it while the README's dual-license claim is itself accurate. Scanner-context finding, not a README defect. | `ls` root vs `README.md:15` |

## 3. `RESTRUCTURE` (diagnose-only, `lite` tier)

| Severity | Finding | Receipt |
|---|---|---|
| LOW | **Front-page scope:** a 541-line README with ~270 lines of per-distro install recipes (`:233-448`) — this is the CLI-tool convention the rules encode (README as landing + install matrix for a tool published through every package manager); the `lite` tier plus §4.2 shape rule keeps it. Not a defect; noted as the contrast point for the comparison. | `README.md:233-448` |
| N/A — verified | **Zero AI tells.** No generation traces, no HTML scaffolding, no badges-beyond-facts, no self-attestation — instead a *disclaimer of the single benchmark* ("a single benchmark is never enough!" `:47`), candid caveats ("not ubiquitous", "not POSIX", "Please file a bug report!"), honest scope ("rudimentary support"), and calibrated performance claims with named corpus + machine. No ban-list vocabulary clusters. Skeleton follows the CLI-tool convention (what → why → benchmarks → install → build → related). | full-file read |

## 4. `VERIFY`

```text
$ python -B scripts/check-readme.py "D:/Aworker/tmp/readjh-acceptance/ripgrep/README.md" --repo-root "D:/Aworker/tmp/readjh-acceptance/ripgrep"
exit 1 — 2 dead-links findings (real broken fragments):
  Line 29:  'FAQ.md#complete' (no anchor '#complete' in FAQ.md)
  Line 120: 'FAQ.md#posix4ever' (no anchor '#posix4ever' in FAQ.md)
other five checks PASS; repo-set: N/A.
```

The two findings are **genuinely dead fragment links in the human README** — the probe catches real defects regardless of authorship. `honest-gaps` PASSED: the "Why shouldn't I use ripgrep?" section is exactly the limitation signal the check looks for.

Checklist (§§1–8): §1 PASS (probe ran, exit 1 findings recorded); §2 PASS; §3 PASS (first screen: name + one-liner + badges + dual license + nav links); §4 PASS (boundaries once each); §5 `N/A`; §6 PASS (zero traces); §7 PASS (zero AI tells at `lite`); §8 PASS (zero writes).

**Zero-write verification:** post-run `files=226 tree_sha256=b2e214e3…25c0c` — identical; `git status` clean pre/post.

## 5. Three-line delivery report

```text
[Conclusion]: FAIL — audit on ripgrep/README.md (intensity tier: lite); audit completed; findings: HIGH 0 / MEDIUM 0 / LOW 1 + 2 probe dead-links; zero AI tells found (baseline behaved as expected); 0 files modified.
[Receipts]: scan-project.py -> exit 0 (license file missed: unconventional LICENSE-MIT+UNLICENSE+COPYING naming); check-readme.py -> exit 1: dead-links x2 (FAQ.md#complete line 29, FAQ.md#posix4ever line 120 — real broken fragments), other 5 checks PASS incl. honest-gaps; LOW: 270-line per-distro install matrix (CLI-tool convention, kept); snapshot 226 files identical pre/post.
[Residual risk]: README commands need manual verification — all package-manager install lines and cargo build/test; external registry/blog/crates.io links unfetched offline; shallow clone limits claim-vs-history checks.
```

## 6. Discrepancies

| # | Severity | Discrepancy |
|---|---|---|
| D1 | LOW | `scan-project.py` "License file: —" misses multi-license repos (`LICENSE-MIT`/`UNLICENSE`/`COPYING`) — same context-artifact class as EgressAPIKEY's `.env.example` flag. |
