import intake
import intake_esm

uri = "dkrz_cmip6_disk.json"
import pandas as pd
df = pd.read_csv(uri.replace("json", "csv.gz"))
print(len(df))
sdf
print("Open")
cat = intake.open_esm_datastore(uri)

print("Subset")
cat_subset = cat.search(
    experiment_id=["historical", "ssp585"],
    table_id="Oyr",
    variable_id="o2",
    grid_label="gn",
)

print("Create dict")
dset_dict = cat_subset.to_dataset_dict(
    xarray_open_kwargs={"decode_times": False, "use_cftime": True}
)
