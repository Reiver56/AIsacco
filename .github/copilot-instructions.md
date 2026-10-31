# Instructions for code review

This is a student project: a reinforcement/imitation learning agent for The Binding of Isaac: Repentance (Lua mod, Python, PyTorch, Gymnasium). Reviews should be clear and explain the reasoning, since the author is still learning deep learning.

## What to check in Python / PyTorch code

- Data leakage: validation or test data must never be used for training, normalization statistics, or model selection. Splits should be by whole game/run, not by random frames.
- Reproducibility: seeds set for `random`, `numpy` and `torch`; configs and hyperparameters not hard-coded in the middle of the code.
- Train/eval mode: `model.eval()` and `torch.no_grad()` (or `inference_mode`) during evaluation and rollouts; `model.train()` restored afterwards.
- Tensor shapes and dtypes: flag silent broadcasting, missing masks for padded entities, wrong dimension in softmax or loss.
- Devices: no mix of CPU and GPU tensors; no needless `.cpu()` / `.item()` calls inside training loops.
- Loss and gradients: correct loss for the task (cross-entropy takes logits, not probabilities), gradients zeroed, gradient clipping where expected, detached targets.
- Reinforcement learning: `terminated` (real end of an episode) and `truncated` (time limit) kept separate; advantages normalized per batch; no data from old policies reused in on-policy updates; reward scale and discount stated explicitly.
- Evaluation: reported metrics use several seeds and episodes not seen in training; policy evaluated without exploration noise.
- Do not commit data, checkpoints or logs (`.pt`, `.npz`, `log.txt`).

## What to check in the Lua mod

- No heavy work in per-frame callbacks; avoid allocating large tables every frame.
- Logged lines keep the `[BOT]` prefix and a stable JSON schema (see `docs/state-schema.md`).

## Style

- Python: ruff rules in `pyproject.toml`, type hints on public functions, short docstrings that say what and why.
- Prefer small, focused PRs: one step, one change.
