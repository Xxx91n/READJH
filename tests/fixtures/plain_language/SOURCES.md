# Plain-language fixture sources

These examples are copied from the throwaway prototype branch
`prototype/plain-readme` (commits `8f6dd6b` and `7fbeaaa`). The prototype took
them from the audited repositories and READJH's own README; the table below
names the exact source for each span. None of them was written for this test.

`cases.json` keeps the exact `source_line` for every example, so the test can
check that each quoted span appears there after markdown links, bold, and code
marks are stripped and whitespace is collapsed. `prototype_excerpt.json` also
stores the hash of each pair's `after` text, so a replacement cannot drift
from the prototype proposal. The full repositories are not copied into this
repo.

## Where each span comes from

| Fixture | Source repo | File | Lines | Commit | Date |
|---|---|---|---|---|---|
| `e1` | `D:/Aworker/6F` | `README.md` | 18 | `dbe463869d89e788199dd6879ff5ee17dd266bef` | 2026-11-06 |
| `e2` | `D:/Aworker/EgressAPIKEY` | `README.md` | 23 | `30e087277381b24715c0a85e44be8bbfe0c6cdd6` | 2026-11-02 |
| `z1` | `D:/Aworker/6F` | `README.zh-CN.md` | 22 | `dbe463869d89e788199dd6879ff5ee17dd266bef` | 2026-11-06 |
| `z2` | `D:/Aworker/maya/maya-mcp-server` | `README.zh-CN.md` | 17 | `89bcbb348da1778edf5ff8b2da93a66a8115925c` | 2026-11-08 |
| `d1` | `D:/Aworker/EgressAPIKEY` | `README.md` | 21 | `30e087277381b24715c0a85e44be8bbfe0c6cdd6` | 2026-11-02 |
| `d2` | `D:/Aworker/6F` | `README.md` | 24 | `dbe463869d89e788199dd6879ff5ee17dd266bef` | 2026-11-06 |
| `d3` | `D:/Aworker/EgressAPIKEY` | `README_CN.md` | 21 | `30e087277381b24715c0a85e44be8bbfe0c6cdd6` | 2026-11-02 |
| `p1` | `D:/Aworker/EgressAPIKEY` | `README_CN.md` | 23 | `30e087277381b24715c0a85e44be8bbfe0c6cdd6` | 2026-11-02 |
| `p2` | `Xxx91n/READJH` | `README.md` | 5-8 | `2547836f65791a4f3459c62dd23fb85dab753fb4` | 2026-11-01 |

## How to re-read a source line

Run this from the repository root, replacing the path, commit, and line:

```bash
git -C "D:/Aworker/6F" show dbe463869d89e788199dd6879ff5ee17dd266bef:README.md | sed -n '18p'
```

For the multi-line `p2` span, use `sed -n '5,8p'` instead.

The recorded `source_line` is the text the main test checks. When a cited
working copy and commit are present, an extra test re-reads the live commit
and compares it with the recorded text. On a machine without those copies,
the extra test skips and the recorded text is still checked. The earlier
prototype checked the live files; this repo keeps that check where it can, but
does not make the whole suite depend on the absolute paths.

## What stays out

- No full repository is copied in.
- No example was rewritten to fit the fixture; the `raw`/`before` strings are
  the prototype's verbatim strings, and the `after` strings are the prototype's
  proposals for the author to review.
- No command from a target README was run.
