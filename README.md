# timetasker ⏳ 

## Setup
* Create python3.12 virtual environment
* Run `pip install -e .`
* Run command `pommo` in terminal
* Run build checks with `tox`

## Configuration
Fully supported config file at `${XDG_CONFIG_HOME}/timetasker/timetasker.toml` for Unix systems or `${APPDATA}\timetasker\timetasker.toml` on Windows:

```toml
[timer]
work_interval = "25m" # supports XhYmZs format
```

### Fallbacks

In the case that XDG_CONFIG_HOME is not set, or the os name is not recognised, timetasker will fall back to `~/.timetasker/`
