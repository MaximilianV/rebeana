import importlib.util
import utils.decorator as decorator


class Metric:
    configuration = {}

    def __init__(self, configuration_dict):
        self.configuration = configuration_dict

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
                self.str_to_module(self.get_name()) + "." + self.str_to_module(variant_name))
            variant_compute = getattr(variant_module, 'compute')
            return variant_compute(log, resource, **parameters)
        except ModuleNotFoundError:
            print("The variant \"" + variant_name + "\" is configured for the metric \"" + self.get_name() + "\".\n" +
                  "However, there is no implementation for this variant!\n" +
                  "Expected to find a file named \"" +
                  self.str_to_module(variant_name) + ".py\" within the metric's directory.")
            raise

    @decorator.variant_exists
    def check_requirements(self, variant_name: str, log) -> bool:
        pass

    @staticmethod
    def str_to_module(name):
        return name.lower().replace(" ", "_")
