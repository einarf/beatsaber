import pytest


@pytest.fixture
def track():
    from beatsaber.track import BSTrack
    return BSTrack('megalovania_remix/Expert.dat', 242),

def test_stuff(track):
    assert True
