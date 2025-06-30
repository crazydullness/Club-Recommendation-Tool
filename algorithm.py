import json
import pypinyin

prefers=[]

def load_prefers():
    file_name="prefers.json"
    with open(file_name, "r", encoding="utf-8") as f:
        Prefers = json.load(f)
    return Prefers

def save_prefers2(c):
    file_name="prefers.json"
    prefers.remove(c)
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(prefers, f, ensure_ascii=False, indent=4)

def save_prefers1(c):
    file_name="prefers.json"
    prefers.append(c)
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(prefers, f, ensure_ascii=False, indent=4)

def save_prefers0():
    file_name="prefers.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(prefers, f, ensure_ascii=False, indent=4)

def clear_prefers():
    file_name="prefers.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

name = ["学生艺术总团舞蹈分团", "“我们”文学社", "”新颜“学生造型协会", "”燕聚“学生校友交流协会", "Linux俱乐部",
        "PKU学生创业圈", "爱心社", "铁路文化协会", "湖湘文化研究会", "创意学社", "八桂发展研究会", "电影协会",
        "东南亚协会", "对冲基金协会", "翻译协会", "传统服饰文化学生交流协会", "道学文化研究社", "曲艺协会", "耕读社",
        "辩论协会", "浦江发展协会", "教育知行社", "荆楚学生发展协会", "开源软件协会", "科幻协会", "流浪猫关爱协会",
        "绿色生命协会", "模拟联合国协会", "魔方社", "魔术爱好者协会", "民俗研究会", "儒行社", "中国音乐学社",
        "书 画协会", "武侠文化交流研究协会", "红十字会学生分会", "青年智库协会", "趣听脱口秀协会", "生活创意协会",
        "三晋文化研究会", "生态文明与碳中和研究社", "手风琴协会", "思维潜能开发协会", "台湾研究会", "提琴社", "钢琴社",
        "推理协会", "人工智能研究会", "五四文学社", "现代 艺术协会", "新媒体通讯社", "信用文化协会",
        "亚洲未来政治人协会", "心理协会", "音乐创作协会", "音乐剧社", "烹饪与美食协会", "元火动漫社", "口琴协会",
        "易学社", "禅学社", "群青美术社", "中医学社", "国际交流协会", "青年摄影协会", "未名红学社", "围棋社",
        "越剧协会", "黄梅剧社", "苏韵文化交流协会", "赣文化交流学会", "中国象棋协会", "龙舟协会", "武术协会", "京昆社",
        "风雷街舞社", "北大剧社", "地板球协会", "弓行社", "影视创作协会", "飞盘协会", "橄榄球协会", "高尔夫协会",
        "滑板协会", "滑雪协会", "击剑协会", "剑道协会", "健身健美协会", "篮 球协会", "轮滑爱好者协会", "排球爱好者协会",
        "青年天文学会", "乒乓球协会", "柔道协会", "赛艇协会", "散打社", "山鹰社", "素质拓展协会", "台球协会",
        "跆拳道社", "徒步爱好者协会", "空手道协会", "游泳爱好者协会", "跑步爱好者协会", "自行车协会", "足球协会",
        "棒垒球协会", "综合格斗社", "之江发展论坛", "中韩交流协会", "中日交流协会", "创业投资研究协会",
        "葡萄酒文化交流协会", "体教部王其和式太极拳社", "体教部国术短乒社", "体教部保龄球协会", "学术写作与表达协会",
        "仲英公益促进协会", "羽毛球协会", "燕语配音社"]

link = ["https://mp.weixin.qq.com/s/XsGAQppcZsNUJ4yPmBJooA", "https://mp.weixin.qq.com/s/4Yq1xEpB3shYRwVv1RjjnQ",
        "https://mp.weixin.qq.com/s/_nKmsP9g85zEpb9w7EPVFA", "https://mp.weixin.qq.com/s/baKnAxn_qSHJZmgpvPaoIg",
        "https://mp.weixin.qq.com/s/GIps1i6ieq2MtW8foDaiZA", "https://mp.weixin.qq.com/s/hOJthDNYmgKVyQ2vzJxwzQ",
        "https://mp.weixin.qq.com/s/HdqWHlER-vAxB8gz1A6Z6g", "https://mp.weixin.qq.com/s/b-R9U839GLgWLbvF8AYTvg",
        "https://mp.weixin.qq.com/s/fB1vERSzGe9sBNAt9QYbdA", "https://mp.weixin.qq.com/s/kYDW2a4Gtd0fupdMzVEoEA",
        "https://mp.weixin.qq.com/s/gjf2pQUqkdsQik6TPV_KLw", "https://mp.weixin.qq.com/s/DJ58u_Z-Bagm_8GPhTo03w",
        "https://mp.weixin.qq.com/s/rZhjViIw4bC4MF3li_lVdw", "https://mp.weixin.qq.com/s/KPXHmqtOUz5lAndLVRRzgQ",
        "https://mp.weixin.qq.com/s/hYSS2jnqLEkaIlNfQ5jgjA", "https://mp.weixin.qq.com/s/x3zvUhcIguUDcppLzldX8Q",
        "https://mp.weixin.qq.com/s/7c2uNoEK6Rh7fMP-icuNQQ", "https://mp.weixin.qq.com/s/2GFNoaR0IFbmVVNr1nx4mg",
        "https://mp.weixin.qq.com/s/DfikQ_st35pn4ApkPWIP4A", "https://mp.weixin.qq.com/s/W3AO05TzSaQ5EuqjyeZYVg",
        "https://mp.weixin.qq.com/s/GmsXLDpyH-m4BxPQVNOHZA", "https://mp.weixin.qq.com/s/5n8MVgbb6Iy3xoiLNfgp1Q",
        "https://mp.weixin.qq.com/s/NulxOe_lSn-UEyvnCLI_YQ", "https://mp.weixin.qq.com/s/YfqMYXqFU1ToN8RaEYLTjg",
        "https://mp.weixin.qq.com/s/BRQ48-y9MYLsJjZzTXYXUg", "https://mp.weixin.qq.com/s/_Lr8PeBmD2t-OnGyU_APcg",
        "https://mp.weixin.qq.com/s/Hr3abEVGI6paxo2sUZAn7w", "https://mp.weixin.qq.com/s/n-YoevkTr_j3ypK0KIc13g",
        "https://mp.weixin.qq.com/s/bSiceCQiDWKX0c86T1tSVA", "https://mp.weixin.qq.com/s/5jBJ8jd2zTmn2AcUDshJ5w",
        "https://mp.weixin.qq.com/s/QpuX7FezRYJ3uxFwLAAgpg", "https://mp.weixin.qq.com/s/6OT4_BAYfsY6rgirHGuVwQ",
        "https://mp.weixin.qq.com/s/umHc2P8-xFnQIpeGps2ymw", "https://mp.weixin.qq.com/s/dADU-bwA4Tz___vFxUsM8g",
        "https://mp.weixin.qq.com/s/S61yWXeyYMf_-lbHwU9x7Q", "https://mp.weixin.qq.com/s/wzhW_nWcqCMEkoLuAfqRTg",
        "https://mp.weixin.qq.com/s/aVr-fPZbslcCyaqB2hyQkQ", "https://mp.weixin.qq.com/s/VTtYj5WDYcGDB1_91Dr01Q",
        "https://mp.weixin.qq.com/s/J-HrCEueC-p_Qut-D1DgVA", "https://mp.weixin.qq.com/s/M--a136j2S_I9Uo-b-WGdw",
        "https://mp.weixin.qq.com/s/EED9Z04Vvm7WqKGLrNZosQ", "https://mp.weixin.qq.com/s/9Gup0LocbYvGqD6RjN5q9Q",
        "https://mp.weixin.qq.com/s/O4PM91NEoCg-bAPjSq2MQg", "https://mp.weixin.qq.com/s/szACUxHldPEfrqNrdLXOkg",
        "https://mp.weixin.qq.com/s/k9GWc-4U3hFaVKoIMQk_9g", "https://mp.weixin.qq.com/s/3UhlVN0VSFJaSZjhDPiTaA",
        "https://mp.weixin.qq.com/s/eNnZ4VkHWO7KnfnJgqaWMA", "https://mp.weixin.qq.com/s/TmYGbyJbTz4pSrplaDJjrg",
        "https://mp.weixin.qq.com/s/m8fafwWkddKpE6Ng7UaFDA", "https://mp.weixin.qq.com/s/V0MTWa0HXb8OOleiGESemQ",
        "https://mp.weixin.qq.com/s/sIv_nrHSSiaHPXJVIlS2Hw", "https://mp.weixin.qq.com/s/ONqCg3hcXVQ5FP1SvzkE8g",
        "https://mp.weixin.qq.com/s/L9B2qlquvIjdOUFOa7shDw", "https://mp.weixin.qq.com/s/1Kq2LlqT9Em698TEPIG5Gg",
        "https://mp.weixin.qq.com/s/Iad1fq-w8LmiQix5ySJe0w", "https://mp.weixin.qq.com/s/JlwBb5TxHbv2Uxng86vVSQ",
        "https://mp.weixin.qq.com/s/jzMbMA-8lFGotBaKcIfehg", "https://mp.weixin.qq.com/s/XvJtzA3O4hxrVT71JV-7QQ",
        "https://mp.weixin.qq.com/s/C_V3gz-41Zp7WQml6wR2uw", "https://mp.weixin.qq.com/s/p3St1T3ILlzMAjXuWMz72A",
        "https://mp.weixin.qq.com/s/ilnETkTvK8yJU8WSiGrX5A", "https://mp.weixin.qq.com/s/zcW4Sgyx3ZR7BKnoXUSuzw",
        "https://mp.weixin.qq.com/s/nImvcggTsld-kOv4czfsFA", "https://mp.weixin.qq.com/s/7Oj-yQAjPH0_RYCzv7ONLA",
        "https://mp.weixin.qq.com/s/8tYeaRoOPsE_sKtrNR_lhw", "https://mp.weixin.qq.com/s/G8x7M5U35qqfbFSiXLZKGg",
        "https://mp.weixin.qq.com/s/7ro5H4nbi_SsVmcxO5N8jw", "https://mp.weixin.qq.com/s/oULedWdETmwwgVBO8uHdFw",
        "https://mp.weixin.qq.com/s/Y1grC4pFZ5_OIvmG8mA-ng", "https://mp.weixin.qq.com/s/y9dRiueVkmkiMEx1x2MlLQ",
        "https://mp.weixin.qq.com/s/w6wqE1wsquM8LzvKzU70gw", "https://mp.weixin.qq.com/s/fAGaNnfDK837ZifOcOmD-g",
        "https://mp.weixin.qq.com/s/tYGJR62o8CjS0oYfLa_Uhw", "https://mp.weixin.qq.com/s/MviY68tSLq-foZGZQFtpzA",
        "https://mp.weixin.qq.com/s/oI7kh3MjzC1xoWDzm-8tOQ", "https://mp.weixin.qq.com/s/Pdu5s4bEJ6MD2dPlHTczkg",
        "https://mp.weixin.qq.com/s/aXbb_-DdnLvXNaHGMeEaTA", "https://mp.weixin.qq.com/s/P0A4tqP-tsiE-oWhLVecBw",
        "https://mp.weixin.qq.com/s/NDWP_0j6Tii8GU80fMjS3g", "https://mp.weixin.qq.com/s/KnJ6Eu5V9QUH6JqIyo1JQQ",
        "https://mp.weixin.qq.com/s/2SBS0pGz68fKpL4Ie1MBsQ", "https://mp.weixin.qq.com/s/2aDnXw7z2BwWY3tOLzjntg",
        "https://mp.weixin.qq.com/s/nGRSiVnt6r7ASRi_vWoo6w", "https://mp.weixin.qq.com/s/vO2bbnMRKmttZNIft6FvcQ",
        "https://mp.weixin.qq.com/s/Gp6M4--Tg_mJHsDoXh5YBg", "https://mp.weixin.qq.com/s/5UWyVZ7O57aVrYpfRLm0gQ",
        "https://mp.weixin.qq.com/s/WwTdQtA8eu-mCjrRZPBD1g", "https://mp.weixin.qq.com/s/uiuP7fjA53ljkph97Um_fQ",
        "https://mp.weixin.qq.com/s/-HhhJfz_y4dgp7y-vhDLQg", "https://mp.weixin.qq.com/s/dEdsWfA6s2X0pNeOtF5n8w",
        "https://mp.weixin.qq.com/s/1u93rwTGO-DwL0GptjqPZA", "https://mp.weixin.qq.com/s/6W2htWyFLI0DGrF9IAz8Ww",
        "https://mp.weixin.qq.com/s/jy-iUrcjY_7gWcmXYQEOYA", "https://mp.weixin.qq.com/s/cnlUeN2UPqHbV8y8AZGXRA",
        "https://mp.weixin.qq.com/s/_ybdDi1uRY0eucr6vcVRDQ", "https://mp.weixin.qq.com/s/MNuhoNHo5Ty1d8xXqeNMHQ",
        "https://mp.weixin.qq.com/s/Kugzb16JiCRRpLwXmX9oGg", "https://mp.weixin.qq.com/s/eBP8PyVyK-_l_Joo9IC2ew",
        "https://mp.weixin.qq.com/s/Z_ogPMCAwwf3uBBrtnodkg", "https://mp.weixin.qq.com/s/Y3eqmFhRyEpKOMWjsdmMNg",
        "https://mp.weixin.qq.com/s/AOUDvVZQn_JqOBDiCw9NMw", "https://mp.weixin.qq.com/s/yavOx43zjP_750Xa8GHSyg",
        "https://mp.weixin.qq.com/s/7bKbkrceTew5av16h6MOQA", "https://mp.weixin.qq.com/s/GajgzXG5cICgNBO12sId5w",
        "https://mp.weixin.qq.com/s/O0CKmEh9NvfUSCJHtLdE9w", "https://mp.weixin.qq.com/s/D_DhcvmT4FpHerMMqzvTcg",
        "https://mp.weixin.qq.com/s/6H-f-svoRA1chQwi69IsZA", "https://mp.weixin.qq.com/s/53sgod1x-q8rT0qnR_dpwQ",
        "https://mp.weixin.qq.com/s/wMzp6n1bUXELO30FHa0czA", "https://mp.weixin.qq.com/s/Skk9y0WlF_Cct1xTg6emdA",
        "https://mp.weixin.qq.com/s/I6hSXd6N-IPK9DNmG9ueIg", "https://mp.weixin.qq.com/s/QsslKRwaxTqEWjXmREWkdA",
        "https://mp.weixin.qq.com/s/rilcc8zo6hoJ2BWbE_H3qQ", "https://mp.weixin.qq.com/s/3Gc7pILwBoCwwDIKgGqwlQ",
        "https://mp.weixin.qq.com/s/aRp4hrVAGcxZimCqoTgO3w", "https://mp.weixin.qq.com/s/BoG8o1gHozthcCngXl6_gg",
        "https://mp.weixin.qq.com/s/6wmCURcoeged5Ek-i4TX7A", "https://mp.weixin.qq.com/s/yZ6BTlsZMYa04BVngKekcA",
        "https://mp.weixin.qq.com/s/pgzZwcWnR-CSsQVRmKWZhw", "https://mp.weixin.qq.com/s/fx6pKZbpR7zHf_l-5DCgwQ"]

tag= ["舞蹈 艺术 表演 形体训练",
       "文学 写作 阅读 创意",
       "造型 时尚 形象设计",
       "校友交流 职业发展 社交 资源共享",
       "Linux 编程 技术交流 开源",
       "创业 商业 资源共享",
       "公益 志愿 社会实践",
       "铁路 交通 历史 旅行",
       "湖南 地域文化",
       "创业 公益实践",
       "广西 地域文化",
       "电影  文化交流",
       "东南亚 地域文化",
       "量化 风险管理 金融投资 职业发展",
       "翻译 外语 语言 文化交流",
       "汉服 文化交流 历史",
       "道学 哲学 文化研究 传统文化",
       "曲艺 传统艺术 文化交流",
       "文学 阅读 农业文化 传统文化",
       "辩论 语言艺术", "上海 地域文化",
       "教育 支教 公益实践",
       "湖北 地域文化",
       "开源 编程 软件开发",
       "科幻 文学 创意写作",
       "动物保护 公益 流浪猫",
       "环保 自然保护 公益 观鸟",
       "国际关系 模拟联合国 政治",
       "魔方 益智游戏 逻辑思维 娱乐",
       "魔术 表演艺术 娱乐",
       "民俗 传统文化",
       "儒学 传统文化 哲学",
       "中国音乐 传统文化 艺术交流",
       "书法 绘画 传统文化 艺术交流 文化交流",
       "武侠 文化研究 传统文化 文学交流",
       "公益 社会服务 志愿者 急救",
       "智库 青年发展 社会研究 政策分析",
       "脱口秀 喜剧 娱乐", "创意 设计 手工",
       "山西 地域文化", "碳中和 可持续发展 生态",
       "手风琴 音乐 乐器 艺术交流",
       "桌游 逻辑训练 娱乐",
       "台湾研究 两岸关系 文化交流 政策分析",
       "提琴 古典音乐 乐器 艺术交流",
       "钢琴 古典音乐 乐器 艺术交流",
       "推理 逻辑思维", "人工智能 编程 机器学习",
       "文学 文学交流 阅读", "电影 艺术 数字媒体",
       "医学 人文", "信用经济 政策分析 金融诚信",
       "政治 亚洲研究 模拟外交", "心理咨询 心理健康 社交",
       "音乐 作曲编曲 跨媒介艺术", "音乐剧 舞台戏剧 声乐表演 文化交流", "美食 厨艺 饮食",
       "二次元 动漫 原神", "口琴 蓝调音乐 乐器 音乐", "易学 哲学 传统文化", "禅学 传统文化 哲学",
       "艺术 当代绘画 创意", "中医 医学 传统文化", " 跨文化对话 文化交流", "摄影 视觉叙事",
       "红楼梦 古典文学 文化交流", "围棋 智力运动", "越剧 地方戏曲 传统文化", "黄梅戏 地方戏曲 传统文化",
       "江苏 地域文化", "江西 地域文化", "象棋 智力运动", "龙舟 团队协作", "武术 体能训练",
       "京剧 昆曲 地方戏曲 传统文化", "街舞  潮流文化 舞蹈", "话剧表演 剧本创作 舞台美术",
       "地板球 小球运动 团队竞技", "射箭 传统弓术 运动", "影片创作 影视工业 电影",
       "飞盘 户外运动 团队竞技 运动", "橄榄球 团队竞技 团队凝聚力 运动", "高尔夫 商务社交 运动 绅士运动",
       "滑板 街头文化 潮流文化", "高山滑雪  滑雪 冬季运动 运动", "击剑 运动", "剑道 日本武道",
       "健身健美 体态管理 力量训练", "篮球 团队竞技 运动", "轮滑 运动", "排球 团队竞技",
       "天文 天文观测 星空摄影", "乒乓球 小球运动 运动", "柔道 日本武道", "赛艇 水上运动 团队竞技 运动",
       "散打 格斗竞技", "登山 攀岩 户外生存", "户外生存 团队竞技 体能", "台球  绅士运动 运动",
       "跆拳道 韩国武道", "徒步探险 徒步", "空手道 日本武道",
       "游泳 水上运动 体能 运动 塑形", "跑步 运动 马拉松", "公路骑行 自行车 骑行", "足球 团队竞技 运动",
       "棒球 垒球 团队竞技 运动", "综合格斗 体能", "浙江 地域文化", "韩国文化 国际交流", "日本文化 国际交流",
       "风险投资 创业", "葡萄酒 饮食", "太极拳 ", "短兵器 武术 运动", "保龄球 室内运动 休闲竞技",
       "论文写作 学术", "公益 社会创新", "羽毛球 小球运动 运动", "配音 影视"]

tag0 = ["舞蹈 艺术 表演 形体训练",
       "文学 写作 阅读 创意",
       "造型 时尚 形象设计",
       "校友交流 职业发展 社交 资源共享",
       "Linux 编程 技术交流 开源",
       "创业 商业 资源共享",
       "公益 志愿 社会实践",
       "铁路 交通 历史 旅行",
       "湖南 地域文化",
       "创业 公益实践",
       "广西 地域文化",
       "电影  文化交流",
       "东南亚 地域文化",
       "量化 风险管理 金融投资 职业发展",
       "翻译 外语 语言 文化交流",
       "汉服 文化交流 历史",
       "道学 哲学 文化研究 传统文化",
       "曲艺 传统艺术 文化交流",
       "文学 阅读 农业文化 传统文化",
       "辩论 语言艺术", "上海 地域文化",
       "教育 支教 公益实践",
       "湖北 地域文化",
       "开源 编程 软件开发",
       "科幻 文学 创意写作",
       "动物保护 公益 流浪猫",
       "环保 自然保护 公益 观鸟",
       "国际关系 模拟联合国 政治",
       "魔方 益智游戏 逻辑思维 娱乐",
       "魔术 表演艺术 娱乐",
       "民俗 传统文化",
       "儒学 传统文化 哲学",
       "中国音乐 传统文化 艺术交流",
       "书法 绘画 传统文化 艺术交流 文化交流",
       "武侠 文化研究 传统文化 文学交流",
       "公益 社会服务 志愿者 急救",
       "智库 青年发展 社会研究 政策分析",
       "脱口秀 喜剧 娱乐", "创意 设计 手工",
       "山西 地域文化", "碳中和 可持续发展 生态",
       "手风琴 音乐 乐器 艺术交流",
       "桌游 逻辑训练 娱乐",
       "台湾研究 两岸关系 文化交流 政策分析",
       "提琴 古典音乐 乐器 艺术交流",
       "钢琴 古典音乐 乐器 艺术交流",
       "推理 逻辑思维", "人工智能 编程 机器学习",
       "文学 文学交流 阅读", "电影 艺术 数字媒体",
       "医学 人文", "信用经济 政策分析 金融诚信",
       "政治 亚洲研究 模拟外交", "心理咨询 心理健康 社交",
       "音乐 作曲编曲 跨媒介艺术", "音乐剧 舞台戏剧 声乐表演 文化交流", "美食 厨艺 饮食",
       "二次元 动漫 原神", "口琴 蓝调音乐 乐器 音乐", "易学 哲学 传统文化", "禅学 传统文化 哲学",
       "艺术 当代绘画 创意", "中医 医学 传统文化", " 跨文化对话 文化交流", "摄影 视觉叙事",
       "红楼梦 古典文学 文化交流", "围棋 智力运动", "越剧 地方戏曲 传统文化", "黄梅戏 地方戏曲 传统文化",
       "江苏 地域文化", "江西 地域文化", "象棋 智力运动", "龙舟 团队协作", "武术 体能训练",
       "京剧 昆曲 地方戏曲 传统文化", "街舞  潮流文化 舞蹈", "话剧表演 剧本创作 舞台美术",
       "地板球 小球运动 团队竞技", "射箭 传统弓术 运动", "影片创作 影视工业 电影",
       "飞盘 户外运动 团队竞技 运动", "橄榄球 团队竞技 团队凝聚力 运动", "高尔夫 商务社交 运动 绅士运动",
       "滑板 街头文化 潮流文化", "高山滑雪  滑雪 冬季运动 运动", "击剑 运动", "剑道 日本武道",
       "健身健美 体态管理 力量训练", "篮球 团队竞技 运动", "轮滑 运动", "排球 团队竞技",
       "天文 天文观测 星空摄影", "乒乓球 小球运动 运动", "柔道 日本武道", "赛艇 水上运动 团队竞技 运动",
       "散打 格斗竞技", "登山 攀岩 户外生存", "户外生存 团队竞技 体能", "台球  绅士运动 运动",
       "跆拳道 韩国武道", "徒步探险 徒步", "空手道 日本武道",
       "游泳 水上运动 体能 运动 塑形", "跑步 运动 马拉松", "公路骑行 自行车 骑行", "足球 团队竞技 运动",
       "棒球 垒球 团队竞技 运动", "综合格斗 体能", "浙江 地域文化", "韩国文化 国际交流", "日本文化 国际交流",
       "风险投资 创业", "葡萄酒 饮食", "太极拳 ", "短兵器 武术 运动", "保龄球 室内运动 休闲竞技",
       "论文写作 学术", "公益 社会创新", "羽毛球 小球运动 运动", "配音 影视"]

historyscore = [0] * 120

def load_his():
    with open("his.json", "r", encoding="utf-8") as f:
        Historyscore = json.load(f)
    return Historyscore
def save_his():
    file_name="his.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(historyscore, f, ensure_ascii=False, indent=4)
Historyscore = [0] * 120
def clear_his():
    file_name="his.json"    
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(Historyscore, f, ensure_ascii=False, indent=4)
    

def load_tag():
    with open("tag.json", "r", encoding="utf-8") as f:
        Tag = json.load(f)
    return Tag
def save_tag():
    file_name="tag.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(tag, f, ensure_ascii=False, indent=4)
def clear_tag():
    file_name="tag.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(tag0, f, ensure_ascii=False, indent=4)

class CLub:
    def __init__(self, i):
        tag=load_tag()
        self.Tag = tag[i]
        self.Link = link[i]
        load_his()
        self.Score = historyscore[i]*0.3
        self.Name = name[i]

    def __lt__(self, a):
        return self.Score > a.Score


def search(S):
    clubs = []
    s = S.split()
    for i in range(0, 120):
        clubs.append(CLub(i))
        for j in clubs[i].Tag.split():
            for k in s:
                if (j == k):
                    clubs[i].Score += 1
                    historyscore[i] += 1
                    save_his()
    clubs.sort()
    res = []
    for i in range(0, 5):
        if (clubs[i].Score != 0):
            res.append((clubs[i].Name, clubs[i].Score, clubs[i].Tag, clubs[i].Link))
    clubs = []
    return res

def pinyin_search(S):
    clubs=[]
    s=S.split()
    for i in range(0,120):
        clubs.append(CLub(i))    
        def check1(a,b):
            if len(a)!=len(b):
                return 0
            for i in range(len(a)):
                if a[i]!=b[i]:
                    return 0
            return 1                
        def check2(a,b):
            if len(a)!=len(b):
                return 0
            for i in range(len(a)):
                if a[i][0]!=b[i]:
                    return 0
            return 1
        for k in s:
            if(check1(pypinyin.lazy_pinyin(clubs[i].Name),pypinyin.lazy_pinyin(k))):
                clubs[i].Score+=1
                historyscore[i]+=1
                save_his()
            elif(check2(pypinyin.lazy_pinyin(clubs[i].Name),k)):
                clubs[i].Score+=1
                historyscore[i]+=1
                save_his()
            elif clubs[i].Name==k:
                clubs[i].Score+=1
                historyscore[i]+=1   
                save_his()
        for j in clubs[i].Tag.split():
            for k in s:
                if(check1(pypinyin.lazy_pinyin(j),pypinyin.lazy_pinyin(k))):
                    clubs[i].Score+=1
                    historyscore[i]+=1
                    save_his()
                elif(check2(pypinyin.lazy_pinyin(j),k)):
                    clubs[i].Score+=1
                    historyscore[i]+=1
                    save_his()
                elif j==k:
                    clubs[i].Score+=1
                    historyscore[i]+=1    
                    save_his()
    clubs.sort()
    res=[]
    for i in range(0,5):
        if(clubs[i].Score!=0):
            res.append((clubs[i].Name,clubs[i].Score,clubs[i].Tag,clubs[i].Link))
    clubs=[]
    return res

class memoryCLub:
    def __init__(self, i):
        tag=load_tag()
        self.Tag = tag[i]
        self.Link = link[i]
        historyscore=load_his()
        self.Score = historyscore[i]
        self.Name = name[i]

    def __lt__(self, a):
        return self.Score > a.Score


def memory():
    clubs = []
    for i in range(0, 120):
        clubs.append(memoryCLub(i))
    clubs.sort()
    res = []
    for i in range(0, 5):
        if (clubs[i].Score != 0):
            res.append((clubs[i].Name, clubs[i].Score, clubs[i].Tag, clubs[i].Link))
    clubs = []
    return res