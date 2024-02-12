import matplotlib.pyplot as plt
import xarray as xr
import getpass
import pydap
import pandas as pd
import numpy as np
import numpy.ma as ma
from datetime import datetime
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
    #USERNAME = getpass.getpass('Enter your username: ')
    #PASSWORD = getpass.getpass('Enter your password: ')
    DATASET_ID = 'dataset-bal-reanalysis-wav-hourly'
    # DATASET_ID = 'cmems_mod_bal_wav_anfc_PT1h-i'
    USERNAME = 'srikka2'
    PASSWORD = 'ULtRAnYL2'
    data_store = copernicusmarine_datastore(DATASET_ID, USERNAME, PASSWORD)

    DS = xr.open_dataset(data_store)

    time = pd.to_datetime(DS.time.data)
    hs = DS.VHM0.sel(time=slice("2004-01-01", "2004-02-15")).mean('time').plot()
    print(hs)

    print('The end!')
