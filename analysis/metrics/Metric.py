import importlib.util


class Metric:
    configuration = {}

    def __init__(self, configuration_dict):
        self.configuration = configuration_dict

    def get_name(self):
        return self.configuration["name"]

    def get_description(self):
        return self.configuration["description"]

    def get_variants(self):
        return self.configuration["variant"]

    def has_variant(self, variant_name: str):
        return any(variant["name"] == variant_name for variant in self.get_variants())

    def execute_variant(self, variant_name: str):
        if (not self.has_variant(variant_name)):
            raise KeyError("The variant " + variant_name +
                           " is not defined for the metric " + self.get_name() + ".")

        variant_module = importlib.import_module(
            self.get_name().lower() + "." + variant_name.lower())
        variant_compute = getattr(variant_module, 'compute')
        variant_compute()
