from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.util import constants
from typing import Union


def filter_log_by_resource_names(log, names: list):
    """Filters the eventlog by events having certain resources

    Arguments:
        log {DataFrame} -- The log to use for analysis
        names {list} -- The resource names to filter by

    Returns:
        DataFrame -- The filtered log
    """
    return attributes_filter.apply_events(log, names, parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: "org:resource", "positive": True})


def get_resources(log, as_dict: bool = False) -> Union[list, dict]:
    """Returns the list of resources than can be found in the log

    Arguments:
        log {DataFrame} -- The log to use for analysis

    Keyword Arguments:
        as_dict {bool} -- If set to true, a dict will be returned including the number of occurences (default: {False})

    Returns:
        list | dict -- A list (or dict) of resource names (with occurences)
    """

    resources = attributes_filter.get_attribute_values(
        log, attribute_key="org:resource")

    if as_dict:
        return resources
    return resources.keys()


def get_resources_with_min_absolute_frequency(log, min_freq: int, as_dict: bool = False) -> Union[list, dict]:
    """Returns the list of resources which occure in at least the given number of events in the log

    Arguments:
        log {DataFrame} -- The log to use for analysis
        min_freq {int} -- The minimum number of times a resource should appear in the log

    Keyword Arguments:
        as_dict {bool} -- If set to true, a dict will be returned including the number of occurences (default: {False})

    Returns:
        list | dict -- A list (or dict) of resource names (with occurences)
    """
    resources = get_resources(log, as_dict=True)
    filtered_resources = {resource: occurence for (
        resource, occurence) in resources.items() if occurence >= min_freq}

    if as_dict:
        return filtered_resources

    return filtered_resources.keys()


def get_most_frequent_resources(log, number_of_resources: int, as_dict: bool = False) -> Union[list, dict]:
    """Returns the n most frequent resources from the log

    Arguments:
        log {DataFrame} -- The log to use for analysis
        number_of_resources {int} -- Specifies how many "top" resources should be returned

    Keyword Arguments:
        as_dict {bool} -- If set to true, a dict will be returned including the number of occurences (default: {False})

    Returns:
        list | dict -- A list (or dict) of resource names (with occurences)
    """
    resources = get_resources(log, True)
    top_resource_names = list(resources.keys())[:number_of_resources]
    if as_dict:
        return {k: v for (k, v) in resources.items() if k in top_resource_names}
    return top_resource_names
