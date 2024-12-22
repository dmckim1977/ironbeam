# Ironbeam

The provides an unofficial python wrapper around [Ironbeam's](https://www.ironbeam.com/) API for
futures.

**This is a work in progress.**

Key features include:

- Account Information
- Orders, both Live orders on your Ironbeam account or use a Demo account that can be created
  with the API.
- Historical Data
- Streaming Data.

## Documentation

Make sure you are familiar with the [Ironbeam Official API Docs](https://docs.ironbeamapi.com/).
There are some typos and stuff with the docs so it took a little detective work to figure this
out. If you see something that doesn't look in this library it might be because the docs are
wrong.

## Roadmap

- Async support
- Documentation
- Community

## Requirements

- httpx = '>=0.28.1'
- pandas = '>=2.2.3'
- pydantic = '>=2.10.4'

## Installation

To install the latest stable version of the package from PyPi:

```bash
pip install -U ironbeam
```

## Usage

```python
# Basic usage
import ironbeam as ib

client = ib.Ironbeam(apikey='<API KEY>')
client.authorize(username='<USERNAME>')
print(client.token)

# Use client...

client.logout()

# Context manager usage
with ib.Ironbeam(apikey='<API KEY>') as client:
  client.authorize(username='<USERNAME>')
```

## Contact

Feel free to [contact us](mail_to:davidmckim@gmail.com) with any questions. 
