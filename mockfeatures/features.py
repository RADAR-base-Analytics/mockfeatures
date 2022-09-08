import pandas as pd

from radarpipeline.datalib import RadarData
from radarpipeline.features import Feature, FeatureGroup


class MockFeatureGroup(FeatureGroup):
    def __init__(self):
        name = "MockFeatureGroup"
        description = "contains mock features"
        features = [PhoneBatteryChargingDuration, StepCountPerDay]
        super().__init__(name, description, features)

    def preprocess(self, data: RadarData) -> RadarData:
        """
        Preprocess the data for each feature in the group.
        """
        pass

    def compute_features(self, data: RadarData) -> RadarData:
        """
        compute and combine the features for each feature in the group.
        """
        pass


class PhoneBatteryChargingDuration(Feature):
    def __init__(self):
        self.name = "PhoneBatteryChargingDuration"
        self.description = "The duration of the phone battery charging"
        self.required_input_data = ["android_phone_battery_level"]

    def calculate(self, data: RadarData) -> float:
        df_phone_battery_level = data.get_combined_data_by_variable(
            "android_phone_battery_level"
        )
        print(df_phone_battery_level)
        df_phone_battery_level["value.time"] = pd.to_datetime(
            df_phone_battery_level["value.time"], unit="s"
        )
        df_phone_battery_level["date"] = df_phone_battery_level["time"].dt.date
        df_phone_battery_level = df_phone_battery_level[
            ~df_phone_battery_level[
                ["key.userId", "value.time", "value.batteryLevel"]
            ].duplicated()
        ]
        df_phone_battery_level["value.statusTime"] = (
            df_phone_battery_level.groupby("key.userId")["value.time"].diff().shift(-1)
        )
        df_phone_battery_level = (
            df_phone_battery_level.groupby(["key.userId", "date", "value.status"])
            .agg({"value.statusTime": "sum"})
            .reset_index()["value.statusTime"]
            .dt.total_seconds()
            / 60
        )
        df_phone_battery_level = df_phone_battery_level.reset_index()
        df_phone_battery_level = df_phone_battery_level[
            df_phone_battery_level["value.status"] == "charging"
        ]
        df_phone_battery_level = df_phone_battery_level.reset_index(drop=True)
        return df_phone_battery_level


class StepCountPerDay(Feature):
    def __init__(self):
        self.name = "StepCountPerDay"
        self.description = "The number of steps per day"
        self.required_input_data = ["android_phone_step_count"]

    def calculate(self, data: RadarData) -> float:
        df_step_count = data.get_combined_data_by_variable("android_phone_step_count")
        print(df_step_count)
        df_step_count["value.time"] = pd.to_datetime(
            df_step_count["value.time"], unit="s"
        )
        df_step_count["date"] = df_step_count["time"].dt.date
        df_step_count = df_step_count[
            ~df_step_count[["key.userId", "value.time", "value.stepCount"]].duplicated()
        ]
        df_step_count = df_step_count.reset_index(drop=True)
        df_total_step_count = df_step_count.groupby(["key.userId", "date"]).agg(
            {"value.stepCount": "sum"}
        )
        df_total_step_count = df_total_step_count.reset_index(drop=True)
        return df_total_step_count
