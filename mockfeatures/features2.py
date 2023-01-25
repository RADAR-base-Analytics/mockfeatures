import pandas as pd
from radarpipeline.datalib import RadarData
from radarpipeline.features import Feature, FeatureGroup


class MockFeatureGroup2(FeatureGroup):
    def __init__(self):
        name = "MockFeatureGroup2"
        description = "contains some more mock features"
        features = [StepCountPerHour, StepCountPerIgnore]
        super().__init__(name, description, features)

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        return data

class StepCountPerHour(Feature):
    def __init__(self):
        self.name = "StepCountPerHour"
        self.description = "The number of steps per hour"
        self.required_input_data = ["android_phone_step_count"]

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        df_step_count = data.get_combined_data_by_variable("android_phone_step_count")
        df_step_count["time"] = pd.to_datetime(df_step_count["value.time"], unit="s")
        df_step_count["date"] = df_step_count["time"].dt.date
        df_step_count = df_step_count[
            ~df_step_count[["key.userId", "value.time", "value.steps"]].duplicated()
        ]
        df_step_count = df_step_count.reset_index(drop=True)
        return df_step_count

    def calculate(self, data) -> float:
        df_step_count = data
        df_step_count["hour"] = df_step_count["time"].dt.hour
        df_total_step_count = df_step_count.groupby(["key.userId", "date", "hour"]).agg(
            {"value.steps": "sum"}
        )
        df_total_step_count = df_total_step_count.reset_index()
        return df_total_step_count

class StepCountPerIgnore(Feature):
    def __init__(self):
        self.name = "StepCountPerIgnore"
        self.description = "The number of steps per hour"
        self.required_input_data = ["android_phone_step_count"]

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        df_step_count = data.get_combined_data_by_variable("android_phone_step_count")
        df_step_count["time"] = pd.to_datetime(df_step_count["value.time"], unit="s")
        df_step_count["date"] = df_step_count["time"].dt.date
        df_step_count = df_step_count[
            ~df_step_count[["key.userId", "value.time", "value.steps"]].duplicated()
        ]
        df_step_count = df_step_count.reset_index(drop=True)
        return df_step_count

    def calculate(self, data) -> float:
        df_step_count = data
        df_step_count["hour"] = df_step_count["time"].dt.hour
        df_total_step_count = df_step_count.groupby(["key.userId", "date", "hour"]).agg(
            {"value.steps": "sum"}
        )
        df_total_step_count = df_total_step_count.reset_index()
        return df_total_step_count
