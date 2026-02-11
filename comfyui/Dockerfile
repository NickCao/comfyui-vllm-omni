FROM docker.io/yanwk/comfyui-boot:cpu
RUN PIP_USER=true pip install kubernetes
RUN git clone --depth 1 --branch knative https://github.com/NickCao/vllm-omni /root/src/vllm-omni
RUN cp -r /root/src/vllm-omni/apps/ComfyUI-vLLM-Omni /default-comfyui-bundle/ComfyUI/custom_nodes/ComfyUI-vLLM-Omni
