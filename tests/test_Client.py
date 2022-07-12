import re
import pytest


@pytest.fixture
def client():
    from hopaas_client import Client
    client = Client()
    return client

################################################################################
def test_client_configurtion(client):
    from hopaas_client import Client
    assert isinstance(client, Client)
    assert isinstance(client.server, str)
    assert len(re.findall("[^:]*:[0-9]*", client.server)) > 0
    assert isinstance(client.token, str)


def test_get_version(client):
    assert isinstance(client.backend_version, str)
