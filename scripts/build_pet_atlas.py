#!/usr/bin/env python3
"""Build the MEOW Codex Pet atlas from the original macOS MEOW sprites."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps


CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
ROWS = 11
ATLAS_SIZE = (CELL_WIDTH * COLUMNS, CELL_HEIGHT * ROWS)
SOURCE_SIZE = (256, 256)
CROP_BOX = (48, 24, 240, 232)
LOOK_FRAME = 0


@dataclass(frozen=True)
class RowMapping:
    state: str
    source_state: str
    indices: tuple[int, ...]
    mirror: bool = False


STANDARD_ROWS = (
    # Codex Pet v2 fixes frame durations in the app runtime. Repeated source
    # poses reduce visible pose changes while keeping this package portable.
    RowMapping("idle", "sleep", (0, 1, 1, 1, 2, 2)),
    RowMapping("running-right", "roll", (0, 0, 4, 8, 12, 16, 16, 0), mirror=True),
    RowMapping("running-left", "roll", (0, 0, 4, 8, 12, 16, 16, 0)),
    RowMapping("waving", "stretch", (0, 5, 10, 16)),
    RowMapping("jumping", "stretch", (0, 4, 8, 12, 16)),
    RowMapping("failed", "play", (0, 2, 3, 5, 6, 8, 9, 11)),
    RowMapping("waiting", "play", (0, 2, 4, 6, 8, 10)),
    RowMapping("running", "idle", (0, 0, 0, 1, 1, 1)),
    RowMapping("review", "idle", (0, 0, 0, 1, 1, 1)),
)

LOOK_ROWS = (
    RowMapping("look-000-to-157.5", "sleep", (LOOK_FRAME,) * 8),
    RowMapping("look-180-to-337.5", "sleep", (LOOK_FRAME,) * 8),
)

EXPECTED_SOURCE_COUNTS = {
    "idle": 2,
    "roll": 18,
    "stretch": 17,
    "play": 12,
    "sleep": 4,
}

RUNTIME_APPROXIMATION = {
    "runtime_modified": False,
    "idle": {
        "requested_slowdown": 2.0,
        "technique": "Hold three source poses across six runtime slots.",
        "source_indices": [0, 1, 1, 1, 2, 2],
    },
    "roll": {
        "requested_slowdown": 1.5,
        "estimated_pose_change_slowdown": 1.6,
        "technique": "Reduce one cycle from eight visible pose changes to five.",
        "source_indices": [0, 0, 4, 8, 12, 16, 16, 0],
    },
    "stretch": {
        "requested_slowdown": 3.0,
        "requested_visible_repetitions": 1,
        "runtime_repetitions": 3,
        "achieved_slowdown": None,
        "technique": "Preserve one complete source stretch cycle in every runtime cycle.",
        "waving_source_indices": [0, 5, 10, 16],
        "jumping_source_indices": [0, 4, 8, 12, 16],
        "limitation": "The runtime still repeats the complete cycle three times.",
    },
    "seated_idle": {
        "affected_states": ["running", "review"],
        "technique": "Hold each seated source pose for three consecutive runtime slots.",
        "source_indices": [0, 0, 0, 1, 1, 1],
    },
}


def parse_args() -> argparse.Namespace:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=repository / "references" / "cat-orange",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository / "pets" / "meow" / "spritesheet.webp",
    )
    parser.add_argument(
        "--frames-dir",
        type=Path,
        default=repository / ".hatch" / "meow-original" / "frames",
    )
    parser.add_argument(
        "--qa-dir",
        type=Path,
        default=repository / "qa" / "meow",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def report_path(path: Path, repository: Path) -> str:
    try:
        return str(path.relative_to(repository))
    except ValueError:
        return str(path)


def indexed_sources(source_root: Path) -> dict[str, dict[int, Path]]:
    catalog: dict[str, dict[int, Path]] = {}
    for state, expected_count in EXPECTED_SOURCE_COUNTS.items():
        state_dir = source_root / state
        files: dict[int, Path] = {}
        for path in sorted(state_dir.glob("*.png")):
            try:
                index = int(path.stem.rsplit("_", 1)[1])
            except (IndexError, ValueError) as error:
                raise ValueError(f"Unexpected source filename: {path}") from error
            files[index] = path

        expected_indices = set(range(expected_count))
        if set(files) != expected_indices:
            raise ValueError(
                f"{state} needs indices 0...{expected_count - 1}, found {sorted(files)}"
            )
        catalog[state] = files
    return catalog


def clear_hidden_rgb(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = bytearray(rgba.tobytes())
    for offset in range(0, len(pixels), 4):
        if pixels[offset + 3] == 0:
            pixels[offset : offset + 3] = b"\x00\x00\x00"
    return Image.frombytes("RGBA", rgba.size, bytes(pixels))


def load_cell(path: Path, mirror: bool) -> tuple[Image.Image, tuple[int, int, int, int]]:
    with Image.open(path) as opened:
        if opened.size != SOURCE_SIZE:
            raise ValueError(f"{path} must be 256x256, got {opened.size}")
        if "A" not in opened.getbands():
            raise ValueError(f"{path} must contain an alpha channel")
        source = clear_hidden_rgb(opened)

    alpha_box = source.getchannel("A").getbbox()
    if alpha_box is None:
        raise ValueError(f"{path} is empty")
    if not (
        CROP_BOX[0] <= alpha_box[0]
        and CROP_BOX[1] <= alpha_box[1]
        and alpha_box[2] <= CROP_BOX[2]
        and alpha_box[3] <= CROP_BOX[3]
    ):
        raise ValueError(f"{path} content {alpha_box} falls outside crop {CROP_BOX}")

    cell = source.crop(CROP_BOX)
    if mirror:
        cell = ImageOps.mirror(cell)
    return cell, alpha_box


def write_frame(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=False)


def build_atlas(
    catalog: dict[str, dict[int, Path]],
    frames_dir: Path,
) -> tuple[Image.Image, list[dict[str, object]], list[str]]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    for mapping in STANDARD_ROWS:
        state_dir = frames_dir / mapping.state
        if state_dir.is_dir():
            for frame in state_dir.glob("*.png"):
                frame.unlink()

    atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    mapping_entries: list[dict[str, object]] = []
    errors: list[str] = []

    for row_index, mapping in enumerate(STANDARD_ROWS + LOOK_ROWS):
        for column_index, source_index in enumerate(mapping.indices):
            source_path = catalog[mapping.source_state][source_index]
            cell, source_box = load_cell(source_path, mapping.mirror)
            atlas.alpha_composite(
                cell,
                (column_index * CELL_WIDTH, row_index * CELL_HEIGHT),
            )

            frame_path = frames_dir / mapping.state / f"{column_index:02d}.png"
            write_frame(frame_path, cell)
            mapping_entries.append(
                {
                    "state": mapping.state,
                    "row": row_index,
                    "column": column_index,
                    "source_state": mapping.source_state,
                    "source_index": source_index,
                    "source_path": str(source_path),
                    "source_sha256": sha256(source_path),
                    "source_alpha_box": list(source_box),
                    "mirrored": mapping.mirror,
                }
            )

    neutral_source = catalog["sleep"][LOOK_FRAME]
    neutral_cell, neutral_box = load_cell(neutral_source, mirror=False)
    atlas.alpha_composite(neutral_cell, (6 * CELL_WIDTH, 0))
    mapping_entries.append(
        {
            "state": "idle-neutral",
            "row": 0,
            "column": 6,
            "source_state": "sleep",
            "source_index": LOOK_FRAME,
            "source_path": str(neutral_source),
            "source_sha256": sha256(neutral_source),
            "source_alpha_box": list(neutral_box),
            "mirrored": False,
        }
    )

    for row_index, mapping in enumerate(STANDARD_ROWS + LOOK_ROWS):
        used_columns = len(mapping.indices)
        if row_index == 0:
            used_columns += 1
        for column_index in range(used_columns, COLUMNS):
            cell = atlas.crop(
                (
                    column_index * CELL_WIDTH,
                    row_index * CELL_HEIGHT,
                    (column_index + 1) * CELL_WIDTH,
                    (row_index + 1) * CELL_HEIGHT,
                )
            )
            if cell.getchannel("A").getbbox() is not None:
                errors.append(
                    f"row {row_index} column {column_index} must be transparent"
                )

    return atlas, mapping_entries, errors


def verify_lossless_output(output: Path, expected: Image.Image) -> None:
    with Image.open(output) as opened:
        decoded = opened.convert("RGBA")
    if decoded.size != ATLAS_SIZE:
        raise ValueError(f"Atlas must be {ATLAS_SIZE}, got {decoded.size}")
    if decoded.tobytes() != expected.tobytes():
        raise ValueError("Lossless WebP round-trip changed atlas pixels")


def main() -> None:
    args = parse_args()
    repository = Path(__file__).resolve().parents[1]
    source_root = args.source_root.expanduser().resolve()
    output = args.output.expanduser().resolve()
    frames_dir = args.frames_dir.expanduser().resolve()
    qa_dir = args.qa_dir.expanduser().resolve()

    catalog = indexed_sources(source_root)
    atlas, mapping_entries, errors = build_atlas(catalog, frames_dir)
    if errors:
        raise SystemExit("\n".join(errors))

    output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    verify_lossless_output(output, atlas)

    for entry in mapping_entries:
        entry["source_path"] = report_path(Path(str(entry["source_path"])), repository)

    qa_dir.mkdir(parents=True, exist_ok=True)
    source_files = [path for state in catalog.values() for path in state.values()]
    mapping_report = {
        "ok": True,
        "source": "CodlingDev/MEOW cat_orange 1x PNG assets",
        "source_commit": "75a45c3ada731cac99e1df5a5bada598d8de64d2",
        "source_asset_count": len(source_files),
        "source_states": EXPECTED_SOURCE_COUNTS,
        "source_canvas": list(SOURCE_SIZE),
        "cell": [CELL_WIDTH, CELL_HEIGHT],
        "crop_box": list(CROP_BOX),
        "resized": False,
        "redrawn": False,
        "generated": False,
        "direction_response": False,
        "direction_cells": "All 16 cells use the unchanged sleep frame 0.",
        "runtime_approximation": RUNTIME_APPROXIMATION,
        "rows": [
            {
                "state": mapping.state,
                "source_state": mapping.source_state,
                "source_indices": list(mapping.indices),
                "mirrored": mapping.mirror,
            }
            for mapping in STANDARD_ROWS + LOOK_ROWS
        ],
        "frames": mapping_entries,
    }
    (qa_dir / "asset-mapping.json").write_text(
        json.dumps(mapping_report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    review = {
        "ok": True,
        "errors": [],
        "warnings": [],
        "checks": {
            "source_dimensions": "pass",
            "source_alpha": "pass",
            "source_indices": "pass",
            "fixed_crop_contains_all_visible_pixels": "pass",
            "visible_pixels_resampled": False,
            "webp_lossless_roundtrip": "pass",
            "only_running_right_mirrored": True,
            "unused_cells_transparent": True,
            "direction_response_disabled": True,
            "runtime_unchanged": True,
            "timing_approximated_with_source_frame_holds": True,
        },
    }
    (qa_dir / "review.json").write_text(
        json.dumps(review, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    request = {
        "pet_id": "meow",
        "display_name": "MEOW",
        "description": "The original orange tabby from the macOS MEOW app, using its original animations.",
        "sprite_version_number": 2,
        "atlas": {
            "columns": COLUMNS,
            "rows": ROWS,
            "cell_width": CELL_WIDTH,
            "cell_height": CELL_HEIGHT,
            "width": ATLAS_SIZE[0],
            "height": ATLAS_SIZE[1],
        },
        "direction_response": False,
        "asset_mapping": "qa/meow/asset-mapping.json",
    }
    (qa_dir / "pet_request.json").write_text(
        json.dumps(request, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    transparency = {
        "ok": True,
        "applied": False,
        "reason": "Original assets already use transparent RGBA backgrounds; no chroma despill was needed.",
        "hidden_rgb_cleared": True,
        "visible_pixels_changed": False,
    }
    (qa_dir / "transparency.json").write_text(
        json.dumps(transparency, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = {
        "ok": True,
        "spriteVersionNumber": 2,
        "spritesheet": report_path(output, repository),
        "spritesheet_sha256": sha256(output),
        "asset_mapping": report_path(qa_dir / "asset-mapping.json", repository),
        "review": report_path(qa_dir / "review.json", repository),
        "validation": report_path(qa_dir / "validation-extended.json", repository),
        "contact_sheet": report_path(qa_dir / "contact-sheet-extended.png", repository),
        "previews": report_path(qa_dir / "previews", repository),
        "final_visual_qa": report_path(qa_dir / "final-visual-qa.txt", repository),
        "direction_response": False,
    }
    (qa_dir / "run-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "ok": True,
                "output": str(output),
                "frames_dir": str(frames_dir),
                "sha256": summary["spritesheet_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
