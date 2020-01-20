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
device_name = "device_01"  # 假设传过来为device_01
err_no = 0   # 假设传过来为err_no=0
err_info = None
errors_obj = data["response"]["errors"]
if device_name in data["response"]["devices"]:
    for i in errors_obj:
        if i["device_name"] == device_name:
            err_no_device = i["errs"]
            for ii in err_no_device:
                if ii["err_no"] == err_no:
                    err_info = ii["err_info"]
                    break

print(err_info)