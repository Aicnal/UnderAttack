# UnderAttack
Automatically enable Cloudflare's "I'm Under Attack" mode to mitigate DDoS attacks.

自动帮你开启 Cloudflare "I'm Under Attack" 模式来缓解 DDoS 攻击。

## How It Works? 如何运作？
This tool monitors system CPU usage. If the CPU usage exceeds a specified threshold within a short period—by default, 80% for 5 minutes (configurable in the `.env` file)—it will use the Cloudflare API to enable the "I'm Under Attack" mode. Once the attack subsides and CPU usage returns to normal, the tool will revert the mode to normal.

该工具通过监控系统 CPU 使用率来判断是否触发攻击模式。如果 CPU 使用率在短时间内超过指定阈值（默认 80%，持续 5 分钟，可在 .env 文件中配置），工具会调用 Cloudflare API 自动开启 "I'm Under Attack" 模式。 一旦攻击结束，CPU 使用率恢复正常，工具会将模式切换回正常状态。

## How To Use? 如何使用？
UnderAttack relies on the Cloudflare API. You need to configure the required environment variables, including api_email, api_key, and zone_id. Additionally, you can customize settings such as `threshold`, `recover_threshold`, `high_duration`, and `low_usage_duration`. If these variables are not set, the tool will use default values.

UnderAttack 依赖 Cloudflare API。你需要配置必要的环境变量，包括 api_email、api_key 和 zone_id。你在 `.env` 自定义以下阈值，`threshold`：触发阈值，`recover_threshold`：恢复阈值，`high_duration`：持续高占用多少时间触发，`low_usage_duration`：持续低占用多长时间回到普通模式

### Example `.env` File `.env` 文件示例
```.env
threshold=80
recover_threshold=30
high_duration=10
low_usage_duration=30
api_email=your_email@example.com
api_key=your_cloudflare_api_key
zone_id=your_cloudflare_zone_id
```

### Example `docker-compose.yml` File `docker-compose.yml` 文件示例
```yml
services:
  attack:
    image: aicnal/underattack:latest
    environment:
      - threshold
      - recover_threshold
      - high_duration
      - low_usage_duration
      - api_email
      - api_key
      - zone_id
    restart: unless-stopped
    volumes:
      - /proc:/host_proc:ro
```

With these configurations, you can seamlessly deploy UnderAttack to monitor and mitigate potential DDoS attacks on your system.

配置完成后，你可以无缝部署 UnderAttack，对系统进行实时监控，及时缓解潜在的 DDoS 攻击。