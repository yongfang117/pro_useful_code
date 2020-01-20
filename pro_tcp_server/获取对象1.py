data={"command": "device",
 "response": {
     "devices":
         [
             "device_test",
             "device_01",
             "device_02"
         ],
     "errors":
         [
             {
                 "device_name": "device_01",
                 "errs":
                     [
                         {
                             "err_no": 0,
                             "err_info": "成功"
                         }, {
                         "err_no": 1,
                         "err_info": "失败"
                     }
                     ]
             },
             {
                 "device_name": "device_02",
                 "errs":
                     [
                         {
                             "err_no": 3,
                             "err_info": "成功"
                         }, {
                         "err_no": 4,
                         "err_info": "失败"
                     }
                     ]
             }

         ]
 }
 }


def return_err_info(device_name,err_no):
    # device_name = "device_01"  # 假设传过来为device_01
    # err_no = 0   # 假设传过来为err_no=0
    err_info = None
    errors_obj = data["response"]["errors"]
    if device_name in data["response"]["devices"]:
        for i in errors_obj:
            if i["device_name"] == device_name:
                err_no_device = i["errs"]
                for ii in err_no_device:
                    if ii["err_no"] == err_no:
                        err_info = ii["err_info"]
                        return err_info
# device_name = "device_01"  # 假设传过来为device_01
# err_no = 0
r=return_err_info("device_01",0)
print(r)

# ------
# 方法2:s使用列表推导式
# data = DEVICE_LIST_INFO["device_list_info"]
#     errors_obj = data["response"]["errors"]
# if device_name in data["response"]["devices"]:
    #     device_name_error_list = [device.get("device_name", None) for device in errors_obj]
    #     if device_name in device_name_error_list:
    #         err_info = [ii["err_info"] for ii in
    #                     [
    #                         i["errs"] for i in errors_obj if i["device_name"] == device_name
    #                     ][0] if ii["err_no"] == err_no
    #                     ]  # 如果err_no存在返回的err_info为含有一个对象的列表,否则返回空列表
    #         err_info = err_info[0] if err_info else None
    #         return err_info
    #
    # return '成功' if err_no == 0 else None