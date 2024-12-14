import json
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1],sep="\t")  

for model in df['Model'].unique():

  dcmqi_seg_dict = {
    "ContentCreatorName": "MOOSE",
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
