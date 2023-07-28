import replicate
import os
from utitlities import DBUpdateARG, DBReadARG, DBRead, custom_round

# Initializing Tokens
os.environ["REPLICATE_API_TOKEN"] = str(DBRead("scribble", "API_KEY"))


def ScribbleAPI(image, prompt, userSession):
    result = {}
    try:
        output = replicate.run(
            "rossjillian/controlnet:795433b19458d0f4fa172a7ccf93178d2adb1cb8ab2ad6c8fdc33fdbcd49f477",
            input={
                "image": open(image, "rb"),
                "prompt": prompt,
                "structure": "scribble",
                "image_resolution": 256,
                "scheduler": "DDIM",
                "steps": 20,
                "scale": 9,
                "seed": 20,
                "negative_prompt": "Longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
                "low_threshold": 100,
                "high_threshold": 200,
            },
        )
        images_count = int(
            DBReadARG("user", "images_count", "email", userSession, result)
        )
        images_count += 1
        DBUpdateARG("user", "images_count", images_count, "email", userSession)
        return output, "", images_count
    except Exception as error:
        images_count = int(
            DBReadARG("user", "images_count", "email", userSession, result)
        )
        return "", error, images_count



