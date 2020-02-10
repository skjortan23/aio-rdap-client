import asyncio
import logging
from unittest import TestCase

from aio_rdap_client.rdap_client import AsyncRdapClient

class Test_rdap(TestCase):
    def setUp(self) -> None:
        self.rdap = AsyncRdapClient(caching=False)
        self.valid_domains = ['intelliagg.com', 'threatfinder.com', 'test.uk']

    def test_bootstrap(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.rdap.bootstrap())

    def test_lookup(self):
        loop = asyncio.get_event_loop()
        async def async_test():
            for domain in self.valid_domains:
                try:
                    res = await self.rdap.resolve(domain)
                    print(res.to_json())
                except LookupError as e:
                    logging.warning(e)
        loop.run_until_complete(async_test())