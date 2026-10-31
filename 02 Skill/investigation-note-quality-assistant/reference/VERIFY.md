# Verifying the contract

`reference/CONTRACT-v0.8.md` should be byte-identical to the contract body that was evaluated.
Nothing in this Skill can enforce that at run time — a Skill has no hash gate — so the check is
manual and it is worth doing after any copy, sync or edit.

## Expected values

| Property | Value |
|---|---|
| SHA-256 | `2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363` |
| Length | 31,438 characters (31,641 bytes as shipped, UTF-8) |
| Trailing newline | **none** — the file as shipped does not end in a newline character |
| Content | the contract body as shipped — hash it exactly as-is; no preprocessing needed or expected |

The "frontmatter stripped, whitespace stripped" step already happened when this file was produced
from the source contract. It is provenance information, not something you need to redo — hash the
file exactly as it sits on disk.

**The most likely accidental corruption is not CRLF — it's a silently added trailing newline.**
Many editors auto-insert a final newline on save, and some Git configurations (`autocrlf`, "ensure
newline at end of file") do the same on first commit or checkout. Either will change both the byte
count and the hash without any visible difference in the text. If your hash doesn't match and the
line-ending check below is clean, check for an added trailing newline first.

## Check it

Python, from the Skill's root folder:

```bash
python3 -c "import hashlib,io; t=io.open('reference/CONTRACT-v0.8.md',encoding='utf-8').read(); print(len(t)); print(hashlib.sha256(t.encode('utf-8')).hexdigest())"
```

PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\reference\CONTRACT-v0.8.md
```

Note that `Get-FileHash` hashes the file's raw bytes. It matches the value above only if the file
has LF line endings and no BOM — which is how it ships. If an editor or a Git checkout has
rewritten the line endings to CRLF, `Get-FileHash` will disagree while the Python check above
still passes. The Python check is the authoritative one.

## If it does not match

Do not update the expected hash to make the mismatch go away. Find out which copy changed and
why. An unexplained difference between this file and the evaluated body means the Skill is
carrying an unknown contract, and every statement in `EVIDENCE-LABEL.md` about which object the
evidence attaches to stops being true.
