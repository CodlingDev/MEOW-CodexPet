PYTHON ?= python3
CODEX_HOME ?= $(HOME)/.codex
HATCH_PET_SCRIPTS := $(CODEX_HOME)/skills/hatch-pet/scripts
FRAMES_DIR := .hatch/meow-original/frames

.PHONY: build qa

build:
	$(PYTHON) scripts/build_pet_atlas.py

qa: build
	$(PYTHON) $(HATCH_PET_SCRIPTS)/validate_atlas.py \
		pets/meow/spritesheet.webp \
		--json-out qa/meow/validation-extended.json \
		--chroma-key '#00FFFF' \
		--require-v2
	$(PYTHON) $(HATCH_PET_SCRIPTS)/make_contact_sheet.py \
		pets/meow/spritesheet.webp \
		--output qa/meow/contact-sheet-extended.png \
		--scale 1
	$(PYTHON) $(HATCH_PET_SCRIPTS)/make_direction_qa_sheet.py \
		pets/meow/spritesheet.webp \
		--output qa/meow/look-directions.png
	$(PYTHON) $(HATCH_PET_SCRIPTS)/render_animation_previews.py \
		--frames-root $(FRAMES_DIR) \
		--output-dir qa/meow/previews
