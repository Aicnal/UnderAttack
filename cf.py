import os
from cloudflare import Cloudflare
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="cloudflare_control.log",  # 日志输出到文件
)

# 通过环境变量获取 Cloudflare API 的邮箱、密钥和域名 ID
api_email = os.getenv("api_email")
api_key = os.getenv("api_key")
zone_id = os.getenv("zone_id")

# 初始化 Cloudflare 客户端
client = Cloudflare(api_email=api_email, api_key=api_key)


# 获取域名
def get_domain():
    try:
        zone = client.zones.get(zone_id=zone_id)
        logging.info(f"成功获取域名: {zone.name}")
        return zone.name
    except Exception as e:
        logging.error(f"获取域名失败: {e}")
        return None


# 获取安全等级
def get_security_level():
    try:
        settings = client.zones.settings.get(zone_id=zone_id, setting_id="security_level")
        logging.info(f"当前安全等级: {settings.value}")
        return settings.value
    except Exception as e:
        logging.error(f"获取安全等级失败: {e}")
        return None


# 切换至挨打模式 (Under Attack)
def under_attack():
    try:
        attack = client.zones.settings.edit(
            zone_id=zone_id,
            setting_id="security_level",
            id="security_level",
            value="under_attack",
        )
        logging.warning("已切换至挨打模式")
        return attack.value
    except Exception as e:
        logging.error(f"切换至挨打模式失败: {e}")
        return None


# 切换回正常模式 (High)
def back_normal():
    try:
        normal = client.zones.settings.edit(
            zone_id=zone_id,
            setting_id="security_level",
            id="security_level",
            value="high",  # 切换到“高”安全等级
        )
        logging.info("已切换至正常模式")
        return normal.value
    except Exception as e:
        logging.error(f"切换回正常模式失败: {e}")
        return None

# # 主函数：切换逻辑
# if __name__ == "__main__":
#     domain = get_domain()
#     if domain:
#         logging.info(f"正在处理域名: {domain}")
#
#         current_level = get_security_level()
#         if current_level == "under_attack":
#             logging.info("域名当前处于挨打模式，尝试切换回正常模式...")
#             back_normal()
#         else:
#             logging.info("域名处于正常模式，尝试切换至挨打模式...")
#             under_attack()
