# About

This is home for WIP code for converting segmentations from NIFTI to DICOM Segmentation 
and segmentation-derived measurements from CSV to DICOM Structured Reports TID1500, for the 
outputs generated using https://github.com/ENHANCE-PET/MOOSE.


# Usage

## Prerequisites

This code assumes the results produced by MOOSE are organized along with the CT series following the organization below:

```
── NLST-MOOSE
    ├── 100002
    │   ├── 1.2.840.113654.2.55.187766322555605983451267194286230980878
    │   │   ├── CT_1.2.840.113654.2.55.107058971791399096468046631579934786083
    │   │   ├── CT_1.2.840.113654.2.55.122344168497038128022524906545138736420
    │   │   ├── CT_1.2.840.113654.2.55.97114726565566537928831413367474015470
    │   │   ├── Nifti
    │   │   │   ├── CT_1.2.840.113654.2.55.122344168497038128022524906545138736420
    │   │   │   │   └── moosez-2024-12-08-16-11-08
    │   │   │   │       ├── segmentations
    │   │   │   │       └── stats
    │   │   │   └── CT_1.2.840.113654.2.55.97114726565566537928831413367474015470
    │   │   │       └── moosez-2024-12-08-16-11-51
    │   │   │           ├── segmentations
    │   │   │           └── stats
```

where segmentation files and stats look like this:

```
    │   │       ├── segmentations
    │   │       │   ├── clin_CT_muscles_segmentation_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875.nii.gz
    │   │       │   ├── clin_CT_organs_segmentation_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875.nii.gz
    │   │       │   ├── clin_CT_peripheral_bones_segmentation_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875.nii.gz
    │   │       │   ├── clin_CT_ribs_segmentation_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875.nii.gz
    │   │       │   ├── clin_CT_vertebrae_segmentation_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875.nii.gz
```

and

```
    │   │       └── stats
    │   │           ├── clin_CT_muscles_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875_ct_volume.csv
    │   │           ├── clin_CT_organs_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875_ct_volume.csv
    │   │           ├── clin_CT_peripheral_bones_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875_ct_volume.csv
    │   │           ├── clin_CT_ribs_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875_ct_volume.csv
    │   │           └── clin_CT_vertebrae_CT_1.2.840.113654.2.55.283399418711252976131557177419186072875_ct_volume.csv
```

## Usage

1. Install the latest release of dcmqi for your platform from here: https://github.com/QIICR/dcmqi/releases
2. Make sure the executables are in the system path.
3. run `python make_moose_dcmqi_jsons.py` to create JSON files that will be used in the following step.
4. run `convert_moose_segmentations.py <path to the root folder with the MOOSE results as above>` 

WARNING: this is WIP and 

MOOSE SNOOMED mapping source is in https://docs.google.com/spreadsheets/d/1Yi_HL8UTNDqRZ4kdZ9XEAVRiG2ijbNK0kL8HvCUe9kI/edit?gid=657933107#gid=657933107.

# Support

@fedorov
