#!/usr/bin/env python3

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Optional

from inflector import Inflector
from rapidfuzz.distance import Levenshtein

ALLOW_SET = {
    "zplugin",
    "manged",
    "connexions",
    "thead",
}


def exclude(old, new) -> bool:
    if Inflector().pluralize(new) == old:
        return True
    elif Inflector().singularize(new) == old:
        return True
    return False


def operation(
    path_in: Path,
    path_out: Path,
    path_word: Optional[Path],
    distance: int,
    freq: int,
    length: int,
) -> None:
    words = set()
    if path_word:
        with path_word.open() as wf:
            for line in wf:
                words.add(line.strip().lower())

    old2new = defaultdict(set)

    with path_in.open() as inf, path_out.open("w") as outf:
        for line in inf:
            items = line.strip().split()
            _freq = int(items[0])
            pair = items[-1].split(",")

            if _freq < freq:
                continue
            if len(pair[0]) < length or pair[0] in words:
                continue
            if exclude(pair[0], pair[1]):
                continue
            if pair[0] in ALLOW_SET:
                continue

            err_char: bool = False
            for c in pair[0]:
                if not (ord("a") <= ord(c) <= ord("z")):
                    err_char = True
                    break
            if err_char:
                continue

            _dist: int = Levenshtein.distance(pair[0], pair[1])
            if _dist <= distance:
                old2new[pair[0]].add(pair[1])

        for _s, _ts in sorted(old2new.items()):
            for _t in _ts:
                assert _t not in old2new
            _t = ",".join(sorted(list(_ts)))
            outf.write(f"{_s},{_t}\n")


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument(
        "--input", "-i", type=Path, default="/dev/stdin", required=False
    )
    oparser.add_argument(
        "--output", "-o", type=Path, default="/dev/stdout", required=False
    )
    oparser.add_argument(
        "--distance",
        type=int,
        default=2,
    )
    oparser.add_argument(
        "--freq",
        type=int,
        default=5,
    )
    oparser.add_argument(
        "--length",
        type=int,
        default=5,
    )
    oparser.add_argument("--word", "-w", type=Path, required=True)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(
        opts.input,
        opts.output,
        opts.word,
        opts.distance,
        opts.freq,
        opts.length,
    )


if __name__ == "__main__":
    main()
