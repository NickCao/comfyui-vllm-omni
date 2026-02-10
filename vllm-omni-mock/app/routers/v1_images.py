# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project
import time
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse

from app.internal.images import (
    ImageData,
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from app.internal.image_api_utils import parse_size
from app.internal.utils import random_image_base64

router = APIRouter()


@router.get("/health")
async def health(raw_request: Request) -> JSONResponse:
    return JSONResponse(content={"status": "healthy"})


@router.get("/v1/models")
async def show_available_models(raw_request: Request) -> JSONResponse:
    return JSONResponse(
        content={
            "object": "list",
            "data": [
                {
                    "id": "mock",
                    "object": "model",
                    "created": 0,
                    "owned_by": "vllm-omni",
                    "permission": [],
                }
            ],
        }
    )


@router.post(
    "/v1/images/generations",
    responses={
        HTTPStatus.OK.value: {"model": ImageGenerationResponse},
    },
)
async def generate_images(
    request: ImageGenerationRequest, raw_request: Request
) -> ImageGenerationResponse:
    width, height = 1024, 1024
    if request.size:
        width, height = parse_size(request.size)

    return ImageGenerationResponse(
        created=int(time.time()),
        data=[
            ImageData(b64_json=random_image_base64(width, height))
            for _ in range(request.n)
        ],
    )


@router.post(
    "/v1/images/edits",
    responses={
        HTTPStatus.OK.value: {"model": ImageGenerationResponse},
    },
)
async def edit_images(
    raw_request: Request,
    image: list[UploadFile] | None = File(None),
    image_array: list[UploadFile] | None = File(None, alias="image[]"),
    url: list[str] | None = Form(None),
    url_array: list[str] | None = Form(None, alias="url[]"),
    prompt: str = Form(...),
    model: str = Form(None),
    n: int = Form(1),
    size: str = Form("auto"),
    response_format: str = Form("b64_json"),
    output_format: str | None = Form("png"),
    background: str | None = Form("auto"),
    output_compression: Annotated[int, Form(ge=0, le=100)] = 100,
    user: str | None = Form(None),  # unused now
    # vllm-omni extensions for diffusion control
    negative_prompt: str | None = Form(None),
    num_inference_steps: int | None = Form(None),
    guidance_scale: float | None = Form(None),
    true_cfg_scale: float | None = Form(None),
    seed: int | None = Form(None),
    generator_device: str | None = Form(None),
    # vllm-omni extension for per-request LoRA.
    lora: str | None = Form(None),  # Json string
) -> ImageGenerationResponse:
    width, height = 1024, 1024
    if size != "auto":
        width, height = parse_size(size)

    return ImageGenerationResponse(
        created=int(time.time()),
        data=[
            ImageData(b64_json=random_image_base64(width, height))
            for _ in range(
                len(image or image_array or []) + len(url or url_array or [])
            )
        ],
        output_format=output_format,
        size=f"{width}x{height}",
    )
