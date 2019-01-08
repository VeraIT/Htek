import time

from phone import Phone
import functions as fun
import configuration as con

print("测试开始")
#创建2个话机 A和B
A = Phone(con.info_a)
B = Phone(con.info_b)
# A向服务器注册并检查状态
fun.phone_register(A)
fun.check_register_state(A)
# B向服务器注册并检查状态
fun.phone_register(B)
fun.check_register_state(B)
#话机A呼叫话机B
fun.A_call_B(A, B)