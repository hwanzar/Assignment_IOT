from datetime import datetime, timedelta

def add_seconds_to_time(time_str, seconds):
    # Chuyển đổi thời gian từ chuỗi thành đối tượng datetime
    time_format = "%H:%M"
    time_obj = datetime.strptime(time_str, time_format)

    # Tạo một đối tượng timedelta để thêm số giây
    delta = timedelta(seconds=seconds)

    # Thêm số giây vào thời gian
    new_time_obj = time_obj + delta

    # Chuyển đổi đối tượng datetime thành chuỗi và trả về
    return new_time_obj.strftime(time_format)

# Sử dụng hàm
input_time = "12:30"
seconds_to_add = 3600  # Ví dụ: cộng thêm 3600 giây (một giờ)
new_time = add_seconds_to_time(input_time, seconds_to_add)
print(type(new_time))
print("Thời gian sau khi cộng thêm {} giây là: {}".format(seconds_to_add, new_time))
