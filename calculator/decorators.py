from django.shortcuts import redirect

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            # Usuário não está logado, redireciona para login (ou pode retornar erro)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper