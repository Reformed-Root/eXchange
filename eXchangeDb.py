import mysql.connector 

def load_secrets(path):
    secrets = {}
    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                secrets[key] = value
    return secrets

def get_connection():
    secrets = load_secrets("secrets.txt")
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd=secrets["key"],
        database=secrets["db"],
        port=secrets["port"]
    ) 



def fetch_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, genre FROM exbooks")
    return cursor.fetchall()


secrets = load_secrets("secrets.txt")

eXdb = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = secrets["key"], database = secrets["db"], port = secrets["port"])

print(eXdb)

if __name__ == "__main__":
    conn = get_connection()
    print("✅ Connected:", conn)
    for row in fetch_books():
        print(row)