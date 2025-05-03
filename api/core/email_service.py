from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.core.settings import Settings

class EmailService:
    def __init__(self):
        self.settings = Settings()
    
    def send_password_reset_email(self, email: str, token: str) -> bool:
        reset_link = f"{self.settings.FRONTEND_URL}/reset-password?token={token}"
        
        msg = MIMEMultipart()
        msg["From"] = f"Suporte {self.settings.SMTP_USER} <{self.settings.SMTP_USER}>"
        msg["To"] = email
        msg["Subject"] = f"Redefinição de senha - {self.settings.SMTP_USER}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2563eb;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    padding: 25px;
                    background-color: #f9fafb;
                    border-radius: 0 0 8px 8px;
                    border: 1px solid #e5e7eb;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background-color: #2563eb;
                    color: white !important;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 15px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #6b7280;
                    text-align: center;
                }}
                .code {{
                    font-family: monospace;
                    background-color: #f3f4f6;
                    padding: 2px 4px;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Redefina sua senha</h1>
            </div>
            
            <div class="content">
                <p>Olá,</p>
                <p>Recebemos uma solicitação para redefinir a senha da sua conta. Clique no botão abaixo para continuar:</p>
                
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Redefinir Senha</a>
                </p>
                
                <p>Se você não solicitou esta alteração, por favor ignore este e-mail.</p>
                <p>O link de redefinição expirará em <strong>1 hora</strong>.</p>
                
                <div class="footer">
                    <p>Caso o botão não funcione, copie e cole este link no seu navegador:</p>
                    <p><small>{reset_link}</small></p>
                    <p>© {datetime.now().year} {self.settings.SMTP_USER}. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, "html"))
        
        try:
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                server.starttls()
                server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False