import json
import os
from typing import Dict, Any

import requests

if __name__ == '__main__':
    INPUT_FOLDER = "Examples"
    PORT = 7812
    for folder in os.scandir(INPUT_FOLDER):

        print(f"Executing: {folder.name}")

        with open(os.path.join(folder, "resources.json"), 'r', encoding="UTF-8") as f:
            resources = json.load(f)

        with open(os.path.join(folder, "viewDefinition.json"), 'r', encoding="UTF-8") as f:
            view = json.load(f)

        request: Dict[str, Any] = {
            "resourceType": "Parameters",
            "parameter": []
        }

        request["parameter"].append(view)
        # for res in resources:
        #     request["parameter"].append(res)
        request["parameter"].append(resources)

        print(json.dumps(request))

        res = None

        try:
            res = requests.post(
                url=f"http://localhost:{PORT}/fhir/ViewDefinition/$run",
                json=request,
                timeout=10,
                headers={
                    "Accept": "text/csv",
                    "Content-Type": "application/json"
                }

            )
        except Exception as e:
            print(res.status_code)
            print(res.reason)

        print(res.text)