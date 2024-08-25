from PIL import Image
import io

def image_to_blob(image):
    """
    Converts an image object (like from Streamlit's file uploader) to a BLOB.

    :param image: An image object (e.g., from Streamlit file uploader).
    :return: Binary data (BLOB) of the image.
    """
    try:
        if hasattr(image, 'read'):  # Check if it's a file-like object
            # Read the image file object as binary
            blob_data = image.read()
        else:
            # Convert PIL Image to binary data
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")  # Save as PNG or appropriate format
            blob_data = buffered.getvalue()

        return blob_data
    except Exception as e:
        print(f"An error occurred while converting image to blob: {e}")
        return None


def blob_to_image(blob_data):
    """
    Converts a BLOB back to an image object.

    :param blob_data: Binary data (BLOB) of the image.
    :return: Image object.
    """
    try:
        # Convert blob data to bytes stream
        image_stream = io.BytesIO(blob_data)
        image = Image.open(image_stream)
        return image
    except Exception as e:
        print(f"An error occurred while converting blob to image: {e}")
        return None
