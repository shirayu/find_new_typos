
# Find new typos

Find new typos for [crate-ci/typos](https://github.com/crate-ci/typos)
by using [GitHub Typo Corpus](https://github.com/mhagiwara/github-typo-corpus)

## Preparation

```bash
poetry install --only main
wget https://github-typo-corpus.s3.amazonaws.com/data/github-typo-corpus.v1.0.0.jsonl.gz
```

## How to work

```bash
make clean
poetry run make FILTER_OPTION="--length 5 --freq 5 --distance 2"
```

- ``typos.candidates.gz``: Candidates of typos
- ``new_typos.csv``: New typos
- ``new_words.csv``: New ``typos/crates/typos-dict/assets/words.csv`` for [crate-ci/typos](https://github.com/crate-ci/typos)

Update ``new_typos.csv`` manually and re-run ``make``.

## License

[Apache License Version 2.0](License.txt)
