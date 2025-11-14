import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt6.QtWidgets import QMessageBox

def enviar_email_gmail_com_cc(sender_email, sender_password, recipient_email, cc_emails, subject, body):
    """
    Envia um e-mail usando o SMTP do Gmail com Senha de App e suporte a CC.

    :param sender_email: O e-mail do remetente (ex: "ceimbratech@gmail.com")
    :param sender_password: A "Senha de App" de 16 dígitos gerada pelo Google
    :param recipient_email: O e-mail do destinatário principal
    :param cc_emails: Uma lista de e-mails para enviar em cópia (CC)
    :param subject: O assunto do e-mail
    :param body: O corpo do e-mail (texto plano)
    """
    try:
        # Cria a mensagem
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        
        # Adiciona os e-mails em CC
        if cc_emails:
            # Filtra e-mails vazios da lista, se houver
            valid_cc_emails = [email.strip() for email in cc_emails if email and email.strip()]
            if valid_cc_emails:
                message["Cc"] = ", ".join(valid_cc_emails)
        
        # Adiciona o corpo do e-mail
        message.attach(MIMEText(body, "plain"))

        # Configura a conexão com o servidor SMTP do Gmail
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            
            # Prepara a lista final de destinatários (Para + CC)
            all_recipients = [recipient_email] + (valid_cc_emails if 'valid_cc_emails' in locals() else [])
            
            # Envia o e-mail
            server.sendmail(
                sender_email, all_recipients, message.as_string()
            )
            
        print(f"E-mail enviado com sucesso para {recipient_email} (CC: {cc_emails})")
        QMessageBox.information(
            None, 
            "E-mail Enviado", 
            f"O e-mail foi enviado com sucesso para:\n{recipient_email}"
        )

    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação. Verifique seu e-mail ou Senha de App.")
        QMessageBox.critical(
            None, 
            "Erro de Autenticação", 
            "Falha ao enviar e-mail. Verifique se o 'E-mail do Remetente' e a 'Senha de App' estão corretos nas Configurações."
        )
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        QMessageBox.critical(
            None, 
            "Erro no Envio", 
            f"Ocorreu um erro inesperado ao enviar o e-mail:\n{e}"
        )
