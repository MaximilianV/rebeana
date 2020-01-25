import importlib.util

import utils.decorator as decorator
from utils.utils import check_valid_name, name_to_module


class Metric:
    configuration = {}

    def __init__(self, configuration_dict):
        self.configuration = configuration_dict
        if not self.check_valid_names():
            raise ValueError

    def get_name(self) -> str:
        return self.configuration["name"]

    def get_description(self) -> str:
        return self.configuration["description"]

    def get_variants_settings(self) -> dict:
        return self.configuration["variant"]

    def get_variants(self) -> []:
        return [variant["name"] for variant in self.get_variants_settings()]

    def has_variant(self, variant_name: str) -> bool:
        return variant_name in self.get_variants()

    @decorator.variant_exists
    def execute_variant(self, variant_name: str, log, resource, **parameters):
        try:
            variant_module = importlib.import_module(
                name_to_module(self.get_name()) + "." + name_to_module(variant_name))
            variant_compute = getattr(variant_module, 'compute')
            return variant_compute(log, resource, **parameters)
        except ModuleNotFoundError:
            print("The variant \"" + variant_name + "\" is configured for the metric \"" + self.get_name() + "\".\n" +
                  "However, there was no implementation for this variant found!\n" +
                  "Expected a file named \"" + name_to_module(variant_name) + ".py\" within the metric's directory.")
            raise

    @decorator.variant_exists
    def check_requirements(self, variant_name: str, log) -> bool:
        pass

    def check_valid_names(self):
        return (check_valid_name(self.get_name()) and all([check_valid_name(variant) for variant in self.get_variants()]))
