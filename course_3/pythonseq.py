import psycopg2

db_config = {
    "host": "pg.pg4e.com",
    "port": 5432,
    "database": "pg4e_4f0d22be5d",
    "user": "pg4e_4f0d22be5d",
    "password": "pg4e_p_aa9df6710fe8c16"
}

create_table_query = """
CREATE TABLE IF NOT EXISTS pythonseq (
    iter INTEGER,
    val INTEGER
);
"""

def generate_and_insert_sequence():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(create_table_query)
        conn.commit()

        value = 165156
        insert_query = "INSERT INTO pythonseq (iter, val) VALUES (%s, %s)"

        for i in range(300):
            iter_num = i + 1
            cursor.execute(insert_query, (iter_num, value))
            value = int((value * 22) / 7) % 1000000

        conn.commit()

        print("300 numbers have been inserted.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

generate_and_insert_sequence()
