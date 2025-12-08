### Tests




## Backbone Cardinality and Cardinality in general

1. Backbones having multiple instances meaning a cardinality of 0..* like for example ``Specimen.container``will each get a separate row
   - this is achieved by adding ```"foreach":"container"```
2. 






Was Tester sehen will:
- datatype (z.B. resource mit 2 backbone elements)
- output csv (z.B. tabelle mit 2 spalten, weil 2 backbone elements)

Einzelner Test:
- pro fhir type
- input:
    - resource.json
    - viewdev.json
- durchführung:
    - resource und viewdev werden in parameter gemerged
    - parameter wird in curl requeset gemerted
    - curl wird abgesendet
- outpt: 
    - eine enizelne csv

- Pro Bundle (1 Zeile in ndjson) eine einzige tabelle
- in viewdev: 1 param pro res und 1 param pro res-viewDef
    -> z.B. 2 observation resources aber nur eine viewDef für resourceType observation
- eine resource auf mehrere Zeilen aufzuteilen ist kein problem solange res.id immer dabei ist

### Rules:
- slices: sideways -> columns
- backbone elements: downwards -> rows
    - für jede definition (Kind) eine spalte
    - für jede vorkommende Kombination eine Zeile
- cardinality * (potentially nested):
    - example: category
    - rule: downwards
- Bindings:
    - like cardinality -> downwards
    - if slices exist inside binding, those slices will be handled like slices -> sideways
- extensions:
    - extensions sideways je nach typ (muss von uns ermittelt werden)
    - Beispiel: backbone in extension: children sidewys, instance combinations downwards 
- polymorphic stuff:
    - sideways nach allen definierten typen, bzw wenn nicht eingeschränkt sideways nach allen FHIR typen
    - Beispiel: Observation.value[x]:
                    - StructureDefinition: valueQuantity, -CodeableConcept,-Range,- Ratio
                    -> 4 Spalten
- alles andere
    - wie backbone betrachten -> kinder sideways, instances down
    - Beispiel: 1 resource hat in 1 feld 2 ranges: Spalten: min, max, Zeilen: jeweils ausgefüllt nach Ausprägung der beiden range elements

- Umsetzung in view definition:
    - kardnialität 1..* --> instances down --> "forEach"
    - kardnialität 0..1 --> kein "forEach"
    - spalten je nach children und slices

- A is signle string
- B is backbone of B_c, B_s
- C is slice of C:X, C:Y
res 1: extension: A1, [{B_c1, B_s1}, {B_c2, B_s1}], C:X
res 2: extension: A2

==> 
id, A, B_c, B_s, C:X, CY
1, A1, B_c1, B_s1 -, -
1, A1, B_c2, B_s1 -, -
2, A2, -, -, -
==> we must know the possbile extensions for the resourceType to be able to define a column for each

extension B of type backbone:
res 1: extension: A1, [{B_c1, B_s1}, {B_c2, B_s1}], CX, -
res 2: extension: A2, [{B_c2, B_s1}], -, -
res 3: extension: A2, -, CX, CY
==> 
id, A, B, C
1, A1, B_c1, B_s1, CX, -
1, A1, B_c2, B_s1, CX, -
2, A2, B_c2, B_s1, -, -
3, A2, -, - , CX, CY
