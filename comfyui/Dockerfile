FROM docker.io/yanwk/comfyui-boot:cpu
RUN git clone --depth 1 https://github.com/vllm-project/vllm-omni.git /root/src/vllm-omni
RUN cp -r /root/src/vllm-omni/apps/ComfyUI-vLLM-Omni /default-comfyui-bundle/ComfyUI/custom_nodes/ComfyUI-vLLM-Omni
