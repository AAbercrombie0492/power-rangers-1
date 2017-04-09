import os
import pandas as pd
import numpy as np
import datetime as dt

ROOT_FOLDER = os.path.dirname(__file__)
RAINFALL_FILE = os.path.join(ROOT_FOLDER, 'rainfall.csv')
START_DATE = dt.datetime(2016, 1, 1, 1)
N_TIMESTAMPS = 8760
FREQ = 'H'
TIMESTAMPS = pd.date_range(start=START_DATE, periods=N_TIMESTAMPS, freq=FREQ)
DF_RAINFALL = pd.read_csv(RAINFALL_FILE)
DF_RAINFALL.index = TIMESTAMPS
RAIN_CLEAN_THRESHOLD = 10.  # mm
SOILING_WASH_THRESHOLD = 0.05  # %


def calculate_rain_event(rainfall, times, rain_threshold, rolling_days=5):

    df_rainfall = pd.DataFrame(rainfall, index=times)
    df_rolled = df_rainfall.rolling(str(rolling_days)+'D').sum()
    rain_clean_events = df_rolled.values >= rain_threshold

    return rain_clean_events


def calculate_soiling_percentage(bur, bur_derate, rain_clean_events, times,
                                 wash_threshold):
    bur_hourly = bur / 24. * (1. - bur_derate)
    soiling_percentage = np.zeros(len(times))
    n_wash_events = 0
    for i in xrange(1, len(rain_clean_events)):
        if rain_clean_events[i]:
            soiling_percentage[i] = 0.
        else:
            soiling_percentage[i] = (soiling_percentage[i-1]
                                     + bur_hourly)
            if soiling_percentage[i] > wash_threshold:
                soiling_percentage[i] = 0.
                n_wash_events += 1

    return soiling_percentage, n_wash_events


def calculate_coating_benefit(bur, bur_derate):

    bur_no_derate = 0.
    rain_clean_events = calculate_rain_event(DF_RAINFALL.values, TIMESTAMPS,
                                             RAIN_CLEAN_THRESHOLD,
                                             rolling_days=5)

    # Calculate the timeseries soiling percentage of the power plant
    soiling_pct_no_coating, n_washes_no_coating = calculate_soiling_percentage(
        bur, bur_no_derate, rain_clean_events, TIMESTAMPS,
        SOILING_WASH_THRESHOLD
    )

    soiling_pct_w_coating, n_washes_w_coating = calculate_soiling_percentage(
        bur, bur_derate, rain_clean_events, TIMESTAMPS,
        SOILING_WASH_THRESHOLD
    )

    # Estimate the energy yield improvement from using soiling
    sum_soiling_no_coating = soiling_pct_no_coating.sum()
    sum_soiling_w_coating = soiling_pct_w_coating.sum()

    pct_yield_increase_w_coating = - ((sum_soiling_w_coating
                                       - sum_soiling_no_coating)
                                      / sum_soiling_no_coating) * 100.

    return (soiling_pct_w_coating, soiling_pct_no_coating,
            n_washes_w_coating, n_washes_no_coating,
            pct_yield_increase_w_coating)


if __name__ == '__main__':
    bur_county = 0.0008  # 0.08 % / day
    bur_derate_ctg = 0.30  # 10% decrease in BUR due to coating

    (soiling_pct_w_ctg, soiling_pct_no_ctg,
     n_washes_w_coating, n_washes_no_ctg,
     pct_yield_increase_w_ctg) = calculate_coating_benefit(bur_county,
                                                           bur_derate_ctg)

    print ("Percent yield increase with coating: "
           "%.2f %%" % pct_yield_increase_w_ctg)
