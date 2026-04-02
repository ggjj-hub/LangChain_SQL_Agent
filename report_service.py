import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()


def generate_pdf(content, filename="Weekly_Report.pdf"):
    """支持中文的 PDF 生成函数"""
    pdf = FPDF()
    pdf.add_page()

    # 1. 注册中文字体 (确保 simhei.ttf 已经拷贝到项目目录下)
    # 如果你用的是微软雅黑，把下面改为 'msyh.ttc'
    try:
        pdf.add_font('SimHei', '', 'simhei.ttf')
        pdf.set_font('SimHei', size=12)
    except Exception as e:
        print(f"字体加载失败，请确认 simhei.ttf 是否在项目目录中: {e}")
        # 如果没字体，这里还是会报之前的错，所以一定要放字体文件！
        return None

    # 2. 写入内容
    # 注意：新版 fpdf2 默认支持 UTF-8，不需要再做复杂的 encode/decode
    pdf.multi_cell(0, 10, text=content)

    pdf.output(filename)
    return filename

def send_email(attachment_path, receiver_email):
    """通过 SMTP 发送带附件的邮件"""
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")  # 这里的密码通常是邮箱的“授权码”
    smtp_server = "smtp.qq.com"  # 以QQ邮箱为例，网易用 smtp.163.com
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "【自动生成】本周销售数据周报"

    msg.attach(MIMEText("您好，附件为您本周的销售汇总报告，请查收。", 'plain'))

    # 添加 PDF 附件
    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("📧 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")


# --- 主流程集成 ---
if __name__ == "__main__":
    # 假设这是 Agent 刚才生成的内容
    agent_output = "张三本周销售总额：23500.50元，完成订单3笔。主要任务：SQL Agent 环境搭建已完成。"

    print("📄 正在生成 PDF...")
    pdf_path = generate_pdf(agent_output)

    print("📤 正在发送邮件...")
    # 替换为你自己的测试邮箱
    send_email(pdf_path, "receiver@example.com")