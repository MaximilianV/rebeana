from typing import List, Dict
import uuid
import pandas as pd

class Configuration:
    #Step 1:
    name: str
    log: pd.DataFrame
    #Step 2:
    resources: List[str]
    input_metrics: List[str]
    output_metrics: List[str]
    metric_configurations: Dict
    #Step 3:
    correlation: str
    regression: str

    def __init__(self, name, log):
        self.name: str = name
        self.log:pd.DataFrame = log
        self.id: str = str(uuid.uuid4())

    def get_all_metrics(self) -> List[str]:
        return self.input_metrics + self.output_metrics
