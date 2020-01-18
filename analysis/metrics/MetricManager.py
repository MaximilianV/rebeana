import os
import toml

class MetricManager:
    metrics = []
    plugin_path = ""

    def __init__(self, plugin_dir=os.path.dirname(__file__)):
        self.plugin_path = plugin_dir

    def load_metrics(self):
        dir_list = next(os.walk(self.plugin_path))[1]
        for dir in dir_list:
            self.load_metric(dir)

    def load_metric(self, dir):
        absolute_path = os.path.join(self.plugin_path, dir)
        try:
            configuration = toml.load(os.path.join(absolute_path, dir + ".toml"))
            print(configuration["name"])
            print(configuration["description"])
        except FileNotFoundError:
            print("Directory \"" + dir + "\" does not contain a configuration file for a metric! It will not be imported.")
        except toml.TomlDecodeError:
            print("Configuration file for \"" + dir + "\" could not be read. Please check it for syntax errors.")

