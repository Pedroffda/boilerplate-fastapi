import typer
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from api.core.db_conection import get_db

from api.models.usuario import Usuario
from api.models.access_policy import AccessPolicy

app = typer.Typer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_administrador_user(email: str, password: str):
    """Cria usuário administrador e política de administradoristração"""
    db: Session = next(get_db())
    
    try:
        # Verifica se já existe administrador
        if db.query(Usuario).filter(Usuario.email == email).first():
            typer.echo("⚠️  Usuário administrador já existe!")
            return False

        # Cria política de admin
        admin_policy = AccessPolicy(
            nome="Administrador",
            actions=["*"],
            effect="ALLOW",
            resources=["*"],
        )
        db.add(admin_policy)
        db.commit()
        db.refresh(admin_policy)

        # Cria usuário admin
        admin_user = Usuario(
            nome="Administrador",
            email=email,
            senha=pwd_context.hash(password),
            id_politica=admin_policy.id,
        )
        db.add(admin_user)
        db.commit()

        typer.echo(f"✅ Usuário administrador criado com sucesso! Email: {email}")
        return True
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Erro ao criar administrador: {str(e)}")
        return False

@app.command()
def interactive():
    """Modo interativo para criar usuário administrador"""
    email = typer.prompt("Digite o email do administrador")
    password = typer.prompt("Digite a senha", hide_input=True, confirmation_prompt=True)
    
    if create_administrador_user(email, password):
        typer.echo("✅ Configuração de administrador concluída com sucesso!")
    else:
        typer.echo("❌ Falha ao configurar administrador", err=True)

@app.command()
def create(
    email: str = typer.Option(..., help="Email do usuário administrador"),
    password: str = typer.Option(..., help="Senha do administrador", hide_input=True)
):
    """Cria usuário administrador diretamente"""
    if create_administrador_user(email, password):
        typer.echo("✅ Configuração de administrador concluída com sucesso!")
    else:
        typer.echo("❌ Falha ao configurar administrador", err=True)

if __name__ == "__main__":
    app()