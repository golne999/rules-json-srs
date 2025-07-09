#!/usr/bin/env python3
import yaml
import json
import requests

# YAML URL
yaml_url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/WeChat/WeChat.yaml"

# 下载 YAML
r = requests.get(yaml_url)
r.raise_for_status()
yaml_text = r.text

# 解析 YAML
data = yaml.safe_load(yaml_text)
payload = data.get("payload", [])

rules = []

for line in payload:
    if line.startswith("DOMAIN-SUFFIX,"):
        domain = line.split(",", 1)[1]
        rules.append({"domain_suffix": [domain]})
    elif line.startswith("DOMAIN-KEYWORD,"):
        keyword = line.split(",", 1)[1]
        rules.append({"domain_keyword": [keyword]})
    elif line.startswith("DOMAIN,"):
        domain = line.split(",", 1)[1]
        rules.append({"domain": [domain]})
    elif line.startswith("DOMAIN-REGEX,"):
        regex = line.split(",", 1)[1]
        rules.append({"domain_regex": [regex]})
    elif line.startswith("IP-CIDR,"):
        ip = line.split(",", 1)[1]
        ip = ip.split(",")[0]   # 去掉可能的 ,no-resolve
        rules.append({"ip_cidr": [ip]})
    else:
        print(f"未知条目：{line}")

# 构造 sing-box JSON
output = {
    "version": 3,
    "rules": rules
}

# 保存 JSON
with open("wechat.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ 已生成 wechat.json")
