"""Implement this interface using a real simulator and validated policies."""
from abc import ABC, abstractmethod
from pathlib import Path

class ExperimentAdapter(ABC):
    @abstractmethod
    def execute_registered_stage(self, root: Path, stage_id: str, protocol: dict, final_lock: dict) -> Path:
        """Run actual registered trials. Return a measured JSONL record path.

        Save every attempted trace and the complete attempt ledger. No synthetic
        fallback is allowed. Implement task/scenario generation, snapshot replay,
        policies, event measurement and exposure rules described in docs.
        """
        raise NotImplementedError

class UnconfiguredAdapter(ExperimentAdapter):
    def execute_registered_stage(self, root, stage_id, protocol, final_lock):
        raise NotImplementedError('No simulator adapter or trained policies configured. No research trials were executed.')
