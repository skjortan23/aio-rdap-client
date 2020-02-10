import asyncio
import logging
from unittest import TestCase

from rdap_client import async_rdap_client


class Test_rdap(TestCase):
    def setUp(self) -> None:
        self.rdap = async_rdap_client(caching=False)
        self.valid_domains = ['intelliagg.com', 'threatfinder.com', 'test.uk']

    def test_bootstrap(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.rdap.bootstrap())

    def test_lookup(self):
        loop = asyncio.get_event_loop()
        async def async_test():
            for domain in self.valid_domains:
                try:
                    await self.rdap.resolve(domain)
                except LookupError as e:
                    logging.warning(e)
        loop.run_until_complete(async_test())