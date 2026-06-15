# pepkio-hwe-equilibrium-studio

Python client for the Pepkio [HWE Equilibrium Studio](https://www.pepkio.com/tools/hwe-equilibrium-studio) tool.

## Install

```bash
pip install pepkio-hwe-equilibrium-studio
```

Development:

```bash
uv sync
```

## Environment

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production API key (tools:run scope) |
| `LOCAL_PEPKIO_API_KEY` | Local dev key for `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API base (default: `https://tools.pepkio.com`) |

Create keys at [pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

## Publish to PyPI

```bash
source ~/.bash_profile   # loads POETRY_PYPI_TOKEN_PYPI
uv build
UV_PUBLISH_TOKEN=$POETRY_PYPI_TOKEN_PYPI uv publish
```

Do not commit tokens.
