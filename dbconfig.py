from sqlalchemy import inspect, create_engine

engine = create_engine("mysql+pymysql://root:root@localhost/hmdp")


def get_all_table_ddl() -> dict:
    """自动从数据库读取所有表结构"""
    inspector = inspect(engine)
    ddl_map = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        col_desc = []
        for col in columns:
            col_desc.append(f"  {col['name']} {col['type']} -- {col.get('comment', '')}")
        ddl_map[table_name] = f"表名：{table_name}\n字段：\n" + "\n".join(col_desc)

    return ddl_map


# 启动时加载一次，不用每次查库
TABLE_DDL = get_all_table_ddl()
TABLE_NAMES = list(TABLE_DDL.keys())