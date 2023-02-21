# PhpIpamApi Python Script

This is a Python 3 script for interacting with the PhpIPAM API.

## Prerequisites

This script requires the following:

- Python 3.x
- `requests` module
- `json` module

## Usage

To use this script, you will need to set up a configuration file (`config.json`) containing your PhpIPAM API settings. By default, the script looks for this file in the same directory as the script, but you can also set the `PHPIPAM_PYCLIENT_CFG_FILE` environment variable to specify a custom location.

The `PhpIpamApi` class provides the following methods:

### `__init__(self, cfg_file="config.json", init_auth=True)`

Initializes a new instance of the `PhpIpamApi` class with the specified configuration file. If `init_auth` is `True` (default), it will also attempt to authenticate the session.

### `load_config(self, cfg_file="config.json")`

Loads the configuration file specified by `cfg_file` and sets the necessary properties.

### `_build_url(self, endpoint: str)`

Builds the full API URL for the specified `endpoint`.

### `auth_session(self)`

Authenticates the session using the configured username and password.

### `_apply_filter(self, filter_obj, collection)`

Applies the specified filter to the provided collection of objects. The `filter_obj` parameter should be a dictionary with the following keys: `type` (string), `field` (string), and `value` (any). The `type` key specifies the type of filter to apply, and must be one of the following: `contains`, `eq`, `ge`, `gt`, `le`, or `lt`. The `field` key specifies the object property to filter on, and the `value` key specifies the filter value.

### `list_devices(self, fields=None, filters=[])`

Retrieves a list of devices from the PhpIPAM API. The `fields` parameter is an optional list of field names to retrieve for each device. The `filters` parameter is an optional list of filter objects to apply to the results.

### `list_vlan(self, fields=None, filters=[])`

Retrieves a list of VLANs from the PhpIPAM API. The `fields` parameter is an optional list of field names to retrieve for each VLAN. The `filters` parameter is an optional list of filter objects to apply to the results.

### `list_subnet(self, fields=None, filters=[])`

Retrieves a list of subnets from the PhpIPAM API. The `fields` parameter is an optional list of field names to retrieve for each subnet. The `filters` parameter is an optional list of filter objects to apply to the results.

## Contributing / Reporting issues

* [Link to Issues](https://github.com/n-K0/api_IPAMPHP/issues)
* [Link to project](https://github.com/n-K0/api_IPAMPHP/projects)

## License

[Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/)

## THANKS / AUTHORS
 [@n-K0] (https://www.github.com/n-K0)
