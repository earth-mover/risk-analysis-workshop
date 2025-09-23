# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "arraylake==0.24.0",
#     "cartopy==0.25.0",
#     "dask==2025.9.1",
#     "flox==0.10.6",
#     "icechunk==1.1.5",
#     "matplotlib==3.10.6",
#     "metpy==1.7.1",
#     "pint==0.25",
#     "pint-xarray==0.6.0",
#     "xarray==2025.9.0",
#     "xclim==0.58.1",
# ]
# ///

import marimo

__generated_with = "0.16.1"
app = marimo.App(width="medium")


@app.cell
def _():
    # Marimo notebook
    import marimo as mo

    # Core Earthmover stack
    import arraylake as al
    import icechunk as ic
    import xarray as xr

    # Climate indices
    import metpy
    import xclim

    # Physical units support
    import pint
    import pint_xarray
    from metpy.units import units

    # Maps
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    # Speeds up groupby / coarsen
    import flox
    return al, ccrs, cfeature, mo, pint, plt, units, xr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Connect to Arraylake""")
    return


@app.cell
def _(al):
    client = al.Client()
    client.login()
    return (client,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## ERA5""")
    return


@app.cell
def _(client):
    al_repo = client.get_repo_object("earthmover-public/era5-surface-aws")
    return (al_repo,)


@app.cell
def _(al_repo):
    al_repo
    return


@app.cell
def _(client):
    ic_repo = client.get_repo("earthmover-public/era5-surface-aws")
    return (ic_repo,)


@app.cell
def _(ic_repo):
    session = ic_repo.readonly_session("main")
    return (session,)


@app.cell
def _(session, xr):
    ds = xr.open_dataset(session.store, group="spatial", engine="zarr", zarr_format=3, chunks={})
    ds
    return (ds,)


@app.cell
def _(ds):
    print(f"This repo contains {ds.nbytes / 1e12:.2g} TB of data!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Total Cloud Cover""")
    return


@app.cell
def _(ds):
    ds["tcc"].attrs
    return


@app.cell
def _(ccrs, ds):
    p1 = (
        ds["tcc"]
        .sel(time="2024-09-23T15:00:00", method="nearest")
        .plot(
            subplot_kws={"projection": ccrs.Orthographic(-73.99, 40.73), "facecolor": "gray"},
            transform=ccrs.PlateCarree(),
        )
    )
    p1.axes.set_global()
    p1.axes.coastlines()
    return


@app.cell
def _(mo):
    mo.md(r"""## Spatial Analysis: Wet bulb temperature""")
    return


@app.cell
def _():
    from metpy.calc import wet_bulb_temperature
    return (wet_bulb_temperature,)


@app.cell
def _(ds):
    india_bbox = {
        "longitude": slice(67, 99),
        "latitude": slice(5, -37.5),
    }
    ds_india = ds.sel(**india_bbox, time="2024-05-28T10:00:00")
    ds_india
    return (ds_india,)


@app.cell
def _(ds_india, pint, wet_bulb_temperature):
    wbt = wet_bulb_temperature(
        pressure=ds_india["sp"].pint.quantify(),
        temperature=ds_india["t2"].pint.quantify(),
        dewpoint=ds_india["d2"].pint.quantify(),
    ).pint.to(pint.Unit("degF"))
    wbt
    return (wbt,)


@app.cell
def _(ccrs, cfeature, plt, wbt):
    # Minimal plot to see if data appears
    p2 = wbt.plot(
        subplot_kws={"projection": ccrs.PlateCarree()},
        transform=ccrs.PlateCarree(),
    )

    india_extent = [68, 97, 6, 38]
    p2.axes.set_extent(india_extent, crs=ccrs.PlateCarree())


    p2.axes.coastlines()
    p2.axes.add_feature(cfeature.BORDERS)


    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"""## Temporal Analysis: Heat wave index""")
    return


@app.cell
def _(session, xr):
    ds_temporal = xr.open_dataset(session.store, group="temporal", engine="zarr", zarr_format=3, chunks={})
    ds_temporal
    return (ds_temporal,)


@app.cell
def _(ds_temporal):
    nyc_coords = {"latitude": 40.730026, "longitude": (360-73.990185)}

    ds_nyc = ds_temporal[['t2', 'd2']].sel(**nyc_coords, method="nearest").load()
    ds_nyc
    return (ds_nyc,)


@app.cell
def _(ds_nyc):
    ds_nyc.nbytes * 144 / 1e6
    return


@app.cell
def _():
    from metpy.calc import relative_humidity_from_dewpoint
    from metpy.calc import heat_index
    return heat_index, relative_humidity_from_dewpoint


@app.cell
def _(ds_nyc, relative_humidity_from_dewpoint, units):
    rel_humid = relative_humidity_from_dewpoint(
        temperature=ds_nyc['t2'] * units.degK,
        dewpoint=ds_nyc['d2'] * units.degK,
    )
    rel_humid
    return (rel_humid,)


@app.cell
def _(rel_humid):
    rel_humid.plot()
    return


@app.cell
def _(ds_nyc, heat_index, rel_humid, units):
    heat_ind = heat_index(
        temperature=ds_nyc['t2'].pint.quantify(units.degK).pint.to(units.degF),
        relative_humidity=rel_humid,
        mask_undefined=False,
    ).pint.to(units.degF)

    heat_ind_daily_max = heat_ind.coarsen(time=24).max()
    heat_ind_daily_max
    return (heat_ind_daily_max,)


@app.cell
def _(heat_ind_daily_max):
    heat_ind_daily_max.plot()
    return


@app.cell
def _(heat_ind_daily_max):
    heat_ind_daily_max
    return


@app.cell
def _():
    from xclim.indices import heat_wave_index
    return (heat_wave_index,)


@app.cell
def _(heat_ind_daily_max, heat_wave_index):
    # use NYC definition of heat wave (https://nychazardmitigation.com/documentation/hazard-profiles/extreme-heat/)
    heat_wave_index(
        heat_ind_daily_max.pint.dequantify(), 
        thresh='95.0 degF', 
        window=2,
    ).plot()
    return


if __name__ == "__main__":
    app.run()
