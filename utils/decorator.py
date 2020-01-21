def variant_exists(method):
    def wrapper(self, variant_name, *args, **kwargs):
        if (not self.has_variant(variant_name)):
            raise KeyError("The variant " + variant_name +
                           " is not defined for the metric " + self.get_name() + ".")
        return method(self, variant_name, *args, **kwargs)
    return wrapper
