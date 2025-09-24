# Risk Analysis Workshop

This project shows how to access ERA5 meteorological data from Earthmover's Arraylake platform.

## Features

- **Spatial analysis**: Plot ERA5 variables globally and regionally,
- **Temporal analysis**: Plot timeseries of ERA5 variables at specific locations.

## Quick Start

First [install uv](https://docs.astral.sh/uv/getting-started/installation/), then launch the interactive marimo notebook using uvx:

```bash
# Heating demand analysis
uvx --from . marimo run era5.py
```

Or install all dependencies locally and run:

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