# NYC Yellow Taxi Trips Data

This repo contains sample code on how to work with [Apache Parquet](https://parquet.apache.org/) using NYC _Yellow Taxi_ Trips Data from [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

## Docker Quickstart

The easiest way to get started is by building a Docker container, this avoids problems with compiling PyArrow's to your host machine. 

1. Clone this repo and from your terminal, run:

```shell
docker build -t percentile .
```

2. Start the container:

```shell
docker run --rm percentile
```

## Running on the host

Building a full-blown container is likely an overkill for the purposes of this repo. Here are the instructions on how to run it on a Linux/Mac OS host:

1. Create and activate a virtual environment

```shell 
python3 -m venv venv
source venv/bin/activate
```

2. Install all dependencies (refer to [Apache Arrow Build documentation](https://arrow.apache.org/docs/developers/python.html#building-on-linux-and-macos) should you have trouble here.

```shell
pip3 install -r requirements.txt
```

3. Run the code
```shell
python3 percentile.py
```

# The Fun (Assumptions) Part
As one can imagine, Taxi Data is subject to various skews. Taximeters break, passenger count is manually input by the driver, total cost doesn't reflect the actual distance reported, among other things.

Although the naive `pandas` approach would "_solve_" the problem at hand with a few code lines, the reported numbers would be totally inaccurate with reality. That said, `pandas` can be reportedly slow (and it particularly annoys me, even for such small parquet file) and - even then - `pandas.quantile()` method may introduce slight inaccuracies, and playing with interpolation methods isn't fun.

That said, the solution at hand relies solely on `NumPy` and `PyArrow`. The performance still isn't great (Rust would be a better tool for the job), but the problem at hand requested for a "_developer-friendly_" code, which means most users are more familiar with Python.

The following assumptions were used when coming up with the logic for the code:

- We are only interested in trips whose **distance and amount** are higher than 0
- We apply a weighted approach. This is done in order to prevent accounting for long trips with an inconsistent pricing amount.
  - Retrieve all trips whose `total_amount > 250` and `distance > 100`
  - Under these restrictions, rank the top 10 trips
  - Compute the minimum and maximum price per mile (price/mile)
- Retrieve all trips such that `total_amount / trip_distance` fall under the previously computed minimum/maximum price per mile rates.
- From these trips, calculate the percentiles
- Present a histogram of all trip distances used for the calculation. Maximum was roughly (because `plotext` and `numpy` hate each other, and I didn't bother checking) 310 miles, which is reasonable as we can imagine wealthy people missing flights and taking a taxi to cross a state instead. :-)

# Room for Improvements

Plenty. Such as:

1. Better structure the code
2. Use Rust instead
3. Allow for user input, such as eg: loading his own parquet file, download from URI, etc
4. Use matplotlib, Flask, asyncio, allow for user manipulation and him to do his own thingie
5. Build more diverse charts. People love staring at charts.
