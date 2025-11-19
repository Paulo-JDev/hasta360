import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt6.QtWidgets import QMessageBox

def enviar_email_gmail_com_cc(sender_email, sender_password, recipient_email, cc_emails, subject, body):
    """
    Envia e-mail usando SMTP com STARTTLS (Porta 587).
    Esta abordagem é menos bloqueada por antivírus do que SMTP_SSL direto.
    """
    try:
        # Configuração da mensagem
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Tratamento dos CCs
        valid_cc_emails = []
        if cc_emails:
            # Limpa e valida a lista de CCs
            valid_cc_emails = [email.strip() for email in cc_emails if email and email.strip()]
            if valid_cc_emails:
                msg['Cc'] = ", ".join(valid_cc_emails)

        # Corpo do e-mail
        msg.attach(MIMEText(body, 'plain'))

        # Lista final de destinatários (Para + CCs)
        all_recipients = [recipient_email] + valid_cc_emails

        # --- MUDANÇA CRUCIAL AQUI ---
        # Usamos a porta 587 e starttls(), igual ao seu código que funciona.
        # Isso é mais "amigável" para o Windows Defender.
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() # Criptografa a conexão após o início
            server.login(sender_email, sender_password)
            server.send_message(msg, to_addrs=all_recipients)
        
        print(f"E-mail enviado com sucesso para {recipient_email} (CC: {valid_cc_emails})")
        QMessageBox.information(
            None, 
            "E-mail Enviado", 
            f"O e-mail foi enviado com sucesso para:\n{recipient_email}"
        )

    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação.")
        QMessageBox.critical(
            None, 
            "Erro de Autenticação", 
            "Falha ao login no Gmail.\nVerifique se o e-mail e a Senha de App estão corretos nas Configurações."
        )
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        QMessageBox.critical(
            None, 
            "Erro no Envio", 
            f"Ocorreu um erro ao enviar o e-mail:\n{str(e)}"
        )
