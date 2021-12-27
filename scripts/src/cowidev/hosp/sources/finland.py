import requests

import pandas as pd

METADATA = {
    "source_url": "https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaHospitalData",
    "source_url_ref": "https://www.thl.fi/episeuranta/tautitapaukset/coronamap.html",
    "source_name": "Department of Health and Welfare",
    "entity": "Finland",
}


def main() -> pd.DataFrame:
    data = requests.get(METADATA["source_url"]).json()
    df = pd.DataFrame.from_records(data["hospitalised"])

    df = df[df.area == "Finland"][["date", "totalHospitalised", "inIcu"]]
    df["date"] = df.date.astype(str).str.slice(0, 10)

    df = df.melt("date", var_name="indicator").dropna(subset=["value"])
    df["indicator"] = df.indicator.replace(
        {
            "totalHospitalised": "Daily hospital occupancy",
            "inIcu": "Daily ICU occupancy",
        }
    )

    df["entity"] = "Finland"

    return df, METADATA


if __name__ == "__main__":
    main()
