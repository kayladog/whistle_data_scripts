import pandas as pd
import matplotlib.pyplot as plt
from pick import pick
pd.options.mode.chained_assignment = None

def process_data():
    #process distance metric and truncate timestamp date
    df = pd.read_csv('dailies.csv')
    table_dist = df[['timestamp','distance']]
    table_dist['timestamp'] = pd.to_datetime(table_dist['timestamp']).dt.date
    table_dist = table_dist.rename(columns = {'timestamp':'date'})
    #process health metrics
    df = pd.read_csv('daily_health_trends.csv')
    table_health = df[['start_date','lick_measured','scratch_measured']]
    table_health['start_date'] = pd.to_datetime(table_health['start_date']).dt.date
    table_health = table_health.rename(columns = {'start_date':'date'})   
    #merge tables
    merged = table_dist.merge(table_health,how='outer',left_on='date',right_on='date')
    merged = merged.sort_values('date')
    return merged

def prompt():
	title = "Please choose the desired metric(s) to visualize"
	options = ['distance','scratching','licking','licking and scratching']
	option, index = pick(options,title)
	return option

def valid_input(date_str):
	if date_str is None or len(date_str)==0:
		return False
	date_list = date_str.strip().split('-')
	date_list = [int(x) for x in date_list]
	if len(date_list) != 3:
		return False
	start = pd.Timestamp(2019,8,1)
	end = pd.Timestamp(2020,8,11)
	try:
		date_obj = pd.Timestamp(date_list[2],date_list[0],date_list[1])
	except ValueError:
		return False
	if date_obj >= start and date_obj <= end:
		return True
	else:
		return False

def get_timestamp(date_str):
	date_list = date_str.strip().split('-')
	date_list = [int(x) for x in date_list]
	return pd.Timestamp(date_list[2],date_list[0],date_list[1])

def get_date_range():
	print('Current dataset contains 08-01-2019 to 08-11-2020')
	start = input('Enter starting date for the graph (in format MM-DD-YYYY):')
	end = input('Enter ending date for the graph (in format MM-DD-YYYY):')
	if valid_input(start) and valid_input(end):
		start_ = get_timestamp(start)
		end_ = get_timestamp(end)
		if start_ < end_:
			return (start_,end_)
	print('Invalid input or date out of dataset range')
	exit(1)

def make_plot(df,metrics,times):
	m = {'distance' : 'distance',
		'scratching' : 'scratch_measured',
		'licking' : 'lick_measured',
		'licking and scratching' : ['scratch_measured','lick_measured']
	}
	tmp = df[(df['date'] >= times[0]) & (df['date'] <= times[1])]
	tmp.plot(x='date',y=m[metrics])
	plt.xlabel('Day')
	plt.ylabel(metrics)
	plt.title('Kayla\'s ' + metrics)
	plt.show()
	plt.close()

kayla_db = process_data()
metric = prompt()
time_range = get_date_range()
make_plot(kayla_db,metric,time_range)