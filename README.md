# Livestatus (Object Oriented)

Helps to query MK Livestatus and return results as objects

## Installation

    pip install livestatus-objects

## Example

    >>> from livestatus_objects import LivestatusServer, Host
    >>> s = LivestatusServer(localhost, 50000)
    >>> host = Host.get(s, 'www01.example.net')
    >>> host
    infra-www01.hostsvpn.sysnove.net
    >>> host.services
    [Fork rate, Linux diskstat, Linux procstat, Load, Memory, NTP Clock Offset, Partitions, Postfix mail queue, Postfix stats, Ssh, Swap, Swap paging rate, Total procs, Uptime, Zombie procs]
    >>> host.last_state
    'UP'
    >>> host.services[3]
    Load
    >>> host.services[3].last_state
    'OK'
    >>> host.services[3].perf_data
    'load1=0.000;5.000;20.000;0; load5=0.010;5.000;15.000;0; load15=0.050;5.000;10.000;0;'


## Licence

This code is under [WTFPL](https://en.wikipedia.org/wiki/WTFPL). Just do what the fuck you want with it.
