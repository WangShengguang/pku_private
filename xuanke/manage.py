from xuanke import Xuanke

if __name__ == "__main__":
    # with open(os.path.join(cur_dir, "补选退选.html"), "r", encoding="utf-8") as f:
    #     content = f.read()
    # Task("", "", "", "", True).parse_content(content)
    username = "用户名"
    password = "密码"
    listening_course = ["机器学习", "自然语言处理", "操作系统高级课程"]  # "机器学习", "自然语言处理",
    page_fresh_frequency = 5 * 60  # 刷新间隔，单位s
    course_fresh_frequency = 1 * 60  # 刷新间隔，单位s
    wechat_info = False  # 是否启用微信通知
    info_person = False  # 是否通知个人
    auto_select = True  # 有空缺自动选课
    parm = {"username": username, "password": password,
            "listening_course": listening_course,
            "page_fresh_frequency": page_fresh_frequency,
            "course_fresh_frequency": course_fresh_frequency,
            "wechat_info": wechat_info, "info_person": info_person,
            "auto_select": auto_select}
    xuanke = Xuanke(**parm)
    xuanke.run()
