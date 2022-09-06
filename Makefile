

all: candidate newtypos new

ORIGINAL:=./typos/crates/typos-dict/assets/words.csv
CORPUS:=github-typo-corpus.v1.0.0.jsonl.gz

TYPOS_CANDIDATES:=typos.candidates.gz
candidate :$(TYPOS_CANDIDATES)

$(TYPOS_CANDIDATES): $(ORIGINAL)
	gzip -cd "$(CORPUS)" \
	    | python ./extract.py --original $(ORIGINAL) \
	    | LANG=C sort | LANG=C uniq -c | sort -k1nr | gzip > $(TYPOS_CANDIDATES)

NEW_TYPOS:=new_typos.csv
ENG_WORDS:=./english-words/words.txt
FILTER_OPTION:=
ALLOW_OPTION:=--allow allow.txt

newtypos: $(NEW_TYPOS) $(ENG_WORDS)
$(NEW_TYPOS): $(TYPOS_CANDIDATES)
	gzip -cd $(TYPOS_CANDIDATES) \
		| python ./filter.py \
		--word $(ENG_WORDS) $(FILTER_OPTION) \
		$(ALLOW_OPTION) > $(NEW_TYPOS)

NEW:=new_words.csv
new: $(NEW)
$(NEW): $(NEW_TYPOS) $(ORIGINAL)
	cat $(NEW_TYPOS) $(ORIGINAL) | sort | uniq > $(NEW)

clean:
	rm $(TYPOS_CANDIDATES) $(NEW_TYPOS) $(NEW)
