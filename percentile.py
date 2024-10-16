import pyarrow.parquet as parquet
import numpy as np
import plotext as plot

parquet_file = 'yellow_tripdata_2024-07.parquet'  
schema = parquet.read_schema(parquet_file, memory_map=True)
# print(schema)
table = parquet.read_table(parquet_file)

total_amount = np.array(table['total_amount'])
trip_distance = np.array(table['trip_distance'])

# Trips with a non-positive total_amount are invalid
# Trips with a non-positive distance are invalid
valid_rows = (trip_distance > 0) & (total_amount > 0)
total_amount = total_amount[valid_rows]
trip_distance = trip_distance[valid_rows]

total_amount_threshold = 250  # total_amount
trip_distance_threshold = 100 # miles

where_clause = np.where((total_amount > total_amount_threshold) & (trip_distance > trip_distance_threshold))

# Get the top 10 rows based on total_amount, where both total_amount and trip_distance exceed our defined weights
top_10 = np.argsort(total_amount[where_clause])[-10:][::-1]

# Retrieve the top 10 values for both columns using the filtered indices
top_total_amount = total_amount[where_clause][top_10]
top_trip_distance = trip_distance[where_clause][top_10]

price_per_mile=[]

# Get price/mile 
for i in range(10):
    price_per_mile.append(top_total_amount[i] / top_trip_distance[i])

price_per_mile = np.asarray(price_per_mile, dtype='float64')
min_price = np.min(price_per_mile)
max_price = np.max(price_per_mile)
print(f"Computed min_price: {min_price}")
print(f"Computed max_price: {max_price}")

# Retrieve trips which fall under min/max price per mile
trip_rates = np.where(trip_distance > 0, total_amount / trip_distance, np.inf)
filtered_trip_distances = trip_distance[(trip_rates >= min_price) & (trip_rates <= max_price)]

# Calculate percentiles
min_trip_distance = np.min(filtered_trip_distances)
avg_trip_distance = np.mean(filtered_trip_distances)
p90_trip_distance = np.percentile(filtered_trip_distances, 90)
p99_trip_distance = np.percentile(filtered_trip_distances, 99)
p999_trip_distance = np.percentile(filtered_trip_distances, 99.9)
max_trip_distance = np.max(filtered_trip_distances)

plot.hist(filtered_trip_distances, bins=30, color='skyblue')
plot.title('Histogram of Trip Distances')
plot.xlabel('Trip Distance (miles)')
plot.ylabel('Frequency')
plot.show()

# Print the percentile chart
print(f"Trip Distance Statistics:")
print(f"Minimum: {min_trip_distance:.2f}")
print(f"Average: {avg_trip_distance:.2f}")
print(f"90th Percentile (P90): {p90_trip_distance:.2f}")
print(f"99th Percentile (P99): {p99_trip_distance:.2f}")
print(f"99.9th Percentile (P99.9): {p999_trip_distance:.2f}")
print(f"Maximum: {max_trip_distance:.2f}")

