import json
import subprocess
import pickle
import torch



AMT_URL = "https://github.com/sony/hFT-Transformer/releases/download/ismir2023/checkpoint.zip"
DEFAULT_NAMES = {
    "amt_encoder": "models/params/amt_encoder.pth",
    "pc_encoder": "models/params/pc_encoder.pth",
    "decoder": "models/params/decoder.pth",
}

def main():
    subprocess.run(["wget", AMT_URL])
    subprocess.run(["unzip", "checkpoint.zip"], )

    set_config()
    save_amt()

    subprocess.run(["rm", "checkpoint.zip"])
    subprocess.run(["rm", "-r", "checkpoint"])


DATA_CONFIG_PATH = "models/hFT_Transformer/config.json"
MODEL_CONFIG_PATH = "checkpoint/MAESTRO-V3/parameter.json"
CONFIG_PATH = "models/config.json"
def set_config():
    with open(DATA_CONFIG_PATH, "r") as f:
        config_data = json.load(f)
    config_data["input"]["min_value"] = 0

    with open(MODEL_CONFIG_PATH, "r") as f:
        config_model = json.load(f)

    config = {
        "data": config_data,
        "model": config_model,
        "default": DEFAULT_NAMES
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module.startswith("model"):
            module = module.replace("model", "models.hFT_Transformer", 1)
        return super().find_class(module, name)

AMT_PATH = "checkpoint/MAESTRO-V3/model_016_003.pkl"
def save_amt():
    with open(AMT_PATH, "rb") as f:
        model = CustomUnpickler(f).load()
    model.to("cpu")
    torch.save(model.encoder_spec2midi.state_dict(), DEFAULT_NAMES["amt_encoder"])
    torch.save(model.decoder_spec2midi.state_dict(), DEFAULT_NAMES["decoder"])


if __name__ == "__main__":
    main()