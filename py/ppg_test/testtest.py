# new_inflct_points = [4, 34, 35, 45, 73, 74, 75, 76, 77, 78, 79, 84, 98, 113, 123, 153, 163, 192, 193, 203, 231, 232, 243, 273, 284, 285]
# diff_ifp = [30,  1, 10, 28,  1, 1, 1, 1, 1, 1, 5, 14, 15, 10, 30, 10, 29, 1, 10, 28, 1, 11, 30, 11, 1]
#
# ifp_d = 20
# diastolic_points = []
#
# def prints():
#     print("new_inflct_points")
#     print(len(new_inflct_points))
#     print(new_inflct_points)
#
#     print("diff_ifp")
#     print(len(diff_ifp))
#     print(diff_ifp)
#
#     print("diastolic_points")
#     print(len(diastolic_points))
#     print(diastolic_points)
#
#
# prints()
#
# # not empty
# if len(diff_ifp) > 0:
#
#     # add ung first element kung okay naman ung unang difference
#     first_diff = diff_ifp[0]
#     if first_diff >= ifp_d:
#         diastolic_points.append(new_inflct_points[0])
#
#     # remove first element para pantay
#     new_inflct_points.pop(0)
#
#     print("\n============================NEW NEW NEW============================\n")
#     prints()
#
#     # ensure same length
#     try:
#         if len(new_inflct_points) != len(diff_ifp):
#             raise IndexError("Inflection Point Removal: Different Lengths, There is a problem")
#     except IndexError as e:
#         print("Caught Exception: " + repr(e))
#
#     for i, d in enumerate(diff_ifp):
#         # eto ung sa distance mula sa katabi
#         if d >= ifp_d:
#             diastolic_points.append(new_inflct_points[i])
#
#         # eto ung distance mula sa last diastolic point
#         elif abs(new_inflct_points[i] - diastolic_points[-1]) >= ifp_d:
#             diastolic_points.append(new_inflct_points[i])
#
#     print(diastolic_points)
#
#
#
# # [4, 34, 35, 45, 73, 74, 75, 76, 77, 78, 79, 84, 98, 113, 123, 153, 163, 192, 193, 203, 231, 232, 243, 273, 284, 285]
# #    [30,  1, 10, 28,  1,  1,  1,  1,  1,  1,  5, 14,  15,  10,  30,  10,  29,   1,  10,  28,   1,  11,  30,  11,   1]
# # [4, 34, 73, 153, 192, 231, 273]
#
# # eto ung luma
# skip = False
# j = 0
# for i in range(len(new_inflct_points) - 1):
#     if skip: i = j; skip = False; continue
#     diastolic_points.append(new_inflct_points[i])
#     j = i
#     while abs(new_inflct_points[i + 1] - new_inflct_points[i]) < ifp_d:
#         skip = True
#         j += 1
#
# # para masama ung last peak. kung hindi sya iniskip due to margin
# if not skip:
#     diastolic_points.append(new_inflct_points[-1])
#
#

x = [1,2,3,4,5,6,7,8,9]
print(x)
x.pop(0); print(x)
x.pop(0); print(x)
x.pop(0); print(x)


print('sadsadasdsa')
i = 2
while i > 0:
    x.pop(0)
    print(i, " | ", x)
    i -= 1
