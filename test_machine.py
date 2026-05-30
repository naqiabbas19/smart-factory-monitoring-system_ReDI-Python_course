
import pytest
from machine import Machine


# -------------------------------------------------
# FIXTURE: 3 machines setup
# -------------------------------------------------

@pytest.fixture
def setup_machines():

    machine_a = Machine("Line A", 500)
    machine_b = Machine("Line B", 500)
    machine_c = Machine("Line C", 500)

    return machine_a, machine_b, machine_c


# -------------------------------------------------
# Test: machine creation
# -------------------------------------------------

def test_machine_creation(setup_machines):

    a, b, c = setup_machines

    assert a.machine_name == "Line A"
    assert b.machine_name == "Line B"
    assert c.machine_name == "Line C"


# -------------------------------------------------
# Test: independent production
# -------------------------------------------------

def test_independent_production(setup_machines):

    a, b, c = setup_machines

    a.produce(200, 10)
    b.produce(300, 6)
    c.produce(100, 5)

    assert a.total_produced == 200
    assert b.total_produced == 300
    assert c.total_produced == 100


# -------------------------------------------------
# Test: defect rate calculation
# -------------------------------------------------

def test_defect_rate(setup_machines):
    def test_zero_production(setup_machines):

        a, _, _ = setup_machines

        assert a.defect_rate() == 0.0

    a, b, c = setup_machines

    a.produce(200, 10)   # 5%
    b.produce(200, 20)   # 10%
    c.produce(100, 5)    # 5%

    assert round(a.defect_rate(), 2) == 5.0
    assert round(b.defect_rate(), 2) == 10.0
    assert round(c.defect_rate(), 2) == 5.0


# -------------------------------------------------
# Test: ranking system logic
# -------------------------------------------------

def test_ranking_logic(setup_machines):

    a, b, c = setup_machines

    a.produce(200, 10)   # 5%
    b.produce(200, 20)   # 10%
    c.produce(100, 5)    # 5%

    ranked = sorted(
        [a, b, c],
        key=lambda m: m.defect_rate()
    )

    assert ranked[0].machine_name in ["Line A", "Line C"]
    assert ranked[-1].machine_name == "Line B"


# -------------------------------------------------
# Test: capacity limit
# -------------------------------------------------

def test_capacity_limit(setup_machines):

    a, _, _ = setup_machines

    with pytest.raises(ValueError):
        a.produce(600, 10)


# -------------------------------------------------
# Test: invalid defects
# -------------------------------------------------

def test_invalid_defects(setup_machines):

    a, _, _ = setup_machines

    with pytest.raises(ValueError):
        a.produce(100, 150)


# -------------------------------------------------
# Test: alert system (high defect rate > 20%)
# -------------------------------------------------

def test_alert_system(setup_machines):

    a, _, _ = setup_machines

    a.produce(100, 50)  # 50% defect rate

    assert "WARNING" in a.alert()