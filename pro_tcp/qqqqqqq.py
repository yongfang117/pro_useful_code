# HOST_ADDRESS = '127.0.0.1'
# PORT_SPURT_CODE = 5000
# PORT_CUT_FEET = 5001
# PORT_AOI = 5002
# PORT_CLAMP = 5003
# PORT_FCT = 5004
# PORT_OFFLINE = 5005
# PORT_FCT_TEST_1 = 5006
# PORT_FCT_TEST_2 = 5007
# PORT_FCT_TEST_3 = 5008
# ADDRS = (
#     (HOST_ADDRESS, PORT_SPURT_CODE),
#     (HOST_ADDRESS, PORT_CUT_FEET),
#     (HOST_ADDRESS, PORT_AOI),
#     (HOST_ADDRESS, PORT_CLAMP),
#     (HOST_ADDRESS, PORT_FCT),
#     (HOST_ADDRESS, PORT_OFFLINE),
#     (HOST_ADDRESS, PORT_FCT_TEST_1),
#     (HOST_ADDRESS, PORT_FCT_TEST_2),
#     (HOST_ADDRESS, PORT_FCT_TEST_3),
# )
# print(ADDRS)

ADDRS = (('127.0.0.1', 5000), ('127.0.0.1', 5001), ('127.0.0.1', 5002), ('127.0.0.1', 5003), ('127.0.0.1', 5004),
         ('127.0.0.1', 5005), ('127.0.0.1', 5006), ('127.0.0.1', 5007), ('127.0.0.1', 5008))

# HDLRS = (
# #     SpurtCodeHandler,
# #     CutFeetHandler,
# #     AOIHandler,
# #     ClampHandler,
# #     FCTHandler,
# #     OfflineHandler,
# #     FCTTest1Handler,
# #     FCTTest2Handler,
# #     FCTTest3Handler
# # )

HDLRS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
print(list(zip(ADDRS, HDLRS)))
print(type(list(zip(ADDRS, HDLRS))))

addr_hdlr = lambda: tuple(zip(ADDRS, HDLRS))

print(addr_hdlr)
