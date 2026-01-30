#!/usr/bin/env python3
"""
SkautIS Contacts Converter - Web Application

Author: Lukas Tesar <lukastesar03@gmail.com>
"""

import os
import shutil

from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from convert import convert
from git import Repo

app = Flask(__name__)
app.config["DEBUG"] = False
app.config["ENV"] = "production"
app.config.from_object("config")

ALLOWED_EXTENSIONS = set(["xlsx"])


def get_git_version(repo_path="."):
    """Get version info from git (nearest tag + short commit hash)."""
    try:
        repo = Repo(repo_path)
        hexsha = repo.head.commit.hexsha[:7]

        # Try to get the nearest tag
        try:
            tag = repo.git.describe("--tags", "--abbrev=0")
        except Exception:
            tag = None

        return tag, hexsha
    except Exception as e:
        print(f"Error retrieving git info: {e}")
        return None, None


def is_allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_output():
    """Delete all files in the output folder except .gitignore."""
    folder = "static/output"
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            if file_name != ".gitignore":
                file_path = os.path.join(folder, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))


def delete_input():
    """Delete all files in the input folder except .gitignore."""
    folder = "static/input"
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            if file_name != ".gitignore":
                file_path = os.path.join(folder, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))


@app.route("/", methods=["GET", "POST"])
def index():
    """Main route for uploading and converting files."""
    delete_output()
    version, hexsha = get_git_version()
    error = None

    if request.method == "POST":
        file = request.files.get("file")
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join("static/input", filename)
            file.save(input_path)

            # Generate output filename (change extension to .csv)
            base_name = os.path.splitext(filename)[0]
            output_filename = f"contacts_{base_name}.csv"
            output_path = os.path.join("static/output", output_filename)

            try:
                convert(input_path, output_path)
                # Clean up input file
                if os.path.exists(input_path):
                    os.remove(input_path)
                return send_from_directory(
                    "static/output",
                    output_filename,
                    as_attachment=True,
                    download_name=output_filename,
                )
            except Exception as e:
                error = f"Conversion failed: {str(e)}"
                # Clean up on error
                if os.path.exists(input_path):
                    os.remove(input_path)
        else:
            error = "Please upload a valid Excel file (.xlsx)"

    return render_template(
        "index.jinja", version=version, hexsha=hexsha, error=error
    )


if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("static/input", exist_ok=True)
    os.makedirs("static/output", exist_ok=True)
    app.run(debug=False, host="0.0.0.0", port=5000)
