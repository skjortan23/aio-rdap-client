# aio-rdap-client

This is a quick and dirty implementation of an rdap client for resolving domain whois information. 
Since whois is getting more and more broken and chaotic the world is switching to rdap for whois infromation.
However this does not seem to be the case with the python world where a lot of broken and unmaintained 
whois packages seems to be the way.

I needed a simple package to do registrar and domain resolution that worked with async. 

Since a could not find anything that fit the bill i had to "Roll my own". 

This project came out of necesity for a tool that gives valid registrar data for security investigations.

## instalation

pip3 install aio-rdap-client

## usage

`from rdap_client import async_rdap_client`

`resolver = async_rdap_client()`

`result = await resolver.resolve('test.com')`
