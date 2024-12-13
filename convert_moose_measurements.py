import pydicom as pd
import pandas
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description="Parse two file names from the command line.")

# Add positional arguments for the two file names
parser.add_argument("input_seg", type=str, help="Name of the first input file (segmentation file).")
parser.add_argument("input_measurements", type=str, help="Name of the second input file (measurements file).")

# Parse the command-line arguments
args = parser.parse_args()

# load the dicom file from the input_seg argument
ds = pd.dcmread(args.input_seg, stop_before_pixels=False)

# load csv file from the input_measurements argument
df = pandas.read_csv(args.input_measurements, sep=",")

# iterate over items in SegmentSequence
for item in ds.SegmentSequence:
  print(item.SegmentLabel)

  segment_measurements = df[df["Regions-Present"] == item.SegmentLabel]

  print(f"Measurements for SegmentNumber {item.SegmentNumber} ({item.SegmentLabel}):")
  print(segment_measurements['Volume(mm3)'].values[0])