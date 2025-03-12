from flask import Flask, request, render_template
from google.cloud import storage

app = Flask(__name__)

# Configure the GCS bucket name
GCS_BUCKET_NAME = 'etl-sales-data-bckt'

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None  # To store success message
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                message = 'No selected file'
            else:
                # Upload the file to GCS
                bucket = storage_client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(file.filename)
                blob.upload_from_file(file)
                
                message = f' File "{file.filename}" has been successfully uploaded to Google Cloud Storage!'
    
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
