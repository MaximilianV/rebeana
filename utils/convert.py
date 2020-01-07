from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter


def convert_xes_file_to_parquet(xes_input_path: str, parquet_output_path: str):
    """Converts a XES file at the given location to a parquet file (via pandas dataframes)

    Arguments:
        xes_input_path {str} -- The filepath the XES file should be read from
        parquet_output_path {str} -- The filepath the new parquet file should be written to
    """
    log = xes_importer.apply(xes_input_path)
    parquet_exporter.apply(log, parquet_output_path)
