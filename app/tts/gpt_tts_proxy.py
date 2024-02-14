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
                                                prompt_language=EXAMPLE_TEXT_LANG,
                                                text=text,
                                                text_language=lang)

        result_list = list(synthesis_result)

        if result_list:
            last_sampling_rate, last_audio_data = result_list[-1]
            output_wav_path = os.path.join(OUTPUT_WAV_PATH, "output.wav")
            sf.write(output_wav_path, last_audio_data, last_sampling_rate)

            result = "Audio saved to " + output_wav_path

        logging.info(f"合成完成！输出路径：{OUTPUT_WAV_PATH}")
        logging.info("处理结果：\n" + result)


if __name__ == "__main__":
    external = InferenceWebUI("/Users/viking/ai/develope/ning_agent/external/pretrained_models/bert_path",
                              "/Users/viking/ai/develope/ning_agent/external/pretrained_models/cnhubert_base_path",
                              "/Users/viking/ai/develope/ning_agent/external/pretrained_models/gpt_weights",
                              "/Users/viking/ai/develope/ning_agent/external/pretrained_models/sovits_weights")
    GptTTSProxy.text_to_speech("我是宁宁，我喜欢唱歌", 'zh', external)
