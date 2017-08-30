#!/usr/bin/env python

import yaml


def yamlstr2dict(str, starting):
    """Return dict with data parsed from yaml string."""
    # Remove everything in string before SQL statistics.
    # Only keeping the yaml data
    pos = str.find(starting)
    f = str[pos:]
    return yaml.load(f)


