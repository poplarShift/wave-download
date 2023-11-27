#!/bin/env python

from pathlib import Path
import xarray as xr
import pandas as pd

variables = ["hs", "tp", "thq", "longitude", "latitude"]


def download(file, pos):
    """https://marine.met.no/node/19
    """
    ds = xr.open_dataset(file)

    ds["r2"] = (ds.longitude - pos[0]) ** 2 + (ds.latitude - pos[1]) ** 2
    ds["r2"] = ds.r2.where(~ds.hs.isel(time=0).isnull())
    ds0 = ds.isel(ds.r2.argmin(dim=["rlon", "rlat"]))

    def get_name(v):
        name = ds[v].attrs.get("standard_name", ds[v].attrs.get("long_name", v))
        unit = ds[v].attrs.get("units", "()")
        return f"{name}_({unit})"

    variables_long = {v: get_name(v) for v in variables}

    df = ds0[variables].to_dataframe().rename(columns=variables_long)
    df = df.drop(columns=["rlat", "rlon"])
    outf = Path(file).with_suffix(".csv").name
    outf = f'{pos[0]:3.3f}_{pos[1]:3.3f}_{outf}'
    df.to_csv(outf)
    print(f"Writing {outf}")
    return outf


def filenames(times):
    fname = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/wave_v4/{yyyy:4d}{mm:02d}_NORA3wave_sub_time_unlimited.nc"
    files = [fname.format(yyyy=date.year, mm=date.month) for date in times]
    return files


if __name__ == "__main__":
    # 1
    pos = 13 + 13.2 / 60, 68 + 30.6 / 60
    times = (
        pd.date_range("2016-6-1", "2017-07-23", freq="MS").tolist()
        + pd.date_range("2020-06-20", "2021-01-13", freq="MS").tolist()
    )

    for file in filenames(times):
        download(file, pos)

    # 2
    pos = 11 + 31.8 / 60, 67 + 07.8 / 60
    times = (
        pd.date_range("2018-5-1", "2018-12-01", freq="MS").tolist()
        + pd.date_range("2019-12-19", "2020-06-02", freq="MS").tolist()
    )

    for file in filenames(times):
        download(file, pos)

    # 3
    pos = 14 + 30.0 / 60, 68 + 00.0 / 60
    times = (
        pd.date_range("2018-5-1", "2018-12-01", freq="MS").tolist()
        + pd.date_range("2019-12-19", "2020-06-02", freq="MS").tolist()
    )

    for file in filenames(times):
        download(file, pos)
