# -*- coding: utf-8 -*-

"""
    livestatus_objects
    ------------------

    This module provides some classes to query MK Livestatus
    and return results as objects.

    :copyright: (c) 2014 by Guillaume Subiron.
    :todo: Docstrings
"""

import socket


__all__ = ['LivestatusServer', 'Host', 'Service']


class MultipleResultsFound(Exception):
    """Raised when multiple results are found, but only one was excepted."""
    pass


class NoResultFound(Exception):
    """Raised when no result is found."""
    pass


class LivestatusServer():
    """Livestatus Server."""
    def __init__(self, host, port):
        """
            Instanciates a new Livestatus connexion.

            :param host: Server hostname or IP address
            :param port: Server port
        """
        self._peer = (host, port)

    def request(self, request):
        """
            Sends a request to the server and returns a python dictionnary.

            :param request: The request to send. Must be a string in
                            MK Livestatus syntax, and must ask for
                            python OutputFormat. You should not use this
                            method directly, but use Host and Services classes
                            instead
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self._peer)
            s.send(request.encode())
            s.shutdown(socket.SHUT_WR)
            return eval(s.makefile().read())
        finally:
            s.close()


class LivestatusObject():
    _entry = None
    _resource = ""

    def __init__(self, server, entry):
        self._server = server
        self._entry = entry

    def __getattr__(self, name):
        if name in self._entry:
            return self._entry[name]
        else:
            raise AttributeError()

    @classmethod
    def _request(cls, server, filters=None):
        request = 'GET %s\n' % (cls._resource)
        if filters:
            for f in filters:
                request += 'Filter: %s\n' % str(f)
        request += 'OutputFormat: json\n'
        request += 'ColumnHeaders: on\n'
        res = server.request(request)
        return [cls(server, dict(zip(res[0], r))) for r in res[1:]]

    @classmethod
    def all(cls, server):
        """
            Retrieves all the instances.
            :param server: LivestatusServer to query.
        """
        return cls._request(server)

    @classmethod
    def get(cls, server, obj):
        raise NotImplementedError()

    @classmethod
    def _get(cls, server, filters):
        res = cls.find(server, filters)
        if len(res) == 1:
            return res[0]
        elif len(res) == 0:
            raise NoResultFound()
        else:
            raise MultipleResultsFound()

    @classmethod
    def find(cls, server, filters):
        return cls._request(server, filters)


class Host(LivestatusObject):
    """Livestatus Host."""

    _resource = "hosts"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, server, hostname):
        return cls._get(server, ['name = %s' % hostname])

    @property
    def services(self):
        return Service.find(self._server, ['host_name = %s' % self.name])


class Service(LivestatusObject):
    """Livestatus Service."""

    _resource = "services"

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    @classmethod
    def get(cls, server, servicename, hostname):
        return cls._get(server, ["description = %s" % servicename,
                                 "host_name = %s" % hostname])

    @property
    def host(self):
        return Host.get(self._server, self.host_name)


class Hostgroup(LivestatusObject):
    """Livestatus Hostgroup."""

    _resource = "hostgroups"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, server, name):
        return cls._get(server, ['name = %s' % name])

    @property
    def members(self):
        return Host.find(self._server, ['groups >= %s' % self.name])
