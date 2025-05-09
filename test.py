# import psycopg2
# from dotenv import load_dotenv
# import os
#
# # Load environment variables from .env
# load_dotenv()
#
# # Fetch variables
# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")
#
# def connect_db():
#     try:
#         connection = psycopg2.connect(
#             user=USER,
#             password=PASSWORD,
#             host=HOST,
#             port=PORT,
#             dbname=DBNAME
#         )
#         print("Connection successful!")
#         return connection
#     except Exception as e:
#         print(f"Failed to connect: {e}")
#         return None
#
# def insert_file(filename, file_size, storage_url):
#     connection = connect_db()
#     if connection:
#         try:
#             cursor = connection.cursor()
#
#             # Insert metadata into the files table
#             cursor.execute("""
#                 INSERT INTO uploaded_files (filename, file_size, file_type, storage_url)
#                 VALUES (%s, %s, %s, %s);
#             """, (filename, file_size, "application/octet-stream", storage_url))
#
#             connection.commit()
#             cursor.close()
#             connection.close()
#             print(f"File metadata saved: {filename}")
#
#         except Exception as e:
#             print(f"Error inserting metadata: {e}")
