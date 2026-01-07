# Procedure
## Start FHIR Server
```sh
docker run ghcr.io/medizininformatik-initiative/fhir-flattener:0.1.0-alpha.4
```

## Request Flattening
```sh
./request-flattening.sh <path/to/viewdef.json> <path/to/resource.json>
```

* Example: `./request-flattening.sh condition-slice/viewDefinition-3.json condition-slice/condition-duplicateSystem.json`
* More Examples are further down

# Purpose
The ``flatteningInstructions`` file represents a lookup table with instructions on how to flatten an element of a profile given the element id.
    This file will be used by the fhir-flattener to create csv file 

# The conceptFile format:
At root level ``url`` and ``elements`` should be present, similar to the viewDefinition format
- ``url``: url of the profile which this conceptFile corresponds to 
- ``elements``: a dictionary holding flatteningInstructions for each element of the Profile
  - Each element contains either ``children`` or ``viewDefintion``:
    - ``viewDefinition``: viewDefinition snippet to use for the element with this id
    - ``children``: array of child element ids. This is used to also support selection of parent nodes in dse selection. 
      Using this approach reduces complexity and file size by avoiding including the parent subtree each time, as the information is stored in the leafs of the tree anyway.

Colum Names: 
- ``name`` of each element in the viewDefinition snippet is created by replacing the `.` with a `_` and a `:` with `#` and prefixed with the profile url / name to make it unique

Example:
```json
{
    "url": "https://www.medizininformatik-initiative.de/fhir/core/modul-diagnose/StructureDefinition/Diagnose",
    "elements": {
        "Condition.stage": {
            "viewDefinition": [],
            "children": ["Condition.stage.summary", "Condition.stage.type"]
        },
        "Condition.stage.summary": {
            "viewDefinition": [
                {
                    "forEach": "stage.summary.coding",
                    "column": [
                        {
                            "name": "summary_system",
                            "path": "system"
                        },
                        {
                            "name": "summary_code",
                            "path": "code"
                        }
                    ]
                }
            ],
          "children": []
        }
    }
}
```

# Rules - Structures:
### Slices:
- Slices are always defined ... ???
- Each defined slice gets a column
  - Slices can be defined by ``fixed`` `pattern` and `bindings`. See ``coding`` for further detail.
- Instances of slices which are not mentioned in the Profile should be ignored
  - Special case: If code and system are defined by a pattern, meaning the expectation is exactly this code-system combination
- If no slice is defined in the profile => create columns ``el-code, el-system``
- (see Coding)

### Backbone:
- For each child of a backbone:
  - if a primitive (a leaf with a value): create a column
  - if still complex: create entry in ```ref```
- Cardinality MANY: create a row for each instance

### Cardinality
- The Profile defines the cardinality for each element with min/max.
  - if el.max == * : for each instance create a row
  - if el.max == 1 : NO NEED FOR FOREACH???
- Keep in mind that elements can have children, each with cardinality MANY. This should be handled by implementation

### Extensions 
- Extensions contain a `url` and ``value``. The ``url`` should be used to create the column name. 
- Extensions should be flattened according to the type of the ``value`` element
- Extensions containing extensions should be flattened to the side. Create a column for each level.

### Polymorphic elements
- Polymorphic elements should be rendered as the specified type defines
- If multiple types are allowed, render all defined. In most cases only one of the defined types is allowed
- If no type is defined, ERROR, this cant be????
  - Beispiel: Observation.value[x]:
    - StructureDefinition: valueQuantity, -CodeableConcept,-Range,- Ratio
      - 4 Spalte

# Rules - 'Datatypes'

### Codeable concept: => coding
````shell
bash ./request-flattening.sh datatypes/CodeableConcept/obs-view.json datatypes/CodeableConcept/Observation_simple.json
````
### Coding: code + system

| el_id_system_1 | el_id_system_2 | ... |
|----------------|----------------|-----|
| code_sys_1     | code_sys_2     | ... |

- For each defined system create a column.
  - If no codesystem is defined than 2 columns ``el-code, el-system`` should be created
- Where to look for code system restrictions:
  - Binding
  - fixed
  - pattern
  - also note that the cardinality of the coding does matter ??
- In the rare case that an instance contains codings with the same codesystem, see the example in ``/condition-slice``
- If no slice is defined create 2 columns ```el-code,el-code``` and fill in if any code+system exists in the instance data

### Reference:

| el_id_reference |
|-----------------|
| ref_string      |
simple string => create column

### Quantity:  code(unit) + value + system | SimpleQuantity

| el_id_quantity_code  | el_id_quantity_value | el_id_quantity_system       | el_id_quantity_comparator |
|----------------------|----------------------|-----------------------------|---------------------------|
| "mm[Hg]"             | 20                   | http://unitsofmeasure.org   | <                         |

> TODO: Debate if comparators are needed. They might be present, tough I could not find them in test-data.zip

````shell
bash ./request-flattening.sh datatypes/Quantity/obs-view.json datatypes/Quantity/Observation.json
````

### Range: low + high
low and high are quantities. create a ```ref``` 

| el_id_range_low_code | el_id_range_low_value | el_id_range_low_system     | el_id_range_high_code | el_id_range_high_value | el_id_range_high_system    |
|----------------------|-----------------------|----------------------------|-----------------------|------------------------|----------------------------|
| {Exon}               | 15                    | http://unitsofmeasure.org  | {Exon}                | 15                     | http://unitsofmeasure.org  |

````shell
bash ./request-flattening.sh datatypes/Range/obs-view.json datatypes/Range/Observation.json
````
### Ratio: numerator + denominator
numerator + denominator are both quantities. create ```refs``` to numerator and denominator
example basically the same as Range

### Period: start + end
start and end are of type: dateTime



# More Example: 

### Slices

Slices defined with different systems
```bash
bash ./request-flattening.sh condition-slice/viewDefinition-2.json condition-slice/condition-unique-systems.json
```
Slices defined with one pattern + extensible binding: example: ``Observation.category.coding`` in ``mikrobio empfindlichkeit``
```bash
bash ./request-flattening.sh condition-slice/viewDefinition-3.json condition-slice/condition-duplicateSystem.json
```
Slice duplicate system, example: ``Observation.code`` in ``mikrobio kulturnachweis`` ???
```bash
bash ./request-flattening.sh condition-slice/viewDefinition-1.json condition-slice/condition-duplicateSystem.json
```

### Backbone
#### - backbone child + unknown slice-systems
Simple children of backbone -> column TODO: multiple 
- example: "Condition.stage.summary" in ``Diagnose``
- making ``system,code`` - pairs because no slice systems defined
```bash
bash ./request-flattening.sh backbone-child/viewDefinition.json backbone-child/condition.json
```
#### - Backbone element
Children in columns, all possible combinations down
- does cross Produkt: 3x3 = 9. Combinations even with not children  
```bash
bash ./request-flattening.sh backbone-parent/viewDefinition.json backbone-parent/condition.json
```
```bash
bash ./request-flattening.sh backbone-parent/testRepeatField-viewDefinition.json backbone-parent/condition.json
```
```bash
bash ./request-flattening.sh backbone-parent/testSelectField-viewDefinition.json backbone-parent/condition.json
```
```bash
bash ./request-flattening.sh backbone-parent/viewDefinition2.json backbone-parent/condition.json
```
broken
```bash
bash ./request-flattening.sh backbone-cardinality-many/viewDefinition.json backbone-cardinality-many/specimen.json
```

### Polymorphic elements:
```bash
bash ./request-flattening.sh polymorphic/viewDefinition.json polymorphic/observation.json
```



```bash
bash ./request-flattening.sh test/cond-view.json test/Condition.json
```


