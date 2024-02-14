import matplotlib.pyplot as plt
import xarray as xr
import getpass
import pydap
import pandas as pd
import numpy as np
import numpy.ma as ma
import datetime as dt
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import griddata
# %matplotlib inline


def copernicusmarine_datastore(dataset, username, password):
    from pydap.client import open_url
    from pydap.cas.get_cookies import setup_session
    cas_url = 'https://cmems-cas.cls.fr/cas/login'
    session = setup_session(cas_url, username, password)
    session.cookies.set("CASTGC", session.cookies.get_dict()['CASTGC'])
    database = ['my', 'nrt']
    url = f'https://{database[0]}.cmems-du.eu/thredds/dodsC/{dataset}'
    try:
        data_store = xr.backends.PydapDataStore(open_url(url, session=session, user_charset='utf-8')) # needs PyDAP >= v3.3.0 see https://github.com/pydap/pydap/pull/223/commits
    except:
        url = f'https://{database[1]}.cmems-du.eu/thredds/dodsC/{dataset}'
        data_store = xr.backends.PydapDataStore(open_url(url, session=session, user_charset='utf-8')) # needs PyDAP >= v3.3.0 see https://github.com/pydap/pydap/pull/223/commits
    return data_store

# can the following code be used for the date generation for HS mean calculations.

from datetime import date, timedelta
"""
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2013, 1, 1)
end_date = date(2015, 6, 2)
for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%Y-%m-%d"))
"""

if __name__ == '__main__':
    #pip install lxml
    # from 2004 to end of 2013
    #USERNAME = getpass.getpass('Enter your username: ')
    #PASSWORD = getpass.getpass('Enter your password: ')
    DATASET_ID = 'dataset-bal-reanalysis-wav-hourly'
    # DATASET_ID = 'cmems_mod_bal_wav_anfc_PT1h-i'
    USERNAME = 'srikka2'
    PASSWORD = 'ULtRAnYL2'
    data_store = copernicusmarine_datastore(DATASET_ID, USERNAME, PASSWORD)

    labels_to_drop = ['VHM0_SW1', 'VHM0_SW2', 'VHM0_WW', 'VMDR_SW1', 'VMDR_SW2', 'VMDR_WW', 'VPED', 'VSDX', 'VSDY',
                      'VTM01_SW1', 'VTM01_SW2', 'VTM01_WW', 'VTM10', 'VTPK']
    DS = xr.open_dataset(data_store).drop_vars(labels_to_drop)

    for year in np.arange(2004, 2014, 1):
        for month in np.arange(1, 13, 1):
            days_in_month = pd.Period(f'{year}-{month}').days_in_month
            print(f'collecting data for year: {year}, month: {month} (days in month: {days_in_month})')
            d1 = DS.sel(time=slice(f'{year}-{month}-{1}', f'{year}-{month}-{days_in_month//2}'))
            d2 = DS.sel(time=slice(f'{year}-{month}-{days_in_month//2 + 1}', f'{year}-{month}-{days_in_month}'))
            data_month = xr.concat([d1, d2], dim='time').to_netcdf(rf'E:\adapt_wave\{year}_{month}.nc', mode='w')
            d1, d2 = None, None

    # time = pd.to_datetime(DS.time.data)
    # d1 = DS.sel(time=slice('2004-01-01 00:00:00', '2004-01-15 23:00:00'))
    # d2 = DS.sel(time=slice('2004-01-16 00:00:00', '2004-01-31 23:00:00'))
    # hs_jan = xr.concat([hs1, hs2], dim='time')
    # data_jan = xr.concat([d1, d2], dim='time')
    # data_jan.to_netcdf(path='2004_jan.nc', mode='w')
    # hs_arr = []
    # for i in range(0, len(time), 15):
    #     start_date = dt.datetime.strptime(time[i], '%Y-%m-%d')
    #     end_date = dt.datetime.strptime(time[i + 15], '%Y-%m-%d') # siin peab mingi parem indekseerimine olema...
    #     # praegu jookseb i+15 üle aastas olevate päevade arvu. aga vb ei peagi aasta kaupa jagama?
    #     hs = DS.VHM0.sel(time=slice(f'{start_date}2004-01-01', f'{end_date}2004-02-15')).mean('time').plot()
    #     if i == 0:
    #         hs_arr = hs.reshape((1, 1, 256, 256))  # esimene tühi dimensioon pole vajalik
    #     else:
    #         hs_arr = np.append(hs_arr, hs.reshape((1, 1, 256, 256)),
    #                             axis=0)
        # kui aasta läbi, siis salvestada array? v salvestada kuude kaupa arrayd koos muutujatega, mis hiljem vajalikud oleks???
    #print(hs)

    print('The end!')
