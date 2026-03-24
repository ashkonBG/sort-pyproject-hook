# sort-pyproject-hook

Sorts array sections in `pyproject.toml` (case-insensitive).
By default sorts `dependencies` and `dev`, but sections are configurable via `--sections`.

## Local run

```bash
python sort_pyproject_hook.py pyproject.toml
python sort_pyproject_hook.py --check --diff pyproject.toml
python sort_pyproject_hook.py --sections dependencies dev optional-dependencies pyproject.toml
```
