"""Generic sanity checks for deep learning models.

Each model factory in MODEL_FACTORIES is checked for the same basic properties.
For now it only contains a stand-in MLP; add the real models (policy, value, BC)
as they are written, so the checks run on them automatically in CI.
"""

import pytest
import torch
from torch import nn

OBS_DIM = 16
N_ACTIONS = 9


def tiny_mlp() -> nn.Module:
    return nn.Sequential(nn.Linear(OBS_DIM, 32), nn.ReLU(), nn.Linear(32, N_ACTIONS))


MODEL_FACTORIES = [tiny_mlp]


@pytest.fixture(autouse=True)
def fixed_seed():
    torch.manual_seed(0)


@pytest.mark.parametrize("make_model", MODEL_FACTORIES)
def test_output_shape(make_model):
    model = make_model()
    out = model(torch.randn(4, OBS_DIM))
    assert out.shape == (4, N_ACTIONS)
    assert torch.isfinite(out).all()


@pytest.mark.parametrize("make_model", MODEL_FACTORIES)
def test_gradients_flow_to_all_parameters(make_model):
    model = make_model()
    loss = model(torch.randn(4, OBS_DIM)).pow(2).mean()
    loss.backward()
    for name, p in model.named_parameters():
        assert p.grad is not None, f"no gradient for {name}"
        assert torch.isfinite(p.grad).all(), f"non-finite gradient for {name}"


@pytest.mark.parametrize("make_model", MODEL_FACTORIES)
def test_can_overfit_tiny_batch(make_model):
    """If a model cannot overfit 8 samples, something in the training loop is broken."""
    model = make_model()
    x = torch.randn(8, OBS_DIM)
    y = torch.randint(0, N_ACTIONS, (8,))
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    loss_fn = nn.CrossEntropyLoss()
    first = loss_fn(model(x), y).item()
    for _ in range(200):
        opt.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        opt.step()
    assert loss.item() < first * 0.2


@pytest.mark.parametrize("make_model", MODEL_FACTORIES)
def test_same_seed_same_output(make_model):
    x = torch.randn(4, OBS_DIM)
    torch.manual_seed(123)
    a = make_model()(x)
    torch.manual_seed(123)
    b = make_model()(x)
    assert torch.equal(a, b)
