"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_hwe_equilibrium_studio.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "hwe-equilibrium-studio"
    names = live_client.list_examples()
    assert "mn_blood_group" in names


def test_run_mn_blood_group(live_client: PepkioClient):
    inp = live_client.get_example_input("mn_blood_group")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.result.get("mode") == "calculator"
    assert result.result.get("has_blocking_errors") is False
    assert isinstance(result.result.get("verdict"), dict)
    assert isinstance(result.result.get("stats"), dict)
    assert isinstance(result.result.get("genotypes"), list)
    assert result.error is None


def test_run_triallelic_counts(live_client: PepkioClient):
    inp = live_client.get_example_input("triallelic_counts")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("has_blocking_errors") is False
    genotypes = result.result.get("genotypes")
    assert isinstance(genotypes, list)
    assert len(genotypes) > 0


def test_run_simulator_fixation(live_client: PepkioClient):
    inp = live_client.get_example_input("simulator_fixation")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("mode") == "simulator"
    trajectory = result.result.get("trajectory")
    assert isinstance(trajectory, list)
    assert len(trajectory) > 0
