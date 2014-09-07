import pytest;

from livestatus_objects import LivestatusServer, Host, Service, Hostgroup, NoResultFound

@pytest.fixture()
def server():
    return LivestatusServer('infra-mon01.sysnove.net', 50000)

def test_get_host(server):
    assert Host.get(server, 'infra-mon01').name == 'infra-mon01'
    with pytest.raises(NoResultFound):
        Host.get(server, 'infra-foo01')

def test_get_host_services(server):
    host = Host.get(server, 'infra-mon01')
    services = host.services
    assert len(services)
    for s in services:
        assert s.host.name == 'infra-mon01'

def test_get_service(server):
    service = Service.get(server, 'Load', 'infra-mon01')
    assert service.description == 'Load'
    assert service.host.name == 'infra-mon01'

def test_get_hostgroup(server):
    hostgroup = Hostgroup.get(server, 'infra')
    assert hostgroup.name == 'infra'
    assert hostgroup.members[0].startswith('infra-')
