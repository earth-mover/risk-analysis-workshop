# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "arraylake==0.24.0",
#     "cartopy==0.25.0",
#     "icechunk==1.1.5",
#     "xarray==2025.9.0",
# ]
# ///

import marimo

__generated_with = "0.16.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    import arraylake as al
    import icechunk as ic
    import xarray as xr
    return al, mo, xr


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
    ds = xr.open_dataset(session.store, group="spatial", engine="zarr", zarr_format=3)
    ds
    return (ds,)


@app.cell
def _(ds):
    print(f"This repo contains {ds.nbytes / 1e12:.2g} TB of data!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Total Cloud Cover""")
    return


@app.cell
def _(ds):
    ds["tcc"].attrs
    return


@app.cell
def _():
    import cartopy.crs as ccrs
    return (ccrs,)


@app.cell
def _(ccrs, ds):
    p = (
        ds["tcc"]
        .isel(time=-1)
        .plot(
            subplot_kws={"projection": ccrs.Orthographic(173, -42), "facecolor": "gray"},
            transform=ccrs.PlateCarree(),
        )
    )
    p.axes.set_global()
    p.axes.coastlines()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
