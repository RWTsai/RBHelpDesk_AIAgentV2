# mssql_client.py
"""
MSSQL 簡易客戶端，用於整個專案。

開發原則：
- 專注「能用、好讀、好改」
- 不封裝複雜 ORM，也不要抽象化
- 商業邏輯不寫在這裡（寫在 views/nodes）
- 只提供最常用的查詢與執行
"""

from config import get_mssql_conn


def query(sql: str, params: tuple = ()):
    """
    執行 SELECT 查詢，回傳 list of dict。

    用法：
        rows = query("SELECT * FROM User WHERE id=?", (1,))
    """
    rows = []
    try:
        with get_mssql_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)

            columns = [col[0] for col in cursor.description]

            for row in cursor.fetchall():
                # row 是 tuple，把它轉 dict
                rows.append(dict(zip(columns, row)))

    except Exception as e:
        print(f"[mssql_client] 查詢失敗: {e}\nSQL={sql}")
        raise

    return rows


def query_one(sql: str, params: tuple = ()):
    """
    執行 SELECT，僅取第一筆資料。
    """
    result = query(sql, params)
    return result[0] if result else None


def execute(sql: str, params: tuple = ()):
    """
    執行 INSERT / UPDATE / DELETE，回傳影響筆數。

    用法：
        count = execute("UPDATE User SET name=? WHERE id=?", ("Alan", 3))
    """
    try:
        with get_mssql_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount

    except Exception as e:
        print(f"[mssql_client] 執行失敗: {e}\nSQL={sql}")
        raise


def execute_many(sql: str, batch_params: list):
    """
    針對批次寫入的輔助方法。
    batch_params: List[Tuple]

    用法：
        execute_many(
            "INSERT INTO Log (msg) VALUES (?)",
            [("A",), ("B",), ("C",)]
        )
    """
    try:
        with get_mssql_conn() as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, batch_params)
            conn.commit()
            return cursor.rowcount

    except Exception as e:
        print(f"[mssql_client] 批次執行失敗: {e}\nSQL={sql}")
        raise
