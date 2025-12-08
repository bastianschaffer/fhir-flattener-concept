#!/bin/bash
VIEW_DEF_FILE="$1"
RESOURCE_FILE="$2"


parameter() {
cat <<EOF
    {
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "viewDefinition",
            "resource": $1
        },
        {
            "name": "resources",
            "resource": $2
        }
    ]
}
EOF
}


resource="$(cat $RESOURCE_FILE)"
view_def="$(cat $VIEW_DEF_FILE)"
filledParam=$(parameter "$view_def" "$resource")
curl -X POST --location "http://localhost:8000/fhir/ViewDefinition/\$run" \
    -H "Content-Type: application/fhir+json" \
    -H "Accept: text/csv" \
    --data-binary "$filledParam"

