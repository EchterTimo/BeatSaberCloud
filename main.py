import os
from flask import Flask, render_template, send_file, redirect

app = Flask(__name__)

# Define the folder where the files are stored
BASE_FOLDER = r"C:\Program Files (x86)\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels"
TEMP_FOLDER = "temp"


@app.route('/')
def root():
    return redirect('/beatsaber/customlevels')


@app.route('/beatsaber/customlevels')
def dashboard():
    # Get list of folders in the base folder
    folders = os.listdir(BASE_FOLDER)
    return render_template('custom_levels.html', folders=folders, length=len(folders))


@app.route('/beatsaber/download/<path:folder_path>')
def download(folder_path):
    # Check if the folder exists in the temporary folder
    temp_folder = os.path.join(TEMP_FOLDER, folder_path)
    zip_file = os.path.join(TEMP_FOLDER, folder_path + '.zip')

    if os.path.exists(zip_file):
        print("Download from cache")
    else:
        print("Download using new zip")
        # If the zip file doesn't exist in temp, zip the folder
        folder_to_zip = os.path.join(BASE_FOLDER, folder_path)
        os.makedirs(os.path.dirname(zip_file), exist_ok=True)
        # Zip the folder
        import zipfile
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_to_zip):
                for file in files:
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file), folder_to_zip))

    # Return the zip file
    return send_file(zip_file, as_attachment=True)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
