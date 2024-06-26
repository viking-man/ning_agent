from typing import Any, List, Dict, Mapping, Optional
import json

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.requests import TextRequestsWrapper
from langchain.llms.base import LLM
from langchain.chains import LLMChain
from langchain.llms import ChatGLM
from langchain.prompts import PromptTemplate
import torch
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline
from app.agent_llama.agent_config import LOCAL_MODEL_PATH


class CustomLLM(LLM):
    logging: bool = False
    output_keys: List[str] = ["output"]

    llm_type: str = "llama3"

    @property
    def _llm_type(self) -> str:
        return self.llm_type

    def log(self, log_str):
        if self.logging:
            print(log_str)
        else:
            return

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        self.log('----------' + self._llm_type + '----------> llm._call()')
        self.log(prompt)
        print(f"prompt{prompt}")

        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            LOCAL_MODEL_PATH, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto"
        )

        max_new_tokens = 256
        text_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            # max_length=max_length,
            max_new_tokens=max_new_tokens,
            # generation_config=generation_config,
        )

        llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})
        # question = "北京和上海两座城市有什么不同？"
        result = llm(prompt)

        if self._llm_type == "llama3":
            self.log('<--------chatglm------------')
            self.log(result)
            return result
        else:
            return "不支持该类型的 llm"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": 10}
