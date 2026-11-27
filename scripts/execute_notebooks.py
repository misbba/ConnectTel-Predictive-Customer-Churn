"""
Notebook Execution and Output Serialization Script.
ConnectTel / Persevex AI Internship Project - Phase 7.2.

Executes all 3 project Jupyter notebooks in sequence:
1. 01_eda_and_feature_engineering.ipynb
2. 02_model_training_and_tuning.ipynb
3. 03_model_interpretation_and_business_recommendations.ipynb

Preserves all markdown cells and source code intact.
Captures stdout, stderr, display_data (PNG images, DataFrames), and execute_result.
Saves execution counts and populated outputs directly into the original .ipynb files.
"""

import ast
import base64
import contextlib
import io
import json
import os
import sys
import types
from pathlib import Path

# Project paths
ROOT_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
SRC_DIR = ROOT_DIR / "src"

# Mock IPython and IPython.display to support display() and Image() seamlessly
class MockImage:
    def __init__(self, filename=None, data=None, width=None, height=None):
        self.filename = filename
        self.width = width
        self.height = height
        if filename:
            with open(filename, "rb") as f:
                self.data = f.read()
        else:
            self.data = data or b""

    def _repr_png_(self):
        return self.data


_CURRENT_CELL_DISPLAYS = []


def mock_display(*objs, **kwargs):
    for obj in objs:
        _CURRENT_CELL_DISPLAYS.append(obj)


# Inject mock IPython into sys.modules
mock_ipython = types.ModuleType("IPython")
mock_ipython.get_ipython = lambda: None
mock_ipython_display = types.ModuleType("IPython.display")
mock_ipython_display.Image = MockImage
mock_ipython_display.display = mock_display
mock_ipython.display = mock_ipython_display
sys.modules["IPython"] = mock_ipython
sys.modules["IPython.display"] = mock_ipython_display


def format_text_lines(text: str):
    """Format string into list of lines ending with newline for notebook JSON."""
    if not text:
        return []
    lines = text.splitlines(keepends=True)
    return lines


def format_dataframe_output(df, exec_count=None):
    """Generate execute_result or display_data payload for pandas DataFrame."""
    import pandas as pd
    html_repr = df.to_html()
    text_repr = repr(df)
    data = {
        "text/html": [html_repr],
        "text/plain": format_text_lines(text_repr)
    }
    return data


def format_image_output(img_obj):
    """Generate display_data payload for MockImage."""
    b64_png = base64.b64encode(img_obj.data).decode("ascii")
    data = {
        "image/png": b64_png,
        "text/plain": ["<IPython.core.display.Image object>"]
    }
    return data


def execute_notebook(nb_path: Path):
    print("=" * 75)
    print(f"EXECUTING NOTEBOOK: {nb_path.name}")
    print("=" * 75)

    with open(nb_path, "r", encoding="utf-8") as f:
        nb_json = json.load(f)

    # Isolated execution namespace
    nb_globals = {
        "__name__": "__main__",
        "__file__": str(nb_path),
        "PROJECT_ROOT": ROOT_DIR,
        "display": mock_display,
        "Image": MockImage
    }

    # Execute inside the notebooks directory so relative paths resolve cleanly
    old_cwd = os.getcwd()
    os.chdir(str(NOTEBOOKS_DIR))

    exec_count = 1
    total_cells = len(nb_json.get("cells", []))
    code_cell_num = 0

    try:
        for i, cell in enumerate(nb_json.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue

            code_cell_num += 1
            source_lines = cell.get("source", [])
            code_text = "".join(source_lines).strip()

            print(f"\n[Cell {i+1} | Code Cell {code_cell_num}] Running ({len(source_lines)} lines)...")
            first_line = source_lines[0].strip() if source_lines else ""
            print(f"  First statement: {first_line[:65]}")

            # Clear cell displays list before running cell
            _CURRENT_CELL_DISPLAYS.clear()

            # Set execution count
            cell["execution_count"] = exec_count
            outputs = []

            # Capture stdout and stderr
            stdout_buf = io.StringIO()
            stderr_buf = io.StringIO()

            eval_result = None
            has_eval_result = False

            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                try:
                    # Parse AST to check if last statement is an expression
                    parsed = ast.parse(code_text)
                    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
                        # Split statements and last expression
                        last_expr = parsed.body.pop()
                        if parsed.body:
                            stmts_code = compile(parsed, filename=str(nb_path), mode="exec")
                            exec(stmts_code, nb_globals)

                        expr_code = compile(ast.Expression(body=last_expr.value), filename=str(nb_path), mode="eval")
                        eval_result = eval(expr_code, nb_globals)
                        if eval_result is not None:
                            has_eval_result = True
                    else:
                        full_code = compile(parsed, filename=str(nb_path), mode="exec")
                        exec(full_code, nb_globals)

                except Exception as e:
                    # Print and raise error with exact notebook, cell number, and traceback
                    print(f"\n❌ FATAL EXECUTION ERROR in {nb_path.name}:")
                    print(f"   Cell Index: {i+1} (Code Cell #{code_cell_num})")
                    print(f"   Exception: {type(e).__name__}: {e}")
                    import traceback
                    tb_lines = traceback.format_exc().splitlines(keepends=True)
                    error_output = {
                        "output_type": "error",
                        "ename": type(e).__name__,
                        "evalue": str(e),
                        "traceback": tb_lines
                    }
                    cell["outputs"] = [error_output]
                    # Re-raise to halt
                    raise RuntimeError(f"Notebook {nb_path.name} failed at Cell {i+1} (Code #{code_cell_num}): {e}") from e

            # Process stdout
            stdout_str = stdout_buf.getvalue()
            if stdout_str:
                outputs.append({
                    "output_type": "stream",
                    "name": "stdout",
                    "text": format_text_lines(stdout_str)
                })
                # Log excerpt to console
                print(f"  [stdout]: {len(stdout_str)} chars captured")

            # Process stderr
            stderr_str = stderr_buf.getvalue()
            if stderr_str:
                outputs.append({
                    "output_type": "stream",
                    "name": "stderr",
                    "text": format_text_lines(stderr_str)
                })
                print(f"  [stderr]: {len(stderr_str)} chars captured")

            # Process display() calls
            for disp_item in _CURRENT_CELL_DISPLAYS:
                if isinstance(disp_item, MockImage):
                    outputs.append({
                        "output_type": "display_data",
                        "data": format_image_output(disp_item),
                        "metadata": {}
                    })
                    print("  [display]: MockImage rendered to base64 display_data")
                elif hasattr(disp_item, "to_html"):
                    outputs.append({
                        "output_type": "display_data",
                        "data": format_dataframe_output(disp_item),
                        "metadata": {}
                    })
                    print(f"  [display]: DataFrame ({disp_item.shape}) rendered to HTML/text display_data")
                else:
                    outputs.append({
                        "output_type": "display_data",
                        "data": {"text/plain": format_text_lines(repr(disp_item))},
                        "metadata": {}
                    })
                    print(f"  [display]: Object ({type(disp_item).__name__}) rendered to text display_data")

            # Process last expression evaluation (execute_result)
            if has_eval_result:
                if hasattr(eval_result, "to_html"):
                    outputs.append({
                        "output_type": "execute_result",
                        "execution_count": exec_count,
                        "data": format_dataframe_output(eval_result, exec_count),
                        "metadata": {}
                    })
                    print(f"  [execute_result]: DataFrame ({eval_result.shape}) captured")
                else:
                    outputs.append({
                        "output_type": "execute_result",
                        "execution_count": exec_count,
                        "data": {"text/plain": format_text_lines(repr(eval_result))},
                        "metadata": {}
                    })
                    print(f"  [execute_result]: {type(eval_result).__name__} captured")

            # Check for any active matplotlib figures
            try:
                import matplotlib.pyplot as plt
                fignums = plt.get_fignums()
                if fignums:
                    for fignum in fignums:
                        fig = plt.figure(fignum)
                        buf = io.BytesIO()
                        fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
                        buf.seek(0)
                        b64_png = base64.b64encode(buf.read()).decode("ascii")
                        outputs.append({
                            "output_type": "display_data",
                            "data": {
                                "image/png": b64_png,
                                "text/plain": [f"<Figure size {fig.get_size_inches()} with {len(fig.axes)} Axes>"]
                            },
                            "metadata": {}
                        })
                        print(f"  [matplotlib]: Captured figure {fignum} as PNG")
                    plt.close("all")
            except Exception as e:
                print(f"  [matplotlib note]: {e}")

            cell["outputs"] = outputs
            exec_count += 1

        print(f"\n✓ Notebook {nb_path.name} execution completed successfully ({code_cell_num} code cells executed).")

        # Save populated notebook back to original path
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb_json, f, indent=1, ensure_ascii=False)
        print(f"✓ Saved populated notebook to: {nb_path}")

    finally:
        os.chdir(old_cwd)


def main():
    notebooks = [
        NOTEBOOKS_DIR / "01_eda_and_feature_engineering.ipynb",
        NOTEBOOKS_DIR / "02_model_training_and_tuning.ipynb",
        NOTEBOOKS_DIR / "03_model_interpretation_and_business_recommendations.ipynb"
    ]

    for nb_path in notebooks:
        if not nb_path.exists():
            raise FileNotFoundError(f"Notebook file not found: {nb_path}")

    for nb_path in notebooks:
        execute_notebook(nb_path)

    print("\n" + "=" * 75)
    print("ALL THREE NOTEBOOKS EXECUTED AND SAVED WITH 100% SUCCESS!")
    print("=" * 75)


if __name__ == "__main__":
    main()
