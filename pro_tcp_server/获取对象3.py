DEVICE_LIST_INFO = {}
DEVICE_LIST_INFO["device_list_info"] = {"command": "device",
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

# 将得到的列表信息整理成该格式:[{'device_01': [{0: '成功'}, {1: '失败'}]}, {'device_02': [{3: '成功'}, {4: '失败'}]}]
errors_list = DEVICE_LIST_INFO["device_list_info"]["response"]["errors"]
# print(errors_list)
# final_dict={}
# final_dict_list=[]
# for i in errors_list:
#     print(i["device_name"])
#     err_list=i["errs"]
#     print(err_list)
#     list2=[]
#     for ii in err_list:
#         dict4={}
#         dict4[ii["err_no"]]=ii["err_info"]
#         print(dict4)
#         list2.append(dict4)
#     final_dict={}
#     final_dict[i["device_name"]]=list2
#     print(final_dict)
#
#     final_dict_list.append(final_dict)
# print(final_dict_list)

# 通过得到的device和err_no 得到err_info
# dev="device_02 "
# err_no=3










