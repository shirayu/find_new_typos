#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import List, Set


def find_typos(
    d,
    ng_words: Set[str],
    ok_words: Set[str],
):
    for tp in d["edits"]:
        if not tp.get("is_typo"):
            continue
        if tp["src"].get("lang") != "eng":
            continue
        if tp["tgt"].get("lang") != "eng":
            continue

        src: List[str] = tp["src"]["text"].split()
        tgt: List[str] = tp["tgt"]["text"].split()
        if len(src) != len(tgt):
            continue

        for _s, _t in zip(src, tgt):
            _s, _t = _s.lower(), _t.lower()
            if "," in _s or "," in _t:
                continue
            if _s in ok_words or _s in ng_words:
                continue
            if _t not in ok_words:
                continue
            if _s != _t:
                yield f"{_s},{_t}"


def operation(path_in: Path, path_out: Path, path_original: Path) -> None:
    ng_words = set()
    ok_words = set()
    with path_original.open() as orgf:
        for line in orgf:
            items = line.strip().split(",")
            ng_words.add(items[0])
            ok_words.add(items[1])

    with path_in.open() as inf, path_out.open("w") as outf:
        for line in inf:
            d = json.loads(line)
            for tp in find_typos(d, ng_words, ok_words):
                outf.write(f"{tp}\n")


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument(
        "--input", "-i", type=Path, default="/dev/stdin", required=False
    )
    oparser.add_argument(
        "--output", "-o", type=Path, default="/dev/stdout", required=False
    )
    oparser.add_argument("--original", type=Path, required=True)

    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    operation(opts.input, opts.output, opts.original)


if __name__ == "__main__":
    main()
