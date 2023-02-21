#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import warnings
import requests
import os
import sys
from collections import defaultdict

from version import __version__

DISABLE_SSL_WARNINGS = True
if DISABLE_SSL_WARNINGS:
    warnings.filterwarnings("ignore")


class PhpIpamApi(object):
    def __init__(self, cfg_file="config.json", init_auth=True):
        try:
            self.load_config(cfg_file=cfg_file)
            if self._passwd and self._user:
                print(self._user, self._passwd)
            self._session = None
            self._verify = False
            if init_auth and self._passwd and self._user:
                self.auth_session()
        except FileNotFoundError as e:
            print(str(e))
        except json.JSONDecodeError as e:
            print(str(e))
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(str(e))
            print("\nHave you configured your config.json file yet? ")
            sys.exit(1)

    def load_config(self, cfg_file="config.json"):

        file_path = os.environ.get("PHPIPAM_PYCLIENT_CFG_FILE")
        if not file_path:
            file_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), cfg_file
            )
        with open(file_path) as json_file:
            data = json.load(json_file)
            self._base_url = data["base_url"]
            self._api_name = data["api_name"]
            self._auth_url = "{0}/{1}/user/".format(self._base_url, self._api_name)
            self._api_url = "{0}/{1}".format(self._base_url, self._api_name)
            self._user = data["user"]
            self._passwd = data["passwd"]
            self._token = {'token': data["token"]}

    def _build_url(self, endpoint: str):
        return f"{self._api_url}/{endpoint}"

    def auth_session(self):
        req = requests.post(
            self._auth_url, auth=(self._user, self._passwd), verify=self._verify
        )
        if req.status_code != 200:
            raise requests.exceptions.RequestException(
                "Authentication failed on {0}".format(self._auth_url)
            )
        self._token = {"token": req.json()["data"]["token"]}
        return req

    def _apply_filter(self, filter_obj, collection):
        if not collection:
            return collection

        if not isinstance(filter_obj, dict):
            raise ValueError(f"filter {filter_obj} must be a dictionary")
        if any(
            (
                "type" not in filter_obj,
                "field" not in filter_obj,
                "value" not in filter_obj,
            )
        ):
            raise ValueError(
                f"filter must have 'type', 'field' and 'value' keys. obj: {filter_obj}"
            )

        def float_cast(value) -> float:
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0

        filter_value = filter_obj["value"]
        filter_field = filter_obj["field"]
        filter_types = {
            "contains": lambda x: filter_value in str(x.get(filter_field)),
            "eq": lambda x: filter_value == str(x.get(filter_field)),
            "ge": lambda x: float(filter_value) <= float_cast(x.get(filter_field)),
            "gt": lambda x: float(filter_value) < float_cast(x.get(filter_field)),
            "le": lambda x: float(filter_value) >= float_cast(x.get(filter_field)),
            "lt": lambda x: float(filter_value) > float_cast(x.get(filter_field)),
        }
        if filter_obj["type"] not in filter_types:
            print(filter_obj["type"])
            raise ValueError(
                f"invalid filter type, it must be of one these values: {list(filter_types.keys())}"
            )

        return list(
            filter(
                filter_types[filter_obj["type"]],
                [elem for elem in collection if filter_obj["field"] in elem],
            )
        )

    def list_devices(self, fields=None, filters=[]):

        if not isinstance(fields, list):
            fields = []

        req = requests.get(
            self._build_url("devices/"), headers=self._token, verify=self._verify
        )
        req.raise_for_status()

        data = req.json().get("data")
        if not data:
            return []

        device_list = []
        for device in data:
            if not fields:
                device_list.append(device)
                continue

            dev = {}
            for field in fields:
                dev[field] = device.get(field)
            if dev:
                device_list.append(dev)

        try:
            for filter_obj in filters:
                device_list = self._apply_filter(filter_obj, device_list)
            return device_list
        except ValueError as e:
            print(str(e))
            sys.exit(1)

    def list_vlan(self, fields=None, filters=[]):
            if not isinstance(fields, list):
                fields = []

            req = requests.get(
                self._build_url("vlan/all/"), headers=self._token, verify=self._verify
            )
            req.raise_for_status()

            data = req.json().get("data")
            if not data:
                return []

            vlan_list = []
            for vlan in data:
                if not fields:
                    vlan_list.append(vlan)
                    continue

                dev = {}
                for field in fields:
                    dev[field] = vlan.get(field)
                if dev:
                    vlan_list.append(dev)

            try:
                for filter_obj in filters:
                    vlan_list = self._apply_filter(filter_obj, vlan_list)
                return vlan_list
            except ValueError as e:
                print(str(e))
                sys.exit(1)

    def list_subnet(self, fields=None, filters=[]):
            if not isinstance(fields, list):
                fields = []

            req = requests.get(
                self._build_url("subnets/all/"), headers=self._token, verify=self._verify
            )
            req.raise_for_status()

            data = req.json().get("data")
            if not data:
                return []

            subnet_list = []
            for subnet in data:
                if not fields:
                    subnet_list.append(subnet)
                    continue

                dev = {}
                for field in fields:
                    dev[field] = subnet.get(field)
                if dev:
                    subnet_list.append(dev)

            try:
                for filter_obj in filters:
                    subnet_list = self._apply_filter(filter_obj, subnet_list)
                return subnet_list
            except ValueError as e:
                print(str(e))
                sys.exit(1)

    def list_domains(self, fields=None, filters=[]):
            if not isinstance(fields, list):
                fields = []

            req = requests.get(
                self._build_url("l2domains/all/"), headers=self._token, verify=self._verify
            )
            req.raise_for_status()

            data = req.json().get("data")
            if not data:
                return []

            domain_list = []
            for domain in data:
                if not fields:
                    domain_list.append(domain)
                    continue

                dev = {}
                for field in fields:
                    dev[field] = domain.get(field)
                if dev:
                    domain_list.append(dev)

            try:
                for filter_obj in filters:
                    domain_list = self._apply_filter(filter_obj, domain_list)
                return domain_list
            except ValueError as e:
                print(str(e))
                sys.exit(1)

    def list_sections(self, fields=None, filters=[]):
            if not isinstance(fields, list):
                fields = []

            req = requests.get(
                self._build_url("sections/"), headers=self._token, verify=self._verify
            )
            req.raise_for_status()

            data = req.json().get("data")
            if not data:
                return []

            section_list = []
            for section in data:
                if not fields:
                    section_list.append(section)
                    continue

                dev = {}
                for field in fields:
                    dev[field] = section.get(field)
                if dev:
                    section_list.append(dev)

            try:
                for filter_obj in filters:
                    section_list = self._apply_filter(filter_obj, section_list)
                return section_list
            except ValueError as e:
                print(str(e))
                sys.exit(1)

    def add_vlan(self, vlan=None):
        if isinstance(vlan, str):
            vlan = json.loads(vlan)

        url = f"{self._api_url}/vlan"
        return requests.post(
            url, headers=self._token, verify=self._verify, data=vlan
        ).status_code

    def add_subnet(self, device=None):
        if isinstance(device, str):
            device = json.loads(device)
        
        url = f"{self._api_url}/subnets"
        return requests.post(
            url, headers=self._token, verify=self._verify, data=device
        ).status_code

    def add_device(self, device=None):
        if isinstance(device, str):
            device = json.loads(device)
        
        url = f"{self._api_url}/devices"
        return requests.post(
            url, headers=self._token, verify=self._verify, data=device
        ).status_code



    def version(self):
        return __version__