

# Slices
RULE:
1. Slices will be sideways, each slice gets a column in the final table


## Example 1
> slices in one element
- Condition.code:sct
- Condition.code:loinc
- Condition.code:icd-10
- Condition.code:alpha-id

### View instruction - concept file:
```json
{
  "url": "https://www.medizininformatik-initiative.de/fhir/core/modul-diagnose/StructureDefinition/Diagnose",
  "elements": [
    {
      "elementId": "Condition.code",
      "columns": [
        {
          "path": "Condition.code.coding.where(system='http://fhir.de/CodeSystem/bfarm/icd-10-gm').code",
          "name": "codeIcd10"
        },
        {
          "path": "Condition.code.coding.where(system='http://fhir.de/CodeSystem/bfarm/alpha-id').code",
          "name": "codeAlphaId"
        },
        {
          "path": "Condition.code.coding.where(system='http://sct.info').code",
          "name": "codesnomedCt"
        },
        {
          "path": "Condition.code.coding.where(system='http://orphanet').code",
          "name": "codeoprhanet"
        }
      ]
    }
  ]
}
```

### Example Output
| getResourceKey()                        | obs_code_sct | obs_code_loinc | obs_code_icd-10 | obs_code_aplha-id |
|-----------------------------------------|--------------|----------------|-----------------|-------------------|
| mii-exa-test-data-patient-1-diagnose-1  | 13420004     | I29578         | B05.3           | I29578            |


# Example 2
> slices in two different elements

- Condition.code:sct
- Condition.code:alpha-id
- Condition.bodySite:sct
- Condition.bodySite:icd-o-3

```json
{
  "url": "https://www.medizininformatik-initiative.de/fhir/core/modul-diagnose/StructureDefinition/Diagnose",
  "elements": [
    {
      "elementId": "Condition.code",
      "columns": [
        {
          "path": "Condition.code.coding.where(system='http://fhir.de/CodeSystem/bfarm/alpha-id').code",
          "name": "code_alpha-id"
        },
        {
          "path": "Condition.code.coding.where(system='http://snomed.info/sct').code",
          "name": "code_sct"
        }
      ]
    },
    {
      "elementId": "Condition.bodySite",
      "columns": [
        {
          "path": "Condition.code.coding.where(system='http://terminology.hl7.org/CodeSystem/icd-o-3').code",
          "name": "bodySite_icd_o_3"
        },
        {
          "path": "Condition.code.coding.where(system='http://snomed.info/sct').code",
          "name": "code_sct"
        }
      ]
    }
  ]
}
```

| getResourceKey()                        | code_sct | code_alpha_id | bodySite_sct | bodySite_icd_o_3 |
|-----------------------------------------|----------|---------------|--------------|------------------|
| mii-exa-test-data-patient-1-diagnose-1  | I29578   | 13420004      | 25342003     | C21.8            |
