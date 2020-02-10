import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

JsonDict = Dict[str, Any]

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

@dataclass
class RdapDomainEntry:
    domain: str
    registered: datetime
    updated: datetime
    expires: datetime
    status: str
    registrar: str
    namservers: List[str]
    secureDNS: bool

    def __init__(self, domain, registered, updated, expires, registrar, nameservers: List[str], status: str):
        self.domain = domain
        self.registered = registered
        self.updated = updated
        self.expires = expires
        self.registrar = registrar
        self.namservers = nameservers
        self.status = status
        self.secureDNS = False

    @classmethod
    def parse_rdap_events(cls, events):
        """
        parses the events portion of a rdap response and returns the dates as datetime
        :return:
        """
        registered = None
        updated = None
        expires = None

        for event in events:
            date = datetime.fromisoformat(event.get('eventDate').replace("Z", "+00:00"))
            event_type = event.get('eventAction')
            if event_type == 'registration':
                registered = date
            if event_type == 'expiration':
                expires = date
            if event_type == "last update of RDAP database":
                updated = date
        return registered, updated, expires

    @classmethod
    def from_rdap_response(cls, rdap_response: JsonDict ):
        rr = rdap_response
        nameservers = [nameserver.get('ldhName') for nameserver in rdap_response.get('nameservers')]
        registered, updated, expires = cls.parse_rdap_events(rr.get('events'))

        return cls(rr['ldhName'].lower(), registered, updated, expires, '', nameservers, rr['status'][0])

    def to_json(self):
        return json.dumps(self, cls=DateTimeEncoder)

    def to_dict(self):
        return dataclasses.asdict(self)