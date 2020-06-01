import os
import sys

import toml

from extraction.metrics.Metric import Metric
from utils.utils import name_to_module


class MetricManager:
    metrics: dict = {}
    plugin_path = ""

    def __init__(self, plugin_dir=os.path.dirname(__file__)):
        self.plugin_path = plugin_dir
        # Add metric/plugin path to sys path to allow importing them as modules
        sys.path.append(self.plugin_path)
        self.load_metrics()

    def load_metrics(self):
        self.metrics = {}
        dir_list = next(os.walk(self.plugin_path))[1]
        for dir in dir_list:
            self._load_metric(dir)

    def _load_metric(self, dir: str):
        if (dir == "__pycache__"):
            return

        absolute_path = os.path.join(self.plugin_path, dir)

        try:
            configuration = toml.load(
                os.path.join(absolute_path, dir + ".toml"))
            metric_name = configuration["name"]
            metric = Metric(configuration)

            if name_to_module(metric_name) != dir:
                raise KeyError(metric_name)

            self.metrics[metric_name] = metric
            # print("Successfully imported metric \"" +
            #       metric_name + "\" from directory \"" + dir + "\".")

        except FileNotFoundError:
            print("Directory \"" + dir +
                  "\" does not contain a configuration file for a metric! It will not be imported.")
        except toml.TomlDecodeError as msg:
            print("Configuration file for \"" + dir +
                  "\" could not be read. Please check it for syntax errors:")
            print(msg)
        except KeyError as metric_name:
            print("The name of the directory the metric \"" + str(metric_name) + "\" is defined in does not match.\n" +
                  "Expected \"" + name_to_module(str(metric_name)) + "\" but was \"" + dir + "\".")
        except ValueError:
            print("The metric defined in \"" + dir +
                  "\" or one of its variants is not named correctly.")
            print("Please make sure that all names start with a letter and only \" \", \"-\" and \"_\" are used as separators.")
            print("Additionally, please check if the directory is named like the metric.")

    def get_available_metrics(self):
        return self.metrics.keys()

    def get_environmental_metrics(self):
        env_metrics = []
        for metric, metric_object in self.metrics.items():
            if (metric_object.is_environmental()):
                env_metrics.append(metric)
        return env_metrics

    def get_behavioural_metrics(self):
        beh_metrics = []
        for metric, metric_object in self.metrics.items():
            if (metric_object.is_behavioural()):
                beh_metrics.append(metric)
        return beh_metrics

    def get_metric(self, metric_name: str) -> Metric:
        try:
            return self.metrics[metric_name]
        except KeyError:
            print("The metric \"" + metric_name + "\" is not defined.")
            print("Maybe try reloading the metrics directory?")
            raise
