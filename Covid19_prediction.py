#Covid19 prediction
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

#Load data
data = pd.read_csv('covid_19_data.csv', parse_dates = ['ObservationDate' , 'Last Update'])
data.head(10)
data.describe()
data.info()
data.isnull().sum()

data.shape
print('Last Updated:' +str(data.ObservationDate.max()))
data = data.drop(['SNo','Last Update'], axis = 1)
data.head()

data = data.rename(columns = {'ObservationDate':'Date', 'Country/Region':'Country','Province/State':'State'})

data.Country = data.Country.str.replace('Hong Kong SAR', 'HongKong')
data.Country = data.Country.str.replace('Taipei and environs', 'Taiwan')
data.Country = data.Country.str.replace('Republic of Korea', 'SouthKorea')
data.Country = data.Country.str.replace('Viet Nam', 'Vietnam')
data.Country = data.Country.str.replace('occupied Palestinian territory', 'Palestine')
data.Country = data.Country.str.replace('Macao SAR', 'Macau')
data.Country = data.Country.str.replace('Russian Federation', 'Russia')
data.Country = data.Country.str.replace('Republic of Moldova', 'Moldova')
data.Country = data.Country.str.replace('Holy See', 'VaticanCity')
data.Country = data.Country.str.replace('Iran \(Islamic Republic of\)', 'Iran')
data.Country = data.Country.str.replace('Mainland China', 'China')
data.Country = data.Country.str.replace('Sri Lanka', 'SriLanka')
data.Country = data.Country.str.replace('United Arab Emirates', 'UAE')
data.Country = data.Country.str.replace('North Macedonia', 'NorthMacedonia')
data.Country = data.Country.str.replace('San Marino', 'SanMarino')
data.Country = data.Country.str.replace('New Zealand', 'NZ')
data.Country = data.Country.str.replace('Czech Republic', 'CzechRepublic')
data.Country = data.Country.str.replace('Dominican Republic', 'DominicanRepublic')
data.Country = data.Country.str.replace('Saudi Arabia', 'Saudi')
data.Country = data.Country.str.replace('Saint Barthelemy', 'Barthelemy')
data.Country = data.Country.str.replace('Faroe Islands', 'Faroe')
data.Country = data.Country.str.replace('Bosnia and Herzegovina', 'B&H')
data.Country = data.Country.str.replace('South Africa', 'SA')
data.Country = data.Country.str.replace('Costa Rica', 'CostaRica')
data.Country = data.Country.str.replace('Vatican City', 'VaticanCity')
data.Country = data.Country.str.replace('French Guiana', 'FrenchGuiana')
data.Country = data.Country.str.replace('Faroe Islands', 'Faroe')
data.Country = data.Country.str.replace('St. Martin', 'StMartin')
data.Country = data.Country.str.replace('Saint Martin', 'StMartin')
data.Country = data.Country.str.replace('Burkina Faso', 'BurkinaFaso')
data.Country = data.Country.str.replace('Channel Islands', 'ChannelIslands')
data.Country = data.Country.str.replace('North Ireland', 'NorthIreland')
data.Country = data.Country.str.replace('Republic of Ireland', 'Ireland')
data['Country'].unique()


daily = data.sort_values(['Date','Country','State'])

#Segemnting data into different groups

def groups(row):
    if row['State'] == 'Hubei':
        return 'Hubei region'
    elif row['Country'] == 'China':
        return 'Other states'
    else: return 'World'

daily['Segment'] = daily.apply(lambda row: groups(row),axis = 1)    

latest = daily[daily.Date == daily.Date.max()]       
print('total number of cases: %d' %np.sum(latest['Confirmed']))
print('total number of deaths: %d' %np.sum(latest['Deaths']))
print('total number of recovered: %d' %np.sum(latest['Recovered']))

print('total number of cases: %d' %np.sum(daily['Confirmed']))
print('total number of deaths: %d' %np.sum(daily['Deaths']))
print('total number of recovered: %d' %np.sum(daily['Recovered']))

segment_latest = latest.groupby('Segment').sum()
segment_daily = daily.groupby('Segment').sum()

segment_latest['Death Rate'] = segment_latest['Deaths']/segment_latest['Confirmed']*100
segment_latest['Recovery Rate'] = segment_latest['Recovered']/segment_latest['Confirmed']*100

segment_daily['Death Rate'] = segment_daily['Deaths']/segment_daily['Confirmed']*100
segment_daily['Recovery Rate'] = segment_daily['Recovered']/segment_daily['Confirmed']*100

print('Total Death rate latest: %d' %np.sum(segment_latest['Death Rate'])+ str('%'))
print('Total Death rate daily: %d' %np.sum(segment_daily['Death Rate'])+ str('%'))

print('Total Recovery rate latest: %d' %np.sum(segment_latest['Recovery Rate'])+ str('%'))
print('Total Recovery rate daily: %d' %np.sum(segment_daily['Recovery Rate'])+ str('%'))

#Confirmed cases in China execpt Hubei
_ = latest.loc[latest.Segment=='Other states',['State','Confirmed']].sort_values('Confirmed',ascending = False)
plt.figure(figsize=(10,8))
sns.barplot('Confirmed','State',data = _)
plt.title('Top confirmed states in china')
plt.yticks()
plt.grid(axis = 'x')
plt.show()

_ = daily.loc[daily.Segment=='Other states',['State','Confirmed']].sort_values('Confirmed',ascending = False)
plt.figure(figsize=(10,8))
sns.barplot('Confirmed','State',data = _)
plt.title('Top confirmed states in china total')
plt.yticks()
plt.grid(axis = 'x')
plt.show()


#Death cases in China execpt Hubei
_ = latest.loc[latest.Segment=='Other states',['State','Deaths']].sort_values('Deaths',ascending = False)
plt.figure(figsize=(10,8))
sns.barplot('Deaths','State',data = _)
plt.title('Top deaths states in china')
plt.yticks()
plt.grid(axis = 'x')
plt.show()

#Recovered cases in China execpt Hubei
_ = latest.loc[latest.Segment=='Other states',['State','Recovered']].sort_values('Recovered',ascending = False)
plt.figure(figsize=(10,8))
sns.barplot('Recovered','State',data = _)
plt.title('Top recovered states in china')
plt.yticks()
plt.grid(axis = 'x')
plt.show()

#Top 25 affected countries
worldstat = latest[latest.Segment=='World'].groupby('Country').sum()
_ = worldstat.sort_values('Confirmed',ascending = False).head(25)
c10 = _.index.tolist()
plt.figure(figsize=(10,8))
sns.barplot(_.Confirmed,_.index)
plt.title('Top 25 affected countries')
plt.xticks()
plt.grid(axis = 'x')
plt.show()

_ = worldstat.sort_values('Deaths',ascending = False).head(25)
c10 = _.index.tolist()
plt.figure(figsize=(10,8))
sns.barplot(_.Deaths,_.index)
plt.title('Top 25 affected countries number of deaths')
plt.xticks()
plt.grid(axis = 'x')
plt.show()

_ = worldstat.sort_values('Recovered',ascending = False).head(25)
c10 = _.index.tolist()
plt.figure(figsize=(10,8))
sns.barplot(_.Recovered,_.index)
plt.title('Top 25 affected countries number of recovery')
plt.xticks()
plt.grid(axis = 'x')
plt.show()

#Death rates in the world
_ = latest.groupby('Country')['Confirmed', 'Deaths'].sum().reset_index()
_['Death Rate'] = _['Deaths']/_['Confirmed']*100
_ = _.sort_values('Death Rate',ascending =False)
Death = _[_['Deaths']>0]
plt.figure(figsize = (10,8))
sns.barplot(Death['Death Rate'],Death['Country'])
plt.title('Death Rate across globe')
plt.yticks()
plt.show()

#Recovered rate
_ = latest.groupby('Country')['Confirmed','Recovered'].sum().reset_index()
_['Recovery rate'] = _['Recovered']/_['Confirmed']*100
_= _.sort_values('Recovery rate',ascending = False)
Recovered = _[_['Recovered']>0]
plt.figure(figsize = (10,8))
sns.barplot(Recovered['Recovery rate'],Recovered['Country'])
plt.title('Recovery rate across globe')
plt.yticks()
plt.show()


#Evolution of virus over time in china
confirm = pd.pivot_table(daily.dropna(subset = ['Confirmed']),columns = 'Segment',values = 'Confirmed',index = 'Date',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(confirm,marker = 'o')
plt.title('Confirmed cases')
plt.legend(confirm.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

#Death due to virus over time in china
death = pd.pivot_table(daily.dropna(subset = ['Deaths']),columns = 'Segment',values = 'Deaths',index = 'Date',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(death,marker = 'o')
plt.title('Death cases')
plt.legend(death.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

#Recoveries after virus attack in China
recovery = pd.pivot_table(daily.dropna(subset = ['Recovered']),columns = 'Segment',values = 'Recovered',index = 'Date',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(recovery,marker = 'o')
plt.title('Recovered cases')
plt.legend(recovery.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

#Active cases in China
daily['Active'] = daily['Confirmed'] - daily['Deaths'] - daily['Recovered']
active = pd.pivot_table(daily.dropna(subset = ['Active']),columns = 'Segment',values = 'Active',index = 'Date',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(active,marker = 'o')
plt.title('Active cases')
plt.legend(active.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

#Evolution of virus in the world
country10 = daily[daily['Country'].isin(c10)]
confirm_w = pd.pivot_table(daily.dropna(subset = ['Confirmed']),columns = 'Country', index = 'Date',values = 'Confirmed',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(confirm_w[confirm_w.index>'2020-02-01'],marker = 'o')
plt.title('Confirmed cases across globe')
plt.legend(confirm_w.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

#Death due to virus in the world
death_w = pd.pivot_table(daily.dropna(subset = ['Deaths']),columns = 'Country', index = 'Date',values = 'Deaths',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(death_w[death_w.index>'2020-02-01'],marker = 'o')
plt.title('Death cases across globe')
plt.legend(death_w.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

#Recovered from virus across the globe
recover_w = pd.pivot_table(daily.dropna(subset = ['Recovered']),columns = 'Country', index = 'Date',values = 'Recovered',aggfunc = np.sum).fillna(method = 'ffill')
plt.figure(figsize =(10,8))
plt.plot(recover_w[recover_w.index>'2020-02-01'],marker = 'o')
plt.title('Recovered cases across globe')
plt.legend(recover_w.columns, loc = 2)
plt.xticks(rotation = 45)
plt.show()

