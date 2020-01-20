payload = {"command": "device",
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
# 将格式整理成
# {"device_01": {"0": "成功", "1": "失败"},"device_02": {"3": "第一失败", "4": "第二失败"}}
errors_list = payload["response"]["errors"]
# print(errors_list)
device_info_dict = {}
for i in errors_list:
    dev_name = i["device_name"]
    err_list = i["errs"]
    # print(err_list)
    dict2 = {}
    for ii in err_list:
        err_no = ii["err_no"]
        err_info = ii["err_info"]
        # print(err_no, err_info)
        dict2[err_no] = err_info
        # print(dict2)
    device_info_dict[dev_name] = dict2
print(device_info_dict)
