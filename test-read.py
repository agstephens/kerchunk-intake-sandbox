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

ds2 = dset_dict["CMIP6.ScenarioMIP.IPSL.IPSL-CM6A-LR.ssp585.r1i1p1f1.Oyr.o2.gn.latest"]

float(ds2.o2[:,0,0,0])

