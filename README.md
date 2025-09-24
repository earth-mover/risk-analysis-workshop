# Risk Analysis Workshop

This project shows how to access ERA5 meteorological data from Earthmover's Arraylake platform.

## Features

- **Spatial analysis**: Plot ERA5 variables globally and regionally,
- **Temporal analysis**: Plot timeseries of ERA5 variables at specific locations.

## Quick Start

First [install uv](https://docs.astral.sh/uv/getting-started/installation/), then launch the interactive marimo notebook using uvx:

```bash
uvx marimo edit --sandbox https://github.com/earth-mover/risk-analysis-workshop/blob/main/era5.py
```

then press `n` to say that you trust that we aren't trying to give you a virus.
Your browser should open a snazzy marimo notebook. 
Press ctrl-enter to run each cell one-by-one.

Or alternatively install all dependencies locally and run:

```bash
uv sync
marimo run era5.py
```

## Data Sources

- **ERA5 Surface Data**: Accessed via Arraylake from [`earthmover-public/era5-surface-aws`](https://app.earthmover.io/earthmover-public/era5-surface-aws)

## Key Technologies

- **arraylake**: Earthmover's data platform for cataloging and governing access to scientific data
- **icechunk**: Cloud-native transactional backend for Zarr
- **xarray**: Multi-dimensional array processing

## License

Apache 2.0