import netCDF4 as nc4
import random
import numpy as np
import datetime


sample_size = 10
lon = [random.uniform(45.2, 101.7) for i in range(sample_size)]
lat = [random.uniform(-30.4, 25.8) for i in range(sample_size)]
cnts = [random.randint(0, 100) for i in range(sample_size)]
cities = ['Amsterdam', 'Barcelona', 'Paris', 'Geneva', 'Munich',
          'Athens', 'Vienna', 'Karachi', 'Islamabad', 'Multan']


def randomtimes(n):
    start = "20-01-2018 13:30:00"
    end = "23-01-2022 04:50:34"
    frmt = '%d-%m-%Y %H:%M:%S'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    td = etime - stime
    return [(random.random() * td + stime).toordinal() for _ in range(n)]


f = nc4.Dataset('sample.nc', 'w', format='NETCDF4')  # 'w' stands for write
f.createDimension('lon', len(lon))
f.createDimension('lat', len(lat))
f.createDimension('count', len(cnts))
f.createDimension('city', len(cities))
f.createDimension('time', None)

str_type = f.createVLType(str, 'strtype')

longitude = f.createVariable('Longitude', 'f4', 'lon')
latitude = f.createVariable('Latitude', 'f4', 'lat')
time = f.createVariable('Time', 'i4', 'time')
city = f.createVariable('City', str_type, 'city')

wikipedia_wc = f.createVariable('wikipediaWC', 'i4', 'count')
population = f.createVariable('population', 'f4', ('time', 'lon', 'lat'))
population_city = f.createVariable('populationCity', 'f4', ('time', 'city'))

longitude[:] = lon
latitude[:] = lat
for i, c in enumerate(cities):
    city[i] = c
time[:] = randomtimes(len(lat))
wikipedia_wc[:] = cnts
population[:] = np.random.randint(
    10000, 5000000, size=(len(lon), len(lat), len(time)))
population_city[:] = np.random.randint(
    10000, 5000000, size=(len(time), len(cities)))

print(f)

f.close()
