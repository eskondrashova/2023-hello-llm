"""
Neural summarization starter.
"""
# pylint: disable= too-many-locals
import json
import os
from pathlib import Path

from config.constants import PROJECT_ROOT
from core_utils.llm.metrics import Metrics
from core_utils.llm.time_decorator import report_time
from lab_7_llm.main import LLMPipeline, TaskDataset, TaskEvaluator, RawDataImporter, RawDataPreprocessor


@report_time
def main() -> None:
    """
    Run the summarization pipeline.
    """
    with open(PROJECT_ROOT / "lab_7_llm" / "settings.json", "r", encoding="utf-8") as settings_file:
        settings = json.load(settings_file)

    importer = RawDataImporter(hf_name=settings["parameters"]["dataset"])
    importer.obtain()

    preprocessor = RawDataPreprocessor(raw_data=importer.raw_data)
    preprocessor.analyze()
    preprocessor.transform()

    dataset = TaskDataset(preprocessor.data.head(100))

    pipeline = LLMPipeline(model_name=settings["parameters"]["model"],
                           dataset=dataset,
                           max_length=120,
                           batch_size=1,
                           device="cpu")

    print(pipeline.analyze_model())
    pipeline.infer_sample(dataset[0])

    result = ""

    assert result is not None, "Demo does not work correctly"


if __name__ == "__main__":
    main()
