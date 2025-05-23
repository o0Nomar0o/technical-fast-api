import os
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi import HTTPException
from tempfile import NamedTemporaryFile
from supabase import create_client, Client

# Supabase setup
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_doc(bot_response):
    try:
        with NamedTemporaryFile(delete=False, suffix=".md") as temp_file:
            temp_file.write(bot_response.encode('utf-8'))
            temp_file_path = temp_file.name
            temp_file_name = os.path.basename(temp_file.name)

        with open(temp_file_path, "rb") as f:
            content = f.read()
            storage_resp = supabase.storage.from_("docs").upload(temp_file_name, content)

            signed_url = supabase.storage.from_("docs").create_signed_url(temp_file_name,7889400, options={"download": temp_file_name})
            print(signed_url)

            return signed_url['signedURL']
        # return supabase.storage.from_("docs").get_public_url(temp_file_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def bucket_exists(bucket_name: str) -> bool:
    try:
        buckets = supabase.storage.list_buckets()
        return any(bucket.name == bucket_name for bucket in buckets)
    except Exception:
        return False

