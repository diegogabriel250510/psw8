from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.admin.views.decorators import staff_member_required
from exames.models import SolicitacaoExame
from django.http import FileResponse
from django.contrib import messages
from django.contrib.messages import constants
from .utils import gerar_pdf_exames, gerar_senha_aleatoria
# Create your views here.
@staff_member_required
def gerenciar_clientes(request):
    clientes = User.objects.filter(is_staff=False)
    
    nome_completo = request.GET.get('nome')
    email = request.GET.get('email')
    if email:
        clientes = clientes.filter(email__contains = email)
    if nome_completo:
        clientes = clientes.annotate(full_name = Concat('first_name',Value(' '), 'last_name')).filter(full_name__contains =nome_completo)
    return render(request, 'gerenciar_clientes.html',{'clientes':clientes})
@staff_member_required 
def cliente(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)
    return render(request, 'cliente.html', {'cliente': cliente, 'exames': exames})
@staff_member_required
def exame_cliente(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    print(exame)
    return render(request, 'exame_cliente.html', {'exame':exame})
def proxy_pdf(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    
    response = exame.resultado.open()

    return FileResponse(response)
def gerar_senha(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    if exame.senha:
        return FileResponse(gerar_pdf_exames(exame.exame.nome,exame.usuario.first_name,exame.senha), filename="token_pdf")
    exame.senha = gerar_senha_aleatoria(9)
    exame.save()
    return FileResponse(gerar_pdf_exames(exame.exame.nome,exame.usuario.first_name,exame.senha), filename="token_pdf")
def alterar_dados_exames(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    pdf = request.FILES.get('resultados')
    status = request.POST.get('status')
    requer_senha = request.POST.get('requer_senha')
    exame.requer_senha = True if requer_senha else False
    if requer_senha and (not exame.senha):
        messages.add_message(request, constants.ERROR, 'para exigir a senha, primeiro crie uma')
        return redirect(f'/empresarial/exame_cliente/{exame_id}')
    if pdf:
        exame.resultado = pdf
    exame.status = status
    exame.save()
    messages.add_message(request, constants.SUCCESS, 'dados alterados com sucesso')
    return redirect(f'/empresarial/exame_cliente/{exame_id}')