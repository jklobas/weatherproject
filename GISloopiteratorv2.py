#For the computation of average temperatures using GHCN data


import ulmo, pandas as pd, matplotlib.pyplot as plt, numpy as np, csv, pickle

#Grab weather stations that meet criteria (from previous work) and assign lists
st = ulmo.ncdc.ghcn_daily.get_stations(country ='US',elements=['TMAX'],end_year=1950, as_dataframe = True)
ids = pd.read_csv('IDfile.csv')
idnames = [ids.id[x] for x in range(0, len(ids))]
Longitude= []
Latitude = []
ID = []
Elev = []
Name = []
Tmaxavgresult = []
Tminavgresult = []
Tmaxavg = []
Tminavg = []
Tmaxstd = []
Tminstd = []
Tmaxz = []
Tminz = []
Tmaxanom = []
Tminanom = []
maxset = []
minset = []
#
#
#begin loop to isolate values of interest
#
#test loop to verify if works
#rando = np.random.random_integers(len(idnames), size = (10,))
#for x in rando:
for q in range(0,len(ids)-1):




#   Grab data and transform to K

    a = st.id[idnames[q]]
    data = ulmo.ncdc.ghcn_daily.get_data(a, as_dataframe=True)
    tmax = data['TMAX'].copy()
    tmin = data['TMIN'].copy()
    tmax.value = (tmax.value/10.0) + 273.15
    tmin.value = (tmin.value/10.0) + 273.15
    
    
    
#   Name and save parameters
    
    b = st.longitude[idnames[q]]
    c = st.latitude[idnames[q]]
    d = st.elevation[idnames[q]]
    e = st.name[idnames[q]]

    

#average only data on a monthly basis and generate x and y coordinates for the years in which El Nino data exists (probably a way more efficient way to do this)
    filedatasmax = []
    filedatasmin = []
    for y in range(1951,2016):
        filedatamax = {}
        filedatamin = {}
        
        datejan = ''.join([str(y),"-01"])
        datefeb = ''.join([str(y),"-02"])
        datemar = ''.join([str(y),"-03"])
        dateapr = ''.join([str(y),"-04"])
        datemay = ''.join([str(y),"-05"])
        datejun = ''.join([str(y),"-06"])
        datejul = ''.join([str(y),"-07"])
        dateaug = ''.join([str(y),"-08"])
        datesep = ''.join([str(y),"-09"])
        dateoct = ''.join([str(y),"-10"])
        datenov = ''.join([str(y),"-11"])
        datedec = ''.join([str(y),"-12"])
        
        nanmaxjan = tmax['value'][datejan]
        nanminjan = tmin['value'][datejan]
        nanmaxfeb = tmax['value'][datefeb]
        nanminfeb = tmin['value'][datefeb]
        nanmaxmar = tmax['value'][datemar]
        nanminmar = tmin['value'][datemar]
        nanmaxapr = tmax['value'][dateapr]
        nanminapr = tmin['value'][dateapr]
        nanmaxmay = tmax['value'][datemay]
        nanminmay = tmin['value'][datemay]
        nanmaxjun = tmax['value'][datejun]
        nanminjun = tmin['value'][datejun]
        nanmaxjul = tmax['value'][datejul]
        nanminjul = tmin['value'][datejul]
        nanmaxaug = tmax['value'][dateaug]
        nanminaug = tmin['value'][dateaug]
        nanmaxsep = tmax['value'][datesep]
        nanminsep = tmin['value'][datesep]
        nanmaxoct = tmax['value'][dateoct]
        nanminoct = tmin['value'][dateoct]
        nanmaxnov = tmax['value'][datenov]
        nanminnov = tmin['value'][datenov]
        nanmaxdec = tmax['value'][datedec]
        nanmindec = tmin['value'][datedec]
        
        #We now concatenate everything
        
        filedatamax = [y, nanmaxjan[~pd.isnull(nanmaxjan)].mean(), nanmaxfeb[~pd.isnull(nanmaxfeb)].mean(),nanmaxmar[~pd.isnull(nanmaxmar)].mean(),nanmaxapr[~pd.isnull(nanmaxapr)].mean(),nanmaxmay[~pd.isnull(nanmaxmay)].mean(),nanmaxjun[~pd.isnull(nanmaxjun)].mean(),nanmaxjul[~pd.isnull(nanmaxjul)].mean(),nanmaxaug[~pd.isnull(nanmaxaug)].mean(),nanmaxsep[~pd.isnull(nanmaxsep)].mean(),nanmaxoct[~pd.isnull(nanmaxoct)].mean(),nanmaxnov[~pd.isnull(nanmaxnov)].mean(),nanmaxdec[~pd.isnull(nanmaxdec)].mean() ]
        filedatamin = [y, nanminjan[~pd.isnull(nanminjan)].mean(), nanminfeb[~pd.isnull(nanminfeb)].mean(),nanminmar[~pd.isnull(nanminmar)].mean(),nanminapr[~pd.isnull(nanminapr)].mean(),nanminmay[~pd.isnull(nanminmay)].mean(),nanminjun[~pd.isnull(nanminjun)].mean(),nanminjul[~pd.isnull(nanminjul)].mean(),nanminaug[~pd.isnull(nanminaug)].mean(),nanminsep[~pd.isnull(nanminsep)].mean(),nanminoct[~pd.isnull(nanminoct)].mean(),nanminnov[~pd.isnull(nanminnov)].mean(),nanmindec[~pd.isnull(nanmindec)].mean() ]
        
        filedatasmax.append(filedatamax)
        filedatasmin.append(filedatamin)
        
        #extract monthly datas
    y_listmax = [filedatasmax[l][1:13] for l in range(0,len(filedatasmax))]
    y_listmin = [filedatasmin[l][1:13] for l in range(0,len(filedatasmin))]
    yvalmax = [ [ y_listmax[y][x] for y in range(0, len(y_listmax))] for x in range(0,12)]
    yvalmin = [ [ y_listmin[y][x] for y in range(0, len(y_listmin))] for x in range(0,12)]
    avgmax = [np.nanmean(yvalmax[x]) for x in range(0, len(yvalmax))]
    avgmin = [np.nanmean(yvalmin[x]) for x in range(0, len(yvalmin))]
    stdmax = [np.nanstd(yvalmax[x]) for x in range(0,len(yvalmax))]
    stdmin = [np.nanmean(yvalmin[x]) for x in range(0,len(yvalmin))]
    anommax = [ [ filedatasmax[x][y] - avgmax[y-1] for y in range(1,13)] for x in range(0,len(filedatasmax)-1) ]
    zmax = [ [ (filedatasmax[x][y] - avgmax[y-1]) / stdmax[y-1]  for y in range(1,13)] for x in range(0, len(filedatasmax)-1)]
    anommin = [ [ filedatasmin[x][y] - avgmin[y-1] for y in range(1,13)] for x in range(0,len(filedatasmax)-1) ]
    zmin = [ [ (filedatasmin[x][y] - avgmin[y-1]) / stdmin[y-1]  for y in range(1,13)] for x in range(0, len(filedatasmax)-1)]
    

    
#   build the big list elements
    
    ID.append(a)
    Longitude.append(b)
    Latitude.append(c)
    Elev.append(d)
    Name.append(e)
    Tmaxavgresult.append(filedatasmax)
    Tminavgresult.append(filedatasmin)
    Tmaxavg.append(avgmax)
    Tminavg.append(avgmin)
    Tmaxstd.append(stdmax)
    Tminavg.append(stdmin)
    Tmaxanom.append(anommax)
    Tmaxz.append(zmax)
    Tminanom.append(anommin)
    Tminz.append(zmin)
    
    #monitor progress because scraping the database takes a while
    print(e)
    print(len(ids)-q)

    
#   concatenate and save the list (150 MB file or so)

biglist = [ID, Name, Elev, Latitude, Longitude, Tmaxavgresult, Tmaxavg, Tmaxstd, Tmaxanom, Tmaxz, Tminavgresult, Tminavg, Tminstd, Tminanom, Tminz ]

with open('biglist.pkl', 'wb') as pickle_file:
    pickle.dump(biglist, pickle_file, protocol = pickle.HIGHEST_PROTOCOL)
