import os
import ruamel.yaml

config_path = r"C:\Users\haqua\AppData\Local\hermes\config.yaml"

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

with open(config_path, "r", encoding="utf-8") as f:
    cfg = yaml.load(f)

desired_models = [
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.5",
    "gpt-5.4-mini",
    "kimi-k2.7-code",
    "kimi-k2.6",
    "glm-5.2",
    "glm-5.1"
]

# Update custom_providers
custom = cfg.get("custom_providers", [])
for p in custom:
    if p.get("name") == "jeniya":
        p["models"] = desired_models
        break
cfg["custom_providers"] = custom

# Update default model if it's currently deepseek
if cfg.get("model", {}).get("default") == "deepseek-v4-pro":
    cfg["model"]["default"] = "gpt-5.6-luna"

with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(cfg, f)

print("Hermes models filtered for Jeniya provider!")
