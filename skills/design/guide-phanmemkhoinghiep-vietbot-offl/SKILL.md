---
name: guide-phanmemkhoinghiep-vietbot-offl
description: '1.1. Luồng xử lý thông thường:'
---

### STEP1. Hiểu luồng xử lý

1.1. Luồng xử lý thông thường:

```sh
Callback_process: stt_process() => Text => Kiểm tra điều kiện thỏa mãn để xử lý các lệnh cơ bản nhất => Nếu không thỏa mãn => Gọi text_process xử lý tiếp

Text_process: Kiểm tra điều kiện thỏa mãn để xử lý các skill cơ bản => Gọi skill_process với các def xử lý từng skill như(hỏi giờ, thời tiết theo khu vực trong config, lịch âm, hass, nghe nhạc offline) trả về text hoặc link, => Nếu không thỏa mãn gọi kết thúc
```
1.2. Luồng xử lý với custom skill:

```sh

Callback_process: stt_process() => Text => Kiểm tra điều kiện thỏa mãn để xử lý các lệnh cơ bản nhất => Nếu không thỏa mãn => Gọi text_process xử lý tiếp

Text_process: Kiểm tra điều kiện thỏa mãn để xử lý các skill cơ bản => Gọi skill_process với các def xử lý từng skill như(hỏi giờ, thời tiết theo khu vực trong config, lịch âm, hass, nghe nhạc offline) trả về text hoặc link, => Nếu không thỏa mãn gọi custom_skill_process

Custom_skill_process: Kiểm tra các điều kiện tùy chọn để gọi các def xử lý từng skill bổ sung trả về text hoặc link, => Nếu không thỏa mãn gọi kết thúc

```
Trong ví dụ này, sẽ tạo 2 custom skill, 1 là skill hỏi ngày này năm xưa và 1 skill sử dụng AI bot Dify, luồng xử lý sẽ như sau:

```sh

Custom_skill_process: Kiểm tra data thỏa mãn điều kiện để gọi skill kỉ niệm ngày này năm xưa, nếu không thỏa mãn thì gọi skill sử dụng AI bot Dify để trả lời, như vậy skill AI bot Dify sẽ trả lời toàn bộ các câu hỏi không thỏa mãn tại các skill mặc định và các skill custom

```

### STEP2. Khai báo trong json

2.1. Chuyển user về level 2 bằng cách cập nhật config.json tại dòng 275

```sh
        "level": 2
```

2.2. Tạo file json chứa config của các skill

2.2.1. Lưu các thông số cần config trong file json, nếu lưu luôn trong các file config.json

Ví dụ nếu khai các tham số config của các skill trong config.json:
```sh
	"today_history": {
		"url":"https://lichngaytot.com/ajax/NgayNayNamXuaAjax""
	},
        "dify": {
            "api_key": "app-qVedgdfg7kO",
			      "url":"https://api.dify.ai/v1/chat-messages",
			      "error":"Lỗi xử lý từ AI chatbot",
			      "no_answer":"Không có trả lời từ AI chatbot"
        }
```
2.2.2. Tạo và lưu điều kiện để kiểm tra skill ngày này năm xưa trong file object.json

```sh
    "history": [{
            "value": "lịch sử"
        },
        {
            "value": "năm xưa"
        }
    ],
```
Có nghĩa là, nếu data trả về def custom_skill_process mà có chứa từ "lịch sử" hoặc "năm xưa" thì sẽ gọi skill history_process

2.2. Khai báo các biến dạng hằng số trong global_constants.py

Ví dụ, các biến của Skill Today_history và diffy được khai báo tại đây

```sh
#Today History Skill
today_history_url=config_data['smart_skill']['today_history']['url']

#Dify Skill
dify_api_key=config_data['smart_skill']['dify']['api_key']
dify_url=config_data['smart_skill']['dify']['url']
dify_error=config_data['smart_skill']['dify']['error']
dify_no_answer=config_data['smart_skill']['dify']['no_answer']
```

2.3. Khai báo các biến dạng biến toàn cục trong global_vars.py (Nếu cần)

Sử dụng biến toàn cục, nếu muốn đọc hoặc chỉnh sửa biến này từ nhiều script tạo thêm, hoặc qua đường API

### STEP3. Code def xử lý

Trong script custom_skill_process.py tạo các def xử lý data và trả về text hoặc text và link

3.1. Code def xử lý

Cài đặt lib bs4 từ môi trường env
```sh
        pip install bs4
```

Ví dụ def today_history_process
```sh
def today_history_process(opt):
    try:

        # Using a dictionary to map the options to their corresponding functions
        date_map = {
            'YESTERDAY': get_current_date()[0],
            'TODAY': get_current_date()[1],
            'TOMORROW': get_current_date()[2],
            'NEXT_DAY': get_current_date()[3],
            'NEXT_WEEK': get_current_date()[4]  # adding an option for the 5th date
        }
        selected_date = date_map.get(opt)
        if not selected_date:
            return None
        payload = {
            'ngayxem': f"{selected_date.day:02d}-{selected_date.month:02d}-{selected_date.year}"
        }
        response = requests.post(global_constants.today_history_url, headers=today_hisotry_headers, data=payload)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        return clean_content(soup.get_text())
    except Exception as e:
        print_out('left',f"Lỗi xử lý Today_history Skill: {str(e)}",'red')
        return 'Không có câu trả lời từ skill của vietbot trong tình huống này'
```

Ví dụ def dify_process
```sh
def dify_process(data):
    request_json = {
        "inputs": {},
        "query": data,
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "abc-123",
        "files": []
    }
    try:
        response = requests.post(global_constants.dify_url, headers=dify_headers, json=request_json, stream=True)
        if response.status_code != 200:
            raise ValueError(f"HTTP Error: {response.status_code} - {response.text}")

        for line in response.iter_lines(decode_unicode=True):
            if line.strip():  # Kiểm tra dòng không rỗng
                if line.startswith("data: "):
                    line = line[6:]  # Loại bỏ tiền tố "data: "
                try:
                    response_data = json.loads(line)  # Parse JSON
                    data_section = response_data.get("data", global_constants.dify_no_answer)
                    if not data_section:
                        continue
                    inputs_section = data_section.get("inputs", global_constants.dify_no_answer)
                    if not inputs_section:
                        continue
                    context_value = inputs_section.get("#context#", global_constants.dify_no_answer)
                    if context_value:
                        # Chỉ lấy dòng đầu tiên
                        first_line = context_value.split("\n")[0].strip()
                        return first_line
                except json.JSONDecodeError:
                    # Bỏ qua lỗi JSON cho các dòng không hợp lệ
                    continue
        # Nếu không tìm thấy giá trị
        return global_constants.dify_no_answer
    except Exception as e:
        print_out('left',f"Lỗi xử lý Dify Skill: {str(e)}",'red')
        return global_constants.dify_no_answer
```


3.2. Lập trình để hàm def custom_skill_process gọi tiếp def xử lý data và trả về kết quả của hàm def xử lý data

Ví dụ def custom_skill_process
```sh
def custom_skill_process(data):
    answer='Không có câu trả lời từ skill của vietbot trong tình huống này'
    if any(item in data for item in global_constant.obj_history):
        if any(item in data for item in global_constant.obj_yesterday):
            answer=today_history_process('YESTERDAY')
        elif any(item in data for item in global_constant.obj_today):
            answer=today_history_process('TODAY')
        elif any(item in data for item in global_constant.obj_tomorrow):
            answer=today_history_process('TOMORROW')
        elif any(item in data for item in global_constant.obj_next_day):
            answer=today_history_process('NEXT_DAY')
        elif any(item in data for item in global_constant.obj_next_week):
            answer=today_history_process('NEXT_WEEK')
    else:
        answer=dify_process(data)
    return answer
```
