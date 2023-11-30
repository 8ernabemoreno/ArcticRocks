# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:19:30 2023

@author: 8erna
"""
import xarray as xr
import pandas as pd
from datetime import datetime as dt
import numpy as np
# import pdb; pdb.set_trace()

df = pd.read_csv(r"D:\spyder\logIsfjorden\s2d_.csv")
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%dT%H:%M:%S')
np.array(df['Date'])

latitude = sorted(list(set(df['Latitude'])))
longitude = sorted(list(set(df['Longitude'])))
time = sorted(list(set(df['Date'])))

slct = ['Date','Latitude', 'Longitude', 'Sea water temperature (degC)', 'Light intensity (lux)' ]
slct_df = df[slct]
slct_df
slct_df.to_csv('s2d_.csv', index=False)

temperature = np.array(df['Sea water temperature (degC)']).reshape(250357,1,1)
light = np.array(df['Light intensity (lux)']).reshape(250357,1,1)
date = np.array(df['Date'])

xrds = xr.Dataset(
    coords = dict(
          longitude = longitude,
          latitude = latitude,
          time = date
          ),
    data_vars = dict(
        sea_water_temperature_at_sea_floor = (["time","latitude","longitude"],temperature),
        light_intensity_at_sea_floor = (["time","latitude","longitude"],light), 
        )
    )

xrds['time'].attrs['standard_name'] = 'time'
xrds['time'].attrs['long_name'] = 'time'
xrds['time'].attrs['comment'] = 'time of sample'
xrds['time'].attrs['coverage_content_type'] = 'coordinate'

xrds = xrds.assign_attrs({
    #'units': 'date time of data point',
    'long_name': 'time',
    'standard_name': 'time',
    'coverage_content_type': 'coordinate'
    })

xrds['latitude'].attrs = {
    'standard_name': 'latitude',
    'long_name': 'decimal latitude in degrees north',
    'units': 'degrees_north',
    'coverage_content_type':'coordinate'
    }

xrds['longitude'].attrs = {
    'standard_name': 'longitude',
    'long_name': 'decimal longitude in degrees east',
    'units': 'degrees_east',
    'coverage_content_type':'coordinate'
    }

xrds['sea_water_temperature_at_sea_floor'].attrs = {
    'standard_name': 'sea_water_temperature_at_sea_floor',
    'long_name': 'Temperature of sea water adjacent to the sea floor',
    'units': 'degC',
    'coverage_content_type':'physicalMeasurement'
    }

xrds['light_intensity_at_sea_floor'].attrs = {
    'standard_name': 'light_intensity_at_sea_floor',
    'long_name': 'Light intensity  adjacent to the sea floor provided in lumen per square metre (lux)',
    'units': 'lux',
    'coverage_content_type':'physicalMeasurement'
    }

global_attributes = pd.read_excel(r'D:\BERNATRACIUS\2022\NatureScientificData\globalAttributes_s2d.xlsx', index_col = 0)
global_attributes_transposed = global_attributes.transpose()
global_attributes_dict = {}
for col in global_attributes_transposed.columns:
    global_attributes_dict[col] = global_attributes_transposed[col].iloc[0]


xrds.attrs = global_attributes_dict

xrds.attrs['date_created'] = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
xrds.attrs['history']= f'File created at {dt.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")} using xarray in Python'

my_encoding = {
    'time': {
        'dtype': 'int64',
        '_FillValue': None
        },
    'latitude': {
        'dtype': 'float64',
        '_FillValue': None
        },
    'longitude': {
        'dtype': 'float64',
        '_FillValue': None
        },
    'sea_water_temperature_at_sea_floor': {
        'dtype': 'float64',
        '_FillValue': 1e20,
        'zlib': False
        },
    'light_intensity_at_sea_floor': {
        'dtype': 'float64',
        '_FillValue': 1e20,
        'zlib': False
        }
    }

# #Set global attributes
# for k, v in global_attributes_dict.items():
#     try:
#         # Clean up attribute name by removing leading and trailing spaces
#         clean_key = k.strip()
        
#         # Check for illegal characters in the cleaned attribute name
#         if not all(c.isalnum() or c in ['_', '-'] for c in clean_key):
#             raise ValueError(f"Illegal character detected in attribute name '{k}'")
        
#         print(f"Attempting to set attribute '{clean_key}' with value '{v}'")
#         xrds.attrs[clean_key] = v
#     except Exception as e:
#         print(f"Error setting attribute '{clean_key}': {e}")

print(xrds)
# for varname, variable in xrds.variables.items():
#     print(f"Variable '{varname}' attributes: {variable.attrs}")
#print(xr.__version__)
# #xrds['time'].attrs.pop('units', None)

#xrds.to_netcdf(r"D:\spyder\logIsfjorden\nc\s2d.nc",encoding=my_encoding)


# # for key, value in xrds['light_intensity_at_sea_floor'].attrs.items():
# #     print(f'{key}: {value}')

#import os
# path = r"D:\spyder\logIsfjorden\nc\s2d.nc"
# file_size_mb = os.path.getsize(path)/(1024*1024)
# os.path.getsize(path)
# print(f"{file_size_mb:.2f}")
    



