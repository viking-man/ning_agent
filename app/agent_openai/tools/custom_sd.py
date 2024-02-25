
from diffusers import StableDiffusionPipeline,DPMSolverMultistepScheduler
from agent_openai.agent.agent_config import STABLE_DIFFUSION_MODEL_PATH

class CustomStableDiffusion:
    
    
    def __init__(self) -> None:
        self.pipeline = StableDiffusionPipeline.from_single_file(STABLE_DIFFUSION_MODEL_PATH)
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(self.pipeline.scheduler.config)
        self.pipeline.safety_checker = None
        self.pipeline.requires_safety_checker = False
        self.pipeline = self.pipeline.to("cuda")
    
    '''提供根据文本生成图片的能力，用户输入指令描述，该方法返回对应的图片输出'''
    '''Provide the ability to generate images based on text, the user inputs a description of the command, the method returns the corresponding image output'''
    def sculpture(self,prompt:str=""):
        image = self.pipeline(prompt).images[0]
        return image
    
# if __name__ == '__main__':
#     sd = CustomStableDiffusion()
#     image = sd.sculpture("A cat running down the street with a fish in his hand.")
#     image.save("test.png")