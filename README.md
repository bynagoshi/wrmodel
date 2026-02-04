# WR Model

## Virtual environments

This project uses two separate virtual environments because `cfbd` and
`nflreadpy` require different Pydantic major versions.

### CFBD environment (Pydantic v1)

```powershell
python -m venv .venv_cfbd
.\.venv_cfbd\Scripts\Activate.ps1
python -m pip install -r requirements_cfbd.txt
```

Run CFBD scripts in this environment (e.g., `pull_data.py`).

### NFL environment (Pydantic v2)

```powershell
python -m venv .venv_nfl
.\.venv_nfl\Scripts\Activate.ps1
python -m pip install -r requirements_nfl.txt
```

Run NFL scripts in this environment (e.g., `load_nfl_data.py`).

