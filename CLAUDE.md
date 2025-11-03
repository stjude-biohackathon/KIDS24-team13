# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

napari-IDMS is a napari plugin that provides integration with IDMS (Image Data Management System). The plugin enables users to browse, select, and materialize image data, ROIs (Regions of Interest), and segmentations from IDMS directly within the napari viewer.

## Environment Setup

### Required Environment Variables

The plugin requires three environment variables to connect to IDMS:

```shell
conda env config vars set IDMS_API_ENDPOINT=''
conda env config vars set PYIDMS_PLUGIN_LOCATION=''
conda env config vars set IDMS_API_TOKEN=''

conda deactivate 'env_name'
conda activate 'env_name'
```

- `IDMS_API_ENDPOINT`: The IDMS API server endpoint
- `PYIDMS_PLUGIN_LOCATION`: Path to the IDMS Python plugin library
- `IDMS_API_TOKEN`: Authentication token for IDMS API

### Installation

```shell
pip install napari-IDMS
python -m pip install "napari[all]"
```

Launch napari:
```shell
napari
```

## Development Commands

### Testing

Run all tests with coverage:
```shell
tox
```

Run tests for a specific Python version and platform:
```shell
tox -e py39-linux
tox -e py310-macos
tox -e py311-windows
```

Run pytest directly (requires testing dependencies):
```shell
pytest -v --color=yes --cov=napari_idms --cov-report=xml
```

### Code Quality

Format code with black (line length: 79):
```shell
black src/
```

Lint with ruff (auto-fix enabled):
```shell
ruff check src/
```

## Architecture

### Widget Hierarchy

The plugin uses a tabbed interface architecture:

1. **Main_Widget** (`_widget.py`): Root widget that creates a QTabWidget container
   - Initializes IDMS_Backend_object (single instance shared across tabs)
   - Creates IDMS_main_object (shared reference for inter-tab communication)
   - Adds tabs for IDMS main, ROI Generator, and Segmentation

2. **IDMS_main_widget** (`IDMS_main_widget.py`): Primary interface for browsing and loading IDMS data
   - Hierarchical navigation: Owner -> Project -> Group -> Image Collection
   - ROI and Segmentation selection via CheckBoxPopup widgets
   - Advanced settings for custom ROI coordinates
   - Materializes data to napari viewer with proper spatial offsets

3. **ROI_Generator_widget** (`roi_generator_widget.py`): Creates new ROIs from napari shapes
   - Monitors napari viewer for shape layers
   - Uploads ROI definitions to IDMS
   - Refreshes IDMS_main_widget ROI list after creation

4. **Segmentation_widget** (`segmentation_generator_widget.py`): Uploads segmentation masks
   - Selects label layers from napari viewer
   - Associates segmentations with existing ROIs
   - Exports to OME-TIFF and uploads to IDMS

### Backend Communication

**IDMS_Backend** (`idms_backend.py`) wraps the IDMS API and provides:
- Hierarchical data retrieval (owners, projects, groups, image collections)
- ROI box operations (search, create, get details)
- Segmentation operations (search, create)
- Image array retrieval with proper dimensionality handling
- Channel stacking for multi-channel images
- Dimension transposition (IDMS format <-> napari format)

**Key Pattern**: The backend uses the external IDMS Python library loaded from `PYIDMS_PLUGIN_LOCATION`, importing from `common.*` modules.

### UI Files

Qt Designer `.ui` files are stored in `src/UI_files/` and loaded at runtime via `uic.loadUi()`. Main UI files:
- `Main_UI.ui`: Tab widget container
- `IDMS_main.ui`: Main IDMS browser interface
- `roi_generate_tab.ui`: ROI generator form
- `segmentation.ui`: Segmentation upload form
- `roi_list_item.ui`: Individual ROI list item widget

### Inter-Widget Communication

Widgets that need access to IDMS_main_widget state receive it as a constructor parameter:
```python
ROI_Generator_widget(viewer, idms_backend, idms_main_object)
Segmentation_widget(viewer, idms_backend, idms_main_object)
```

After creating ROIs or segmentations, child widgets call:
- `idms_main_object.roi_refresh()`: Refresh ROI list
- `idms_main_object.seg_refresh()`: Refresh segmentation list

### Data Materialization

When loading data from IDMS, the plugin:
1. Retrieves numpy arrays via IDMS backend
2. Expands 2D arrays to 3D (adds Z dimension) if needed
3. Applies spatial offsets using napari's `translate` parameter
4. Adds images as `viewer.add_image()` or labels as `viewer.add_labels()`

Coordinate system: (Z, Y, X) with offsets from ROI/segmentation metadata.

## Testing

Test files are in `src/napari_idms/_tests/`:
- `test_widget.py`: Widget instantiation tests
- `test_writer.py`: Data writer tests

The test suite requires:
- pytest
- pytest-cov (coverage)
- pytest-qt (Qt widget testing)
- napari
- pyqt5

## Key Design Patterns

1. **Hierarchical Dropdown Population**: Each combobox level triggers clearing and repopulating downstream comboboxes
2. **Custom CheckBox Widgets**: CheckBoxPopup and CheckableComboBox for multi-selection
3. **Progress Tracking**: QProgressBar updated during materialization
4. **Shared Backend**: Single IDMS_Backend instance passed to all widgets
5. **UI File Loading**: Dynamic UI loading from `.ui` files rather than hardcoded layouts
6. **Dimension Handling**: Automatic 2D->3D expansion and CZYX transposition

## Important Notes

- The plugin depends on an external IDMS Python library that must be available at the path specified in `PYIDMS_PLUGIN_LOCATION`
- Line length is enforced at 79 characters (black and ruff config)
- Runtime type annotations are required for magicgui (pyupgrade checks UP006/UP007 are disabled)
- The plugin is currently marked as `visibility: hidden` in the napari hub
