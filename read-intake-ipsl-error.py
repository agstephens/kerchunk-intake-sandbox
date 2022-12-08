import matplotlib.pyplot as plt

import intake
import intake_esm

uri = "intake-catalogs/ceda-cmip6-files.json"
cat = intake.open_esm_datastore(uri)

cat_subset = cat.search(
    experiment_id=["historical", "ssp585"],
    table_id="Oyr",
    variable_id="o2",
    grid_label="gn",
)

dset_dict = cat_subset.to_dataset_dict(
    xarray_open_kwargs={"decode_times": False, "use_cftime": True}
)

time_mean = lambda da: da.isel(olevel=0).mean(dim=["time"], keep_attrs=True).squeeze()


ds1 = dset_dict["CMIP6.CMIP.IPSL.IPSL-CM6A-LR.historical.r1i1p1f1.Oyr.o2.gn.latest"]
ds2 = dset_dict["CMIP6.ScenarioMIP.IPSL.IPSL-CM6A-LR.ssp585.r1i1p1f1.Oyr.o2.gn.latest"]
print(ds1)
#ds1 = dset_dict["CMIP6.CMIP.NCC.NorESM2-LM.historical.r1i1p1f1.Oyr.o2.gn.latest"]
#ds2 = dset_dict["CMIP6.ScenarioMIP.NCC.NorESM2-LM.ssp585.r1i1p1f1.Oyr.o2.gn.latest"]

print(f"Shapes: {ds1.o2.shape}, {ds2.o2.shape}")

diff = time_mean(ds2.o2) - time_mean(ds1.o2)
print(f"[INFO] Max of diff: {float(diff.max())}")

diff.plot()
plt.show()

fig = "output.png"
plt.savefig(fig)

print(f"[INFO] Saved to {fig}")

