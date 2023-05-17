import os
import pandas as pd

path = "/home/david/Documents/Projects/traffic/data/"

df = pd.DataFrame(
    pd.read_excel(
        os.path.join(
            path, "raw", "traffic-signal-vehicle-and-pedestrian-volumes-data.xlsx"
        )
    )
)

data = df[
    [
        "Latitude",
        "Longitude",
        "8 Peak Hr Vehicle Volume",
        "8 Peak Hr Pedestrian Volume",
    ]
]

data.columns = ["LAT", "LONG", "VEH", "PED"]
data.to_csv(os.path.join(path, "processed", "signals.csv"), index=False)

signals = pd.read_csv(os.path.join(path, "processed", "signals.csv"))
df = pd.read_csv(os.path.join(path, "raw", "KSI.csv"))

data = df[
    ["LATITUDE", "LONGITUDE", "TIME", "VISIBILITY", "LIGHT", "RDSFCOND", "IMPACTYPE"]
]

data["TIME"] = data["TIME"] // 100 * 60 + data["TIME"] % 100

data.to_csv(os.path.join(path, "processed", "ksi.csv"), index=False)


