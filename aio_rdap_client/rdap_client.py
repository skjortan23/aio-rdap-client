import aiohttp
from tldextract import tldextract
from async_lru import alru_cache

from aio_rdap_client.RdapResponse import RdapDomainEntry


class AsyncRdapClient:

    def __init__(self, caching=True):
        self.server_list = {}
        self.bootstrap_url = "https://data.iana.org/rdap/dns.json"
        self.bootstraped = False
        self.caching = caching

    @alru_cache(maxsize=32)
    async def _fetch_json(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    async def resolve(self, domain):
        if not self.bootstraped:
            await self.bootstrap()
        tld = tldextract.extract(domain).suffix
        apex_domain = tldextract.extract(domain).registered_domain
        try:
            authorative_server = self.server_list[tld]
            async with aiohttp.ClientSession() as session:
                res = await self._fetch_json(session, "%sdomain/%s" %(authorative_server, apex_domain ))
                if res:
                    entry = RdapDomainEntry.from_rdap_response(res)
                    return entry
                else:
                    raise LookupError('no valid rdap data received')
        except KeyError:
            raise LookupError("No rdap server found for domain: %s" % domain)


    async def parse_bootstrap_services(self, service_data):
        """
        This function sets the bootstrap servers for each tld and must be called before a query.
        :param service_data:
        :return:
        """
        for entry in service_data.get('services'):
            tlds = entry[0]
            servers = entry[1]
            for tld in tlds:
                self.server_list[tld] = servers[0]
        self.bootstraped = True


    async def bootstrap(self):
        """
        This function bootstraps the class with the correct servers per tld using a bootstrap query
        :return:
        """
        async with aiohttp.ClientSession() as session:
            bootstrap_data = await self._fetch_json(session, self.bootstrap_url)
            await self.parse_bootstrap_services(bootstrap_data)

