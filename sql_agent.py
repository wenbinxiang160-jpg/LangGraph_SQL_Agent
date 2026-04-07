from sqlalchemy import create_engine, text

from agent_state import AgentState

from llm import llm

# 连接你的 MySQL（本地生活平台的库）
engine = create_engine("mysql+pymysql://root:root@localhost/hmdp")

SQL_PROMPT = """你是 MySQL 专家。数据库有以下表：

表结构：
- tb_shopCREATE TABLE `tb_shop` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '商铺名称',
  `type_id` bigint unsigned NOT NULL COMMENT '商铺类型的id',
  `images` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '商铺图片，多个图片以'',''隔开',
  `area` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '商圈，例如陆家嘴',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '地址',
  `x` double unsigned NOT NULL COMMENT '经度',
  `y` double unsigned NOT NULL COMMENT '维度',
  `avg_price` bigint unsigned DEFAULT NULL COMMENT '均价，取整数',
  `sold` int(10) unsigned zerofill NOT NULL COMMENT '销量',
  `comments` int(10) unsigned zerofill NOT NULL COMMENT '评论数量',
  `score` int(2) unsigned zerofill NOT NULL COMMENT '评分，1~5分，乘10保存，避免小数',
  `open_hours` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '营业时间，例如 10:00-22:00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `foreign_key_type` (`type_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPACT
- tb_shop_type:
    CREATE TABLE `tb_shop_type` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '类型名称',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '图标',
  `sort` int unsigned DEFAULT NULL COMMENT '顺序',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPACT
- tb_voucher:
    CREATE TABLE `tb_voucher` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `shop_id` bigint unsigned DEFAULT NULL COMMENT '商铺id',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '代金券标题',
  `sub_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '副标题',
  `rules` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '使用规则',
  `pay_value` bigint unsigned NOT NULL COMMENT '支付金额，单位是分。例如200代表2元',
  `actual_value` bigint NOT NULL COMMENT '抵扣金额，单位是分。例如200代表2元',
  `type` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '0,普通券；1,秒杀券',
  `status` tinyint unsigned NOT NULL DEFAULT '1' COMMENT '1,上架; 2,下架; 3,过期',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPACT
- tb_voucher_order
    CREATE TABLE `tb_voucher_order` (
  `id` bigint NOT NULL COMMENT '主键',
  `user_id` bigint unsigned NOT NULL COMMENT '下单的用户id',
  `voucher_id` bigint unsigned NOT NULL COMMENT '购买的代金券id',
  `pay_type` tinyint unsigned NOT NULL DEFAULT '1' COMMENT '支付方式 1：余额支付；2：支付宝；3：微信',
  `status` tinyint unsigned NOT NULL DEFAULT '1' COMMENT '订单状态，1：未支付；2：已支付；3：已核销；4：已取消；5：退款中；6：已退款',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
  `pay_time` timestamp NULL DEFAULT NULL COMMENT '支付时间',
  `use_time` timestamp NULL DEFAULT NULL COMMENT '核销时间',
  `refund_time` timestamp NULL DEFAULT NULL COMMENT '退款时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPACT
规则：
1. 只生成 SELECT 语句
2. 时间用 DATE_FORMAT(create_time, '%Y-%m') 处理月份
3. 只输出 SQL，不要解释

用户问题：{question}
"""


def sql_agent(state: AgentState) -> AgentState:
    # 1. 让 LLM 生成 SQL
    sql = llm.invoke(SQL_PROMPT.format(question=state["question"])).content.strip()

    # 2. 安全检查（面试可以提这个点）
    if any(kw in sql.upper() for kw in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        return {"sql": sql, "query_result": [{"error": "危险操作被拦截"}]}

    # 3. 执行 SQL
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = [dict(row._mapping) for row in result.fetchall()]
            print(f"sql: {sql}, query_result: {rows}")
        return {"sql": sql, "query_result": rows}
    except Exception as e:
        # SQL 出错，告诉 Supervisor 重试（面试可以讲这个容错机制）
        return {"sql": sql, "query_result": [{"error": str(e)}]}


if __name__ == '__main__':
    state = {
        "question": "哪个商家的创建时间最晚？",
        "sql": "",
        "query_result": [],
        "analysis": "",
        "report": "",
        "next": ""
    }
    result = sql_agent(state=state)
    print("生成的 SQL:", result["sql"])
    print("查询结果:", result["query_result"])
