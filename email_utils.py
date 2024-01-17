# email_utils.py
import smtplib
from email.mime.text import MIMEText

def send_confirmation_email(email, name):
    sender_email = "seuemail@gmail.com"  # Substitua pelo seu e-mail
    sender_password = "sua_senha"  # Substitua pela sua senha
    msg = MIMEText(f"Olá {name}, seu cadastro foi concluído com sucesso!")
    msg['Subject'] = "Confirmação de Cadastro"
    msg['From'] = sender_email
    msg['To'] = email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
