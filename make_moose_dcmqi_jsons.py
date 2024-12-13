import pydcmqi
import json
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('MOOSE SNOMED mapping - MOOSE SNOMED MAPPING.tsv',sep="\t")  

# Display the first few rows of the DataFrame
print(df.head())

for model in df['Model'].unique():

  dcmqi_seg_dict = {
    "ContentCreatorName": "MOSE",
    "ClinicalTrialSeriesID": "Session1",
    "ClinicalTrialTimePointID": "1",
    "ClinicalTrialCoordinatingCenterName": "MOOSE",
    "SeriesDescription": f"MOOSE segmentation - {model}",
    "SeriesNumber": "300",
    "InstanceNumber": "1",
    "segmentAttributes": []}

  dcmqi_seg_dict["segmentAttributes"].append([])

  # iterate over rows in df
  for index, row in df.iterrows():
    if row["Model"] != model:
      continue

    segment_attributes = {
      "labelID": row['label_id'],
      "SegmentDescription": row['label_name'],
      "SegmentAlgorithmType": 'AUTOMATIC',
      "SegmentAlgorithmName": 'MOOSE',
      "SegmentedPropertyCategoryCodeSequence": {
        "CodeValue": str(int(row['SegmentedPropertyCategoryCodeSequence.CodeValue'])),
        "CodingSchemeDesignator": row['SegmentedPropertyCategoryCodeSequence.CodingSchemeDesignator'],
        "CodeMeaning": row['SegmentedPropertyCategoryCodeSequence.CodeMeaning'],
      },
      "SegmentedPropertyTypeCodeSequence": {
        "CodeValue": str(int(row['SegmentedPropertyTypeCodeSequence.CodeValue'])),
        "CodingSchemeDesignator": row['SegmentedPropertyTypeCodeSequence.CodingSchemeDesignator'],
        "CodeMeaning": row['SegmentedPropertyTypeCodeSequence.CodeMeaning'],
      },
      "TrackingIdentifier": row['label_name'],
      "recommendedDisplayRGBValue": [
            221,
            130,
            101
          ],
    }

    if not pd.isna(row['SegmentedPropertyTypeModifierCodeSequence.CodeValue']):
      segment_attributes["SegmentedPropertyTypeModifierCodeSequence"] = {
        "CodeValue": str(int(row['SegmentedPropertyTypeModifierCodeSequence.CodeValue'])),
        "CodingSchemeDesignator": row['SegmentedPropertyTypeModifierCodeSequence.CodingSchemeDesignator'],
        "CodeMeaning": row['SegmentedPropertyTypeModifierCodeSequence.CodeMeaning'],
      }

    dcmqi_seg_dict["segmentAttributes"][0].append(segment_attributes)
    
  # save dcmqi_seg_dict to json file
  with open(f'{model}-dcmqi_seg_dict.json', 'w') as outfile:
    json.dump(dcmqi_seg_dict, outfile, indent=2)