async def catch_video_id(response, future):
    if "personal" in response.url and response.request.method == "POST":
        try:
            json_body = await response.json()
            video_data = json_body.get("Resp", {}).get("data", [])
            if video_data and isinstance(video_data, list):
                video_id = video_data[0].get("video_id")
                print(f"Найден video_id: {video_id}")
                if not future.done():
                    future.set_result(video_id)
        except Exception as e:
            print(f"Ошибка разбора ответа: {e}")
