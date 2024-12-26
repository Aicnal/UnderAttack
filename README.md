# UnderAttack

Automatically enable Cloudflare's "I'm Under Attack" mode to mitigate DDoS attacks.

## How It Works?

This tool monitors system CPU usage. If the CPU usage exceeds a specified threshold within a short period—by default, 80% for 5 minutes (configurable in the `.env` file)—it will use the Cloudflare API to enable the "I'm Under Attack" mode. Once the attack subsides and CPU usage returns to normal, the tool will revert the mode to normal.
## How To Use?

UnderAttack relies on the Cloudflare API. You need to configure the required environment variables, including api_email, api_key, and zone_id. Additionally, you can customize settings such as `threshold`, `recover_threshold`, `high_duration`, and `low_usage_duration`. If these variables are not set, the tool will use default values.
### Example `.env` File

```.env
threshold=80
recover_threshold=30
high_duration=10
low_usage_duration=30
api_email=your_email@example.com
api_key=your_cloudflare_api_key
zone_id=your_cloudflare_zone_id
```

### Example `docker-compose.yml` File

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
      - /var/run/docker.sock:/var/run/docker.sock
```

With these configurations, you can seamlessly deploy UnderAttack to monitor and mitigate potential DDoS attacks on your system.