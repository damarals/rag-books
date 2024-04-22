import argparse
import json
import timeit
from typing import get_args

from rag.pipeline import get_rag_response
from rag.types import ModeType

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "topic", type=str, help="The topic of the module to be generated."
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="chapter",
        choices=get_args(ModeType),
        help="The mode to be used for the pipeline.",
    )
    args = parser.parse_args()

    start = timeit.default_timer()
    answer = get_rag_response(args.topic, args.mode)
    end = timeit.default_timer()

    print(f"\nAnswer:\n{json.dumps(answer['result'], indent=4)}")
    print("=" * 50)
    print(f"Sources consulted ({len(answer['source_documents'])}):")
    for source in answer["source_documents"]:
        print(source.metadata["id"])
    print("=" * 50)

    print(f"Time to answer: {round(end - start, 2)} seconds")
