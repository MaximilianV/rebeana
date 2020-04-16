from utils.Configuration import Configuration
from extraction.metrics.MetricManager import MetricManager

class Extraction:
    @staticmethod
    def check_metrics():
        raise NotImplementedError

    @staticmethod
    def extract_metrics(config: Configuration):
        metrics = MetricManager()

        for metric_name in config.get_all_metrics():
            # Check if its an attribute. If yes, we do not need to extract it
            if config.is_metric_attribute(metric_name):
                continue

            metric = metrics.get_metric(metric_name)

            variant = config.get_variant_for_metric(metric_name)
            variant_config = config.get_variant_configuration(metric_name)

            for resource in config.resources:
                metric.execute_variant(variant, config.log, resource, **variant_config)
