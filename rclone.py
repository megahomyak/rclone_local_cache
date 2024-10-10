import sqlite3
import os
import sys


connection = sqlite3.connect("rclone_local_cache.sqlitedb")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS remotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
);

CREATE TABLE IF NOT EXISTS files (
remote_id INTEGER,
modification_time INTEGER,
file_path TEXT,
);

CREATE INDEX IF NOT EXISTS files_index ON files (file_name, remote_id);
""")

for remote in sys.argv[1:]:
    cursor.execute("INSERT OR IGNORE INTO remotes (name) VALUES (?);", remote)
    cursor.execute("SELECT (file_name, modification_time) FROM files WHERE remote_id=(SELECT (id) FROM remotes WHERE name = ?)", remote)
    old_data = cursor.fetchall()


for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        full_path = os.path.join(dirpath, filename)

cursor.close()
connection.close()
