import argparse
import os

# Force Java 21 so Spark/Hadoop do not crash
os.environ["JAVA_HOME"] = "/home/leo/.sdkman/candidates/java/21.0.5-tem"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]

print("Using Java:")
print(os.popen("java -version 2>&1").read())

from pathling import PathlingContext
import json



def configure_args_parser():
    arg_parser = argparse.ArgumentParser(description="Generate Translations for fdpg terms")
    arg_parser.add_argument("--ex", type=str, help="The name of the folder containing the example")
    arg_parser.add_argument("--view", type=str,help="The viewDefinition to be executed. If none provided, all views are executed")
    return arg_parser


def get_view_def(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_view_def(view_def_name):

    view_def = get_view_def(view_def_name)

    view_def_resource = view_def["resource"]["resource"]
    view_def_select = view_def["resource"]["select"]

    result = data.view(
        resource=view_def_resource,
        select=view_def_select,
    )

    result.show(truncate=False)


if __name__ == '__main__':
    args = configure_args_parser().parse_args()
    pc = PathlingContext.create()
    args.ex = "condition-slice"
    print(args.ex)
    data = pc.read.ndjson(os.path.join(args.ex, "input"))
    print(data)
    if args.view is None:
        for view_def_file in os.scandir(os.path.join(args.ex,"views")):
            print(f"view: {view_def_file}")
            run_view_def(view_def_file)
    else:
        run_view_def(os.path.join(args.ex,"views",args.view))