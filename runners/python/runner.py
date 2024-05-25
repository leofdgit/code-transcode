import json
import sys
import traceback


def run_function_with_args(json_args):
    try:
        args = json.loads(json_args)

        if not isinstance(args, list):
            raise ValueError("Arguments must be an array.")

        result = main(*args)
        print(json.dumps(result))
        sys.exit(0)
    except Exception as e:
        print(json.dumps("\n".join(traceback.format_exception(e))), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_args = sys.argv[1]
        run_function_with_args(json_args)
    else:
        print("No arguments provided", file=sys.stderr)
        sys.exit(1)
