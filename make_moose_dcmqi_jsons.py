import json
import pandas as pd
import re
import sys

df = pd.read_csv(sys.argv[1])  

print(df.columns)

algorithm = sys.argv[2]

try:
  models = df['Model'].unique()
except KeyError:
  models = ['UNKNOWN']

for model in models:

  dcmqi_seg_dict = {
    "ContentCreatorName": algorithm,
    "ClinicalTrialSeriesID": "Session1",
    "ClinicalTrialTimePointID": "1",
    "ClinicalTrialCoordinatingCenterName": algorithm,
    "SeriesDescription": f"{algorithm} segmentation - {model}",
    "SeriesNumber": "300",
    "InstanceNumber": "1",
    "segmentAttributes": []}

  dcmqi_seg_dict["segmentAttributes"].append([])

  # iterate over rows in df
  for index, row in df.iterrows():
    if model != 'UNKNOWN':
      if row["Model"] != model:
        continue

    try:
      rgb=[int(num) for num in re.findall(r'\d+', row['recommendedDisplayRGBValue'])]
    except TypeError:
      print("Failed to parse RGB value for row: ", row)

    segment_attributes = {
      "labelID": row['label_id'],
      "SegmentDescription": row['label_name'],
      "SegmentAlgorithmType": 'AUTOMATIC',
      "SegmentAlgorithmName": algorithm,
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
            rgb[0],
            rgb[1],
            rgb[2]
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
  with open(f'{algorithm}-{model}-dcmqi_seg_dict.json', 'w') as outfile:
    json.dump(dcmqi_seg_dict, outfile, indent=2)
