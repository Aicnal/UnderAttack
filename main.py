import time
import os
from cf import get_domain, under_attack, back_normal, api_key, api_email, zone_id
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="main.log",  # 日志输出到文件
)

# 添加一个 StreamHandler 将日志输出到终端
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

# 获取用户设置阈值，带有默认值
threshold = int(os.environ.get("threshold", 80)) # 挨打开启的阈值
recover_threshold = int(os.environ.get("recover_threshold", 30))  # 恢复模式的CPU阈值
high_durations = int(os.environ.get("high_duration", 10)) * 60 # 持续高占用多长时间触发
low_usage_duration = int(os.environ.get("low_usage_duration", 30)) * 60 # 降低多长时间后降低

if not all([api_email, api_key, zone_id]):
    logging.error("请检查有关Cloudflare环境变量是否正确填写")
    exit(1)

start_time = None
low_usage_start_time = None
recover_start_time = None
under_attack_mode = False  # 是否在防护模式中

try:
    logging.info('当前设置域名为：')
    get_domain()
except Exception as e:
    logging.error(f"获取域名失败: {e}")

def get_host_cpu_usage():
    def read_cpu_times():
        try:
            with open('/host_proc/stat') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('cpu '):
                        cpu_times = line.split()[1:]
                        return [int(x) for x in cpu_times]
            return None
        except FileNotFoundError:
            logging.error("Host CPU information not available.")
            return None

    try:
        cpu_times1 = read_cpu_times()
        if not cpu_times1:
            return 0
        time.sleep(1)
        cpu_times2 = read_cpu_times()
        if not cpu_times2:
            return 0

        idle_time1, idle_time2 = cpu_times1[3], cpu_times2[3]
        total_time1, total_time2 = sum(cpu_times1), sum(cpu_times2)
        idle_delta = idle_time2 - idle_time1
        total_delta = total_time2 - total_time1
        return 100 * (1 - idle_delta / total_delta)
    except Exception as e:
        logging.error(f"Error calculating CPU usage: {e}")
        return 0

while True:
    cpu_usage = get_host_cpu_usage()
    logging.info("Host CPU Usage: {:.2f}%".format(cpu_usage))

    if under_attack_mode:
        # 在防护模式下，检测低于恢复阈值的时间
        if cpu_usage < recover_threshold:
            if recover_start_time is None:
                recover_start_time = time.time()
            elif time.time() - recover_start_time >= low_usage_duration:
                logging.info("CPU usage has been below {}% for 30 minutes. Disabling Under Attack mode.".format(recover_threshold))
                try:
                    back_normal()
                    under_attack_mode = False
                    recover_start_time = None
                except Exception as e:
                    logging.error(f"关闭防护模式失败: {e}")
        else:
            recover_start_time = None  # 如果CPU高于恢复阈值，重置恢复计时器
    else:
        # 在非防护模式下，检测高负载
        if cpu_usage > threshold:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= high_durations:
                logging.info("CPU usage has been above {}% for {} minutes. Enabling Under Attack mode.".format(threshold, high_durations // 60))
                try:
                    under_attack()
                    under_attack_mode = True
                except Exception as e:
                    logging.error(f"开启防护模式失败: {e}")
                start_time = None
            low_usage_start_time = None
        else:
            start_time = None
            if low_usage_start_time is None:
                low_usage_start_time = time.time()
            elif time.time() - low_usage_start_time >= low_usage_duration:
                logging.info("CPU usage has been below {}% for 30 minutes.".format(threshold))
                low_usage_start_time = None

    time.sleep(1)