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

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Climate risk indicators from ERA5

    We will access the copy of ERA5 surface data on Arraylake, then calculate some climate risk indicators. To do this we will run basic Xarray queries that are accelerated by Icechunk, experiencing the speed of the Earthmover platform firsthand.
    """
    )
    return


@app.cell
def _():
    # marimo notebook
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
    return al, ccrs, cfeature, mo, pint, units, xr


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Connect to Arraylake

    Now let's login to arraylake. We can [login to the web app](https://app.earthmover.io/earthmover-public/era5-surface-aws), or log in from the notebook programatically via the client.
    """
    )
    return


@app.cell
def _(al):
    client = al.Client()
    client.login()
    return (client,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## ERA5 in Icechunk

    The `earthmover-public` org in arraylake contains some example public datasets. Let's take a look at the ECMWF Reanalysis v5 dataset, more commonly known as ERA5. We can [view the ERA5 repo in the arraylake web app](https://app.earthmover.io/earthmover-public/era5-surface-aws).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can alternatively use the client to see information about the repo, such as which bucket the data resides in.""")
    return


@app.cell
def _(client):
    client.get_repo_object("earthmover-public/era5-surface-aws")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Whilst the web app shows us various metadata about the contents of the repo, to actually access data we need to use the client to open the underlying Icechunk repository:""")
    return


@app.cell
def _(client):
    ic_repo = client.get_repo("earthmover-public/era5-surface-aws")
    return (ic_repo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Icechunk is Earthmover's open-source transactional storage engine. You can think of it as "version-controlled, multiplayer Zarr".

    Icechunk is incredibly powerful, and you can read more about it in the [icechunk documentation](https://icechunk.io/en/latest/), and on the [Earthmover Blog](https://earthmover.io/blog).

    For today, in this notebook, Icechunk will mainly be behind-the-scences.

    To access the data in Icechunk via zarr, we need to start an icechunk `Session`, then get the Zarr store object.
    """
    )
    return


@app.cell
def _(ic_repo):
    session = ic_repo.readonly_session("main")
    icechunk_store = session.store
    return icechunk_store, session


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now we have something that xarray can read from!""")
    return


@app.cell
def _(icechunk_store, xr):
    ds = xr.open_dataset(icechunk_store, group="spatial", engine="zarr", zarr_format=3, chunks={})
    ds
    return (ds,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This `xarray.Dataset` represents a lazy view of the data in the `"spatial"` group of the zarr data in the `era5-surface-aws` repo.""")
    return


@app.cell
def _(ds):
    print(f"This repo contains {ds.nbytes / 1e12:.2g} TB of data!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Note that we obviously did not just download 40TB of data in one second - instead we only downloaded the zarr metadata to learn what data we have in the store. This works because Zarr is a [cloud-optimized data format](https://earthmover.io/blog/fundamentals-what-is-cloud-optimized-scientific-data).""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Precipitation

    This dataset has lots of interesting variables, but let's try plotting just one first - precipitation. We can look at the metadata of the `"cp"` variable to confirm that that's the one that represents precipitation.
    """
    )
    return


@app.cell
def _(ds):
    ds["cp"].attrs
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now as this dataset is global, we should pick a map projection, for which we'll use the cartopy library. Let's also pick a date and time to display the data.""")
    return


@app.cell
def _(ccrs, ds):
    p1 = (
        ds["cp"]
        .sel(time="2024-09-24T20:00:00", method="nearest")  # subset to the same date and time last year
        .plot(
            subplot_kws={
                "projection": ccrs.Orthographic(-73.99, 40.73),  # center over NYC
                "facecolor": "gray"
            },
            transform=ccrs.PlateCarree(),
            robust=True,
        )
    )
    p1.axes.set_global()
    p1.axes.coastlines()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Voila! What the convective precipitation looked like globally (centered over New York) on this date and time last year.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Notice that region of high precipitation on the western tip of Cuba - that's [Hurricane Helene](https://en.wikipedia.org/wiki/Hurricane_Helene) developing, which went on to hit the South-Eastern US, causing almost $80 billion in damage.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Spatial Analysis: Wet bulb temperature during 2024 Indian heatwave

    Now let's calculate some quantities related to climate risk.

    We'll start with the [wet bulb temperature](https://en.wikipedia.org/wiki/Wet-bulb_temperature), which is a measure of heat stress, particularly for human health and safety. Prolonged periods above a wet bulb temperature of 95°F are likely to be fatal to even fit and healthy humans.

    Let's look at how high the wet bulb temperature got during the [2024 Indian heatwave](https://en.wikipedia.org/wiki/2024_Indian_heat_wave). We'll start by subsetting to a bounding box over India and Bangladesh, and a specific time within the (months-long) heatwave.
    """
    )
    return


@app.cell
def _(ds):
    india_bbox = {
        "longitude": slice(67, 99),
        "latitude": slice(37.5, 5),
    }

    ds_india = ds[
        ["sp", "t2", "d2"]  # keep only the variables we need to calculate wet bulb temperature
    ].sel(
        **india_bbox, 
        time="2024-05-28T10:00:00",  # subset to a time within the 2024 Indian heatwave
    ).load().pint.quantify()  # use pint-xarray to automatically handle unit conversions

    ds_india
    return (ds_india,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Calculating wet-bulb temperature isn't trivial (it requires an iterative algorithm), but luckily the [MetPy package](https://unidata.github.io/MetPy/latest/index.html) conveniently provides an xarray-aware [function](https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.wet_bulb_temperature.html#wet-bulb-temperature) for calculating wet bulb temperature for us.""")
    return


@app.cell
def _():
    from metpy.calc import wet_bulb_temperature
    return (wet_bulb_temperature,)


@app.cell
def _(ds_india, pint, wet_bulb_temperature):
    wbt = wet_bulb_temperature(
        pressure=ds_india["sp"],
        temperature=ds_india["t2"],
        dewpoint=ds_india["d2"],
    ).pint.to(pint.Unit("degF"))
    wbt
    return (wbt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Note: To understand how on earth all the physical units conversions were just magically handled correctly for us there, [read this blog post about `pint-xarray`](https://xarray.dev/blog/introducing-pint-xarray) that I wrote back in 2022.""")
    return


@app.cell
def _(ccrs, cfeature, wbt):
    p = wbt.plot.contourf(
        subplot_kws={"projection": ccrs.PlateCarree(), "facecolor": "lightgray"},
        transform=ccrs.PlateCarree(),
    )
    p.axes.coastlines(resolution='50m')
    p.axes.add_feature(cfeature.BORDERS)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    If 95F is lethal, then clearly the temperature and humidity was dangerously high over significant areas, particularly in east India and Bangladesh. 

    Indeed there were a total of 219 deaths reported from the heat wave, and 25,000 others suffered from heatstroke ([source: wikipedia](https://en.wikipedia.org/wiki/2024_Indian_heat_wave)).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Temporal Analysis: Heat wave index

    So far we have analysed large spatial regions at specific times. We also do the opposite - analyse trends at specific locations over long time periods. Let's calculate the number of days each year that New York City experienced a heatwave.

    For analyses to work efficiently, our queries need to be aligned with our chunking pattern on-disk. We now want to use the orthogonal query pattern, so let's open a slightly different version of the ERA5 dataset, this time with spatial instead of temporal chunking.
    """
    )
    return


@app.cell
def _(session, xr):
    ds_temporal = xr.open_dataset(session.store, group="temporal", engine="zarr", zarr_format=3, chunks={})
    ds_temporal
    return (ds_temporal,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The official [NYC Hazard Mitigation Plan](https://nychazardmitigation.com/documentation/hazard-profiles/extreme-heat/) defines heatwaves in terms of the National Weather Service's heat index chart. This quantity is a function of air temperature and relative humidity.

    <figure>
      <img src="https://nychazardmitigation.com/wp-content/uploads/2023/01/2024.08.05_12_Heat-Index.png)" alt="Alt text" width="600">
      <figcaption>Heat index table. Source: National Weather Service.</figcaption>
    </figure>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Again we will need both the temperature and the dewpoint temperature.""")
    return


@app.cell
def _(ds_temporal):
    nyc_coords = {"latitude": 41, "longitude": 286}

    ds_nyc = ds_temporal[['t2', 'd2']].sel(**nyc_coords, method="nearest").load().pint.quantify()
    ds_nyc
    return (ds_nyc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""To calculate this we can use metpy again, but first we need to find the relative humidity.""")
    return


@app.cell
def _():
    from metpy.calc import relative_humidity_from_dewpoint
    from metpy.calc import heat_index
    return heat_index, relative_humidity_from_dewpoint


@app.cell
def _(ds_nyc, relative_humidity_from_dewpoint):
    rel_humid = relative_humidity_from_dewpoint(
        temperature=ds_nyc['t2'],
        dewpoint=ds_nyc['d2'],
    )
    return (rel_humid,)


@app.cell
def _(ds_nyc, heat_index, rel_humid, units):
    heat_ind = heat_index(
        temperature=ds_nyc['t2'],
        relative_humidity=rel_humid,
        mask_undefined=False,
    ).pint.to(units.degF)
    return (heat_ind,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Only the maximum heat index reached on a given day matters for whether or not that day is considered part of a heatwave, so let's calculate the daily maximum heat index over all time.""")
    return


@app.cell
def _(heat_ind):
    heat_ind_daily_max = heat_ind.coarsen(time=24).max()
    heat_ind_daily_max.plot()
    return (heat_ind_daily_max,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""That looks sensible - it has the right magnitude, the right units, and shows an annual cycle.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    NYC Emergency Management issues a "heat advisory" if the heat index is greater than 95°F for two consecutive days.

    There is another xarray-based open-source package called [`xclim`](https://xclim.readthedocs.io/en/stable/index.html) which has a [convenient function](https://xclim.readthedocs.io/en/stable/indices.html#xclim.indices.heat_wave_index) for calculating the number of days in a year that match this criterion.
    """
    )
    return


@app.cell
def _():
    from xclim.indices import heat_wave_index
    return (heat_wave_index,)


@app.cell
def _(heat_ind_daily_max, heat_wave_index):
    heat_wave_index(
        heat_ind_daily_max.pint.dequantify(), 
        thresh='95.0 degF', 
        window=2,
    ).plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Looks like the average number of heatwave days per year in NYC is ~10, and has been increasing noticeably over the last decade or so.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    From [nychazardmitigation.com](https://nychazardmitigation.com/documentation/hazard-profiles/extreme-heat/#probability:~:text=The%202024%20New%20York%20City%20Panel%20on%20Climate%20Change%20(NPCC)%20report%20(NPCC4)%20estimated%20that%20from%201981%20to%202010%2C%20New%20York%20City%20had%20an%20average%20of%2017%20days%20per%20year%20with%20maximum%20temperatures%20at%20or%20above%2090%C2%B0F%20and%20had%20heat%20waves%20lasting%20an%20average%20of%20four%20days):

    > The 2024 New York City Panel on Climate Change (NPCC) report (NPCC4) estimated that from 1981 to 2010, New York City had an average of 17 days per year with maximum temperatures at or above 90°F and had heat waves lasting an average of four days.

    So our quick estimate seems consistent with the official analysis.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Conclusion

    We have:

    - Viewed and accessed a subset of 40TB of ERA5 data in arraylake,
    - Plotted quantities of interest globally and regionally at specific times,
    - Computed quantities of interest locally over the whole time history.

    All of this using open-source packages, accessing Earthmover's public ERA5 Icechunk dataset in the cloud, from your laptop!
    """
    )
    return


if __name__ == "__main__":
    app.run()
