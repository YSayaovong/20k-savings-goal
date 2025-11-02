from pipeline.generate_cashflows import run_projection

def test_interest_nonnegative():
    df = run_projection()
    assert (df["interest"] >= 0).all()

def test_monotonic_balance():
    df = run_projection()
    assert df["balance_end"].is_monotonic_increasing

def test_reasonable_first_interest():
    df = run_projection()
    assert 0 <= df["interest"].iloc[0] < 5
