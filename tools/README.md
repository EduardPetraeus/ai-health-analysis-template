# tools

Standard library Python only; nothing to install.

| File | What |
|---|---|
| `check.py` | Blocks data files, large files and your private terms from commits; checks that every folder has a README naming its files and that every link works; warns about expired status confirmations. `--install-hook` makes it run before every commit |
| `extract_checks.py` | `validate_extract` (validate before writing, fail hard) and `grep_with_positive_control` (no "nothing found" without a control). Used by analysis scripts |
| `config.py` | Reads `config.yaml` without extra packages: `data_path()` for scripts, `private_terms()` for the check |
