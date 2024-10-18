from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "api_path": "",
        "kwargs": {}
    },
    "tweaks":
        tweaks,
    "converter": {
        "use": "opencc",
        "kwargs": {}
    },
    "generator": [{
        "use": "rime",
        "kwargs": {
            "output": ""
        }
    }]
}
