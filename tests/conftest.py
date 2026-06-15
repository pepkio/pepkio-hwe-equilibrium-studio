"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "hwe-equilibrium-studio",
        "title": "HWE Equilibrium Studio",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "mn_blood_group",
                "description": "Classic MN blood group data (N=6129), HWE-consistent",
                "input": {
                    "mode": "calculator",
                    "allele_count": 2,
                    "input_kind": "genotype_counts",
                    "genotype_counts": {
                        "A1_A1": 1787,
                        "A1_A2": 3039,
                        "A2_A2": 1303,
                    },
                },
            },
            {
                "name": "simulator_fixation",
                "description": "Strong selection drives fixation within 200 generations",
                "input": {
                    "mode": "simulator",
                    "allele_count": 2,
                    "initial_frequencies": [0.5, 0.5],
                    "generations": 200,
                    "Ne": 50,
                    "selection_coefficients": [0.3, -0.2],
                    "mutation_rate": 0,
                    "migration_rate": 0,
                    "random_seed": 7,
                },
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "mode": "calculator",
            "has_blocking_errors": False,
            "errors": [],
            "warnings": [],
            "genotypes": [
                {"genotype": "A1_A1", "observed": 1787, "expected": 1750.0},
            ],
            "stats": {"n": 6129, "k": 3, "df": 1},
            "verdict": {"hwe_consistent": True, "p_value": 0.42},
            "trajectory": [],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
