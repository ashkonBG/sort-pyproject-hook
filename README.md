# sort-pyproject-hook

Sorts array sections in `pyproject.toml` (case-insensitive) and normalizes indentation to four spaces.
By default, sorts `dependencies` and `dev`, but sections are configurable via `--sections`.

## Arguments

| Argument     | Type       | Default            | Description                                                                              |
|--------------|------------|--------------------|------------------------------------------------------------------------------------------|
| `files`      | positional | `pyproject.toml`   | Files to process. Passed automatically by pre-commit. Overrides the default if provided. |
| `--sections` | optional   | `dependencies,dev` | Comma-separated section names to sort. Errors if a section is not found (catches typos). |
| `--check`    | flag       | off                | Don't write changes; exit 1 if any file needs sorting.                                   |
| `--diff`     | flag       | off                | Print a unified diff of changes to stdout.                                               |

## Pre-commit usage

Add to your `.pre-commit-config.yaml`:

### Default (sorts `dependencies` and `dev`)

```yaml
repos:
  - repo: https://github.com/your-username/sort-pyproject-hook
    rev: v0.1.0
    hooks:
      - id: sort-pyproject
```

### Custom sections (comma-separated)

```yaml
repos:
  - repo: https://github.com/your-username/sort-pyproject-hook
    rev: v0.1.0
    hooks:
      - id: sort-pyproject
        args: [ "--sections", "dependencies,dev,optional-dependencies" ]
```

### Single section only

```yaml
repos:
  - repo: https://github.com/your-username/sort-pyproject-hook
    rev: v0.1.0
    hooks:
      - id: sort-pyproject
        args: [ "--sections", "dev" ]
```

### Check-only mode (CI, no writes)

```yaml
repos:
  - repo: https://github.com/your-username/sort-pyproject-hook
    rev: v0.1.0
    hooks:
      - id: sort-pyproject
        args: [ "--check", "--diff" ]
```

### Custom file pattern

By default, pre-commit passes matching files to the hook automatically.
You can control which files the hook runs on using pre-commit's own `files` regex filter:

```yaml
repos:
  - repo: https://github.com/your-username/sort-pyproject-hook
    rev: v0.1.0
    hooks:
      - id: sort-pyproject
        files: ^pyproject\.toml$
```

To match `pyproject.toml` in subdirectories as well:

```yaml
repos:
  - repo: https://github.com/your-username/sort-pyproject-hook
    rev: v0.1.0
    hooks:
      - id: sort-pyproject
        files: (^|/)pyproject\.toml$
```

> **Note:** The `files` filter is evaluated by pre-commit *before* the hook runs.
> If no files match the pattern, pre-commit skips the hook entirely with
> `(no files to check) Skipped` — the hook script is never invoked.

## Local run

```bash
# Default: sorts "dependencies" and "dev" in pyproject.toml
python hooks/sort_pyproject.py

# Custom file
python hooks/sort_pyproject.py path/to/pyproject.toml

# Custom sections
python hooks/sort_pyproject.py --sections dependencies,dev,optional-dependencies

# Check only with diff output
python hooks/sort_pyproject.py --check --diff
```
