# iterate recursively over the directory and check if the file has nii extension and "segmentation" in the name

# Import the necessary libraries
import os
import re
import pandas
import pydicom

dcmqi_measurements_json = {
  "SeriesDescription": "MOOSE segmentations measurements",
  "SeriesNumber": "1001",
  "InstanceNumber": "1",

  "observerContext": {
    "ObserverType": "DEVICE",
  },

  "VerificationFlag": "VERIFIED",
  "CompletionFlag": "COMPLETE",

  "activitySession": "1",
  "timePoint": "1",

  "Measurements": []
}

# conversion function
def convert_moose_segmentations(results_directory, force_overwrite=False):
    # Iterate recursively over the directory
    for root, dirs, files in os.walk(results_directory):
        for file in files:
            if file.endswith(".nii.gz") and "segmentation" in file:
                print(f"Processing {file}")
                # extract model name from the file name string given that
                # it is contained between "CT_" and "_CT" in that string
                model_name = re.search('CT_(.*)_segmentation_CT', file).group(1)
                print(f"Model name: {model_name}")
                path_components = root.split(os.path.sep)
                patient_id = path_components[-6]
                study_instance_uid = path_components[-5]
                print(f"ct folder: " +path_components[-3])
                ct_series_instance_uid = path_components[-3].split('_')[1]
                ct_folder_path = os.path.join(results_directory, patient_id, study_instance_uid, f"CT_{ct_series_instance_uid}")

                # check that ct_folder_path exists and is not empty
                if os.path.exists(ct_folder_path) and os.listdir(ct_folder_path):
                    print(f"CT folder path: {ct_folder_path}")
                else:
                    print(f"CT folder path does not exist or is empty: {ct_folder_path}")

                dcmq_model_json = os.path.join(f"{model_name}-dcmqi_seg_dict.json")                                    
                # confirm that the dcmqi model json file exists
                if os.path.exists(dcmq_model_json):
                    print(f"dcmqi model json file exists: {dcmq_model_json}")
                else:
                    print(f"dcmqi model json file does not exist: {dcmq_model_json}")

                dcm_seg_filename = os.path.join(root, f"{model_name}_segmentation.dcm")
                if os.path.exists(dcm_seg_filename) and not force_overwrite:
                    print(f"DCM segmentation file already exists: {dcm_seg_filename}")
                else:
                    # build conversion command line
                    input_seg_nifti = os.path.join(root, file)
                    cmd = f"itkimage2segimage --inputDICOMDirectory {ct_folder_path}    --inputImageList {input_seg_nifti} --outputDICOM {dcm_seg_filename}    --inputMetadata {dcmq_model_json}"

                    # execute the conversion command
                    print(f"Executing command: {cmd}")
                    os.system(cmd)

                    # check that the output dcm segmentation file exists
                    if os.path.exists(dcm_seg_filename):
                        print(f"DCM segmentation file created: {dcm_seg_filename}")
                    else:
                        print(f"DCM segmentation file not created: {dcm_seg_filename}")

                continue

                # Measurements WIP

                # check if measurements exist
                measurements_dir = os.path.join(path_components[:-1], "stats")
                measurements_file = os.path.join(measurements_dir, f"clin_CT_{model_name}_CT_{ct_series_instance_uid}_ct_volume.csv")

                if not os.path.exists(measurements_file):
                    continue                    
                
                print(f"Measurements file exists: {os.path.join(measurements_dir, measurements_file)}")
                measurements_sr_file = os.path.join(measurements_dir, f"{model_name}_volume_sr.dcm")
                if os.path.exists(measurements_sr_file) and not force_overwrite:
                    print(f"Measurements SR file already exists: {measurements_sr_file}")
                else:
                    # load csv file from the input_measurements argument
                    df = pandas.read_csv(measurements_file, sep=",")
                    seg_ds = pydicom.dcmread(dcm_seg_filename, stop_before_pixels=False)

                                        # iterate over items in SegmentSequence
                    for item in seg_ds.SegmentSequence:
                        segment_measurements = df[df["Regions-Present"] == item.SegmentLabel]
                        if segment_measurements.empty:
                            continue
                        these_measurements = dcmqi_measurements_json.deepcopy()
                        # TODO: populate these from segmentation category sequence
                        these_measurements["Finding"] = {
                            "CodeValue": "123037004",
                            "CodingSchemeDesignator": "SCT",
                            "CodeMeaning": "Anatomical structure"
                        }
                        these_measurements["Finding site"] = {
                            "CodeValue": item.SegmentationTypeCodeSequence[0].CodeValue,
                            "CodingSchemeDesignator": item.segmentationTypeCodeSequence[0].CodingSchemeDesignator,
                            "CodeMeaning": item.segmentationTypeCodeSequence[0].CodeMeaning
                        }
                        # TODO: handle modifier code sequence
                        measurement_item = {}
                        print(item.SegmentLabel)

                    

                    print(f"Measurements for SegmentNumber {item.SegmentNumber} ({item.SegmentLabel}):")
                    print(segment_measurements['Volume(mm3)'].values[0])


# in the __main__ function, parse the parameter which is the directory name
# and call convert_moose_segmentations function with the directory name as the argument

if __name__ == "__main__":
    import argparse

    # confirm that itkimage2segimage executable is in the system path
    import subprocess
    try:
        subprocess.run(["itkimage2segimage", "--help"], check=True)
    except FileNotFoundError:
        print("itkimage2segimage executable not found in system path.")
        exit(1)

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Parse a directory name from the command line.")

    # Add positional arguments for the directory name
    parser.add_argument("directory", type=str, help="Name of the input directory.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the convert_moose_segmentations function with the directory name as the argument
    convert_moose_segmentations(args.directory)