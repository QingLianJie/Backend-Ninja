AUTH_VERIFY_CODE_EXPIRE_SECONDS = 60 * 10  # 验证码过期时间（秒）
AUTH_VERIFY_CODE_LENGTH = 6  # 验证码位数
AUTH_RESET_PASSWORD_EMAIL_TITLE = "清廉街密码重置"
AUTH_RESET_PASSWORD_EMAIL_BODY = """您的验证码为: {0}
收到这封邮件是因为有人请求重置你在清廉街账户 {1} 的密码，如果非本人操作请忽略这封邮件。

Best Regards,
qinglianjie.cn
"""