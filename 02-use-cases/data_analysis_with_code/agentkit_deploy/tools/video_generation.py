import os
import json
import logging
import time
from typing import List
import httpx
from rich.console import Console

LAS_REGION = os.getenv("LAS_REGION", os.getenv("TOS_REGION", "cn-beijing"))
LAS_OPERATOR_ID = os.getenv("LAS_OPERATOR_ID", "las_seedance")


def generate_video_from_images(
    image_urls: List[str],
    prompt: str = "",
    aspect_ratio: str = "16:9",
    duration_seconds: int = 5,
    fps: int = 24,
    resolution: str = "720p",
    watermark: bool = False,
) -> str:
    """
    将图像列表提交到 LAS AI（Seedance Operator）进行视频生成。
    返回 JSON 字符串，包含生成结果或错误信息。
    """
    console = Console()
    try:
        # 1. 数据准备阶段：校验输入、转换URL、构建请求内容
        las_api_key, content_items = _data_preparation(image_urls, console)
        
        # 2. 构造请求 Payload
        payload = _construct_payload(content_items)
        
        # 3. 发送创建任务请求
        task_id, headers = _create_task(payload, las_api_key, console)
        
        # 4. 轮询任务执行进度和获取结果
        return poll_task_result(task_id, headers, console)
    except Exception as e:
        console.print(f"[red]视频生成失败: {e}[/red]")
        return json.dumps({"error": str(e)}, ensure_ascii=False)



def _data_preparation(image_urls: List[str], console: Console) -> tuple:
    """
    数据准备阶段：
    1. 基础校验（image_urls 非空且为列表）
    2. 获取 TOOL_LAS_API_KEY 环境变量
    3. 转换 tos:// 协议的 URL 为 https://
    4. 构建 API 请求所需的 content_items
    
    返回值:
    - las_api_key: LAS 接口密钥
    - content_items: 转换后的图片 URL 列表
    """
    # 基础校验
    if not image_urls or not isinstance(image_urls, list):
        raise ValueError("image_urls 为空或类型错误")
    
    # 获取 LAS API 密钥
    las_api_key = os.getenv("TOOL_LAS_API_KEY")
    if not las_api_key:
        raise ValueError("缺少 TOOL_LAS_API_KEY，请在 settings.txt 或环境变量中配置")
    
    console.print(f"🎬 准备生成视频: OperatorId={LAS_OPERATOR_ID}, 区域={LAS_REGION}, 图像数={len(image_urls)}")
    
    # URL 转换函数
    def _convert_tos_url(url: str) -> str:
        url = str(url)
        if url.startswith("tos://"):
            rest = url[len("tos://"):]
            bucket, key = rest.split("/", 1)
            return f"https://{bucket}.tos-{LAS_REGION}.volces.com/{key}"
        return url
    
    # 构建 content_items
    content_items = []
    for u in image_urls:
        try:
            content_items.append({"type": "image_url", "image_url": {"url": _convert_tos_url(u)}})
        except Exception as e:
            console.print(f"[yellow]转换图片 URL 失败: {e}[/yellow]")
    
    return las_api_key, content_items



def _construct_payload(content_items: list) -> dict:
    """
    构造请求 Payload
    
    参数:
    - content_items: 转换后的图片 URL 列表
    
    返回值:
    - payload: 构建完成的 API 请求 Payload
    """
    return {
        "model_name": "doubao-seedance-1.0-lite-i2v",
        "content": content_items,
        "return_last_frame": False,
    }



def _create_task(payload: dict, las_api_key: str, console: Console) -> tuple:
    """
    发送创建任务请求
    
    参数:
    - payload: API 请求 Payload
    - las_api_key: LAS 接口密钥
    - console: Rich Console 实例，用于打印日志
    
    返回值:
    - task_id: 任务 ID
    - headers: 请求头（用于后续轮询）
    """
    # 直接调用 Seedance Online API
    gen_url = "https://operator.las.cn-beijing.volces.com/api/v1/online/video/generate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {las_api_key}",
    }
    
    console.print("🚀 已提交视频生成请求到 LAS Seedance Online …")
    
    with httpx.Client(timeout=60.0) as client:
        resp = client.post(gen_url, headers=headers, json=payload)
        console.print(f"HTTP Status(generate): {resp.status_code}")
        
        # 调试信息
        masked_headers = dict(headers)
        if masked_headers.get("Authorization"):
            masked_headers["Authorization"] = masked_headers["Authorization"][:20] + "..."
        console.print(f"[debug] POST {gen_url}")
        console.print(f"[debug] Headers: {masked_headers}")
        
        try:
            console.print("[debug] Payload(JSON):\n" + json.dumps(payload, ensure_ascii=False, indent=2))
        except Exception:
            console.print("[debug] Payload(JSON) 打印失败，改用字符串：" + str(payload))
        
        try:
            console.print(f"[debug] Response Headers(generate): {dict(resp.headers)}")
        except Exception:
            pass
        
        try:
            console.print(f"[debug] Response Text Length(generate): {len(resp.text)}")
            console.print(f"[debug] Response Text Preview(generate): {resp.text[:1200]}")
        except Exception:
            pass
        
        # 解析响应
        data = None
        try:
            data = resp.json()
            console.print(f"返回(JSON generate): {str(data)[:300]}")
        except Exception:
            console.print("返回非 JSON，改用文本输出。")
            data = {"text": resp.text}
        
        # 兼容不同字段命名
        task_id = (
            data.get("task_id")
            or data.get("taskId")
            or (data.get("data") or {}).get("task_id")
            or (data.get("data") or {}).get("id")
        )
        
        if not task_id:
            raise ValueError(f"未获取到 task_id: {str(data)[:200]}")
    
    return task_id, headers


def poll_task_result(task_id, headers, console):
    task_url = "https://operator.las.cn-beijing.volces.com/api/v1/online/video/task"
    console.print(f"⏳ 开始轮询任务状态 task_id={task_id}")
    start = time.time()
    deadline = start + float(os.getenv("SEEDANCE_POLL_TIMEOUT", "120"))
    interval = float(os.getenv("SEEDANCE_POLL_INTERVAL", "3"))
    last_data = None

    while time.time() < deadline:
        try:
            # 调试：打印 task 请求详情
            task_payload = {"task_id": task_id}
            masked_headers = dict(headers)
            try:
                if masked_headers.get("Authorization"):
                    masked_headers["Authorization"] = masked_headers["Authorization"][:20] + "..."
            except Exception:
                pass
            console.print(f"[debug] POST {task_url}")
            console.print(f"[debug] Headers(task): {masked_headers}")
            try:
                console.print("[debug] Payload(task JSON):\n" + json.dumps(task_payload, ensure_ascii=False, indent=2))
            except Exception:
                console.print("[debug] Payload(task) 打印失败：" + str(task_payload))

            with httpx.Client(timeout=300.0) as client:
                resp = client.post(task_url, headers=headers, json=task_payload)
                status = resp.status_code
                try:
                    console.print(f"[debug] Response Headers(task): {dict(resp.headers)}")
                except Exception:
                    pass
                try:
                    console.print(f"[debug] Response Text Length(task): {len(resp.text)}")
                    console.print(f"[debug] Response Text Preview(task): {resp.text[:1200]}")
                except Exception:
                    pass
                try:
                    data = resp.json()
                except Exception:
                    data = {"text": resp.text}
                last_data = data
                console.print(f"HTTP Status(task): {status} | {str(data)[:240]}")
                # 兼容字段判断
                state = (
                    data.get("status")
                    or (data.get("data") or {}).get("status")
                    or (data.get("result") or {}).get("status")
                )
                video_url = (
                    (data.get("result") or {}).get("url")
                    or (data.get("data") or {}).get("video_url")
                    or data.get("video_url")
                    or (data.get("data") or {}).get("content", {}).get("video_url")
                )
                if str(state).lower() in ("succeeded", "success", "completed", "done") or video_url:
                    console.print("✅ 视频生成完成。")
                    # 始终返回结构化 JSON，避免 Agent 误判而重复调用
                    result_obj = {
                        "status": "ok",
                        "task_status": str(state).lower() if state else "succeeded",
                        "video_url": video_url
                    }
                    try:
                        console.print("[debug] Final Result(JSON):\n" + json.dumps(result_obj, ensure_ascii=False, indent=2))
                    except Exception:
                        console.print("[debug] Final Result(JSON) 打印失败，改用字符串：" + str(result_obj))
                    return json.dumps(result_obj, ensure_ascii=False)
        except Exception as e:
            console.print(f"[yellow]轮询失败: {e}[/yellow]")
        time.sleep(interval)

    console.print("[red]轮询超时，返回最后一次响应。[/red]")
    timeout_obj = {
        "task_id": task_id,
        "status": "timeout",
        "video_url": None,
        "raw": last_data,
    }
    try:
        console.print("[debug] Final Result(JSON):\n" + json.dumps(timeout_obj, ensure_ascii=False, indent=2))
    except Exception:
        console.print("[debug] Final Result(JSON) 打印失败，改用字符串：" + str(timeout_obj))
    return json.dumps(timeout_obj, ensure_ascii=False)
