import logging

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, StableDiffusionImg2ImgPipeline
from app.agent_openai.agent.agent_config import STABLE_DIFFUSION_MODEL_PATH
from langchain.agents import tool
from torch import torch
import time
from app.common.utils import string_utils
from translatepy import Translate
from PIL import Image
from pathlib import Path


class CustomImg2ImgStableDiffusion:

    def __init__(self):
        self.pipe = StableDiffusionImg2ImgPipeline.from_single_file(STABLE_DIFFUSION_MODEL_PATH)
        self.pipe = self.pipe.to(
            "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

    def img2img(self, image_input_path, prompt):
        try:
            init_image = Image.open(image_input_path).convert("RGB")
            init_image = init_image.resize((768, 512))
        except IOError as e:
            logging.info(f"Error opening image: {e}")
            raise Exception(e)

        images = self.pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images

        image_input_path = Path(image_input_path)
        stem = image_input_path.stem
        suffix = image_input_path.suffix
        output_path = image_input_path.with_name(f"{stem}_sd{suffix}")
        images[0].save(output_path)
        return output_path


class CustomStableDiffusion:

    def __init__(self) -> None:
        self.pipeline = StableDiffusionPipeline.from_single_file(STABLE_DIFFUSION_MODEL_PATH)
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
        # self.pipeline.safety_checker = None
        # self.pipeline.requires_safety_checker = False
        DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        self.pipeline = self.pipeline.to(DEVICE)


'''该方法用于用户绘画相关的需求，提供根据文本生成图片的能力，用户输入图片相关的指令描述，该方法返回对应的图片输出'''


def translate_text(image_text, target_language='zh-CN'):
    translator = Translate()
    translated_text = translator.translate(image_text, target_language).result
    return translated_text


@tool
def sculpture(prompt: str = ""):
    '''This method is used for user drawing-related needs, providing the ability to generate images based on the text, the user inputs a description of the image-related instructions, the method returns the corresponding image output'''

    if string_utils.contains_chinese(prompt):
        prompt = translate_text(prompt, target_language="en")

    image = CustomStableDiffusion().pipeline(prompt).images[0]

    image_file = str(Path("app/files/image",
                          "image_" + str(int(time.time())) + ".png").absolute())
    image.save(image_file)
    return image_file


if __name__ == '__main__':
    # image_file = sculpture("A cat standing on the ground,watching the star river over his head.")
    # print(image_file)
    diffusion = CustomImg2ImgStableDiffusion()
    diffusion.img2img(
        "/Users/viking/ai/develope/ning_agent/app/static/ning_wink.jpg",
        "Make the picture more dreamy")
