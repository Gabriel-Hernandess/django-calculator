from django.shortcuts import redirect
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')

        # Se não está logado, manda para login
        if not usuario_id:
            return redirect('login')

        # Senão, executa a view normalmente
        return view_func(request, *args, **kwargs)

    return wrapper