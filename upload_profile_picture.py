import os
import requests
from flask import request, jsonify, g
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads/profile_pictures"


def upload_profile_picture_url(current_user):
    """
    Accepts a remote image URL and saves it as the user's profile picture.
    """
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    try:
        # Vulnerability: SSRF — image_url is user-controlled with no allowlist or
        # host validation. Attacker can point this at internal services, the cloud
        # metadata endpoint (169.254.169.254), or loopback addresses.
        resp = requests.get(image_url, timeout=10, allow_redirects=True, verify=False)

        if resp.status_code != 200:
            return jsonify({"error": "Failed to fetch image"}), 400

        content_type = resp.headers.get("Content-Type", "")
        ext = ".jpg"
        if "png" in content_type:
            ext = ".png"
        elif "gif" in content_type:
            ext = ".gif"

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(f"user_{current_user['id']}_profile{ext}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(resp.content)

        return jsonify({"message": "Profile picture updated", "file_path": file_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
