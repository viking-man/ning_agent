from gpt_tts_config import *
import os
import soundfile as sf
import logging
from GPT_SoVITS.inference_webui import InferenceWebUI


class GptTTSProxy:

    def __init__(self):
        super().__init__()
        self.init_models()

    def init_models(self):
        self.GPT_model_path = GPT_MODEL_PATH
        self.SoVITS_model_path = SOVITS_MODEL_PATH

    def text_to_speech(text: str, lang: str, external: InferenceWebUI):
        # gpt微调权重
        external.change_gpt_weights(gpt_path=external.gpt_path)
        # sovits微调权重
        external.change_sovits_weights(sovits_path=external.sovits_path)
        # 生成wav
        synthesis_result = external.get_tts_wav(ref_wav_path=EXAMPLE_WAV,
                                                prompt_text=EXAMPLE_TEXT,
                                                # prompt_language=EXAMPLE_TEXT_LANG,
                                                text=text
                                                # text_language=lang
                                                )

        result_list = list(synthesis_result)

        if result_list:
            last_sampling_rate, last_audio_data = result_list[-1]
            output_wav_path = os.path.join(OUTPUT_WAV_PATH, "output.wav")
            sf.write(output_wav_path, last_audio_data, last_sampling_rate)

            result = "Audio saved to " + output_wav_path

        logging.info(f"合成完成！输出路径：{OUTPUT_WAV_PATH}")
        logging.info("处理结果：\n" + result)


if __name__ == "__main__":
    external = InferenceWebUI(
        "/Users/viking/ai/github/GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large",
        "/Users/viking/ai/github/GPT-SoVITS/GPT_SoVITS/pretrained_models/chinese-hubert-base",
        "/Users/viking/ai/github/GPT-SoVITS/GPT_weights/ningning-e15.ckpt",
        "/Users/viking/ai/github/GPT-SoVITS/SoVITS_weights/ningning_e8_s80.pth"
    )

    GptTTSProxy.text_to_speech("我是宁宁，我喜欢唱歌，我喜欢舞台", 'zh', external)

