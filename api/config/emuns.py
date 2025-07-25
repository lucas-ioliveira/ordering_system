from enum import Enum


class UserErrorMessages(str, Enum):
    USER_NOT_FOUND = 'Usuário não encontrado!'
    USER_NOT_FOUND_OR_CREDENTIALS_INVALID = 'Usuário não encontrado ou credenciais incorretas!'
    EMAIL_ALREADY_REGISTERED = 'E-mail já cadastrado!'
    USER_NOT_AUTHENTICATED = 'Usuário não autenticado!'
    USER_INVALID_TOKEN = 'Token inválido!'
    USER_NOT_ACTIVE = 'Usuário inativo!'
    USER_NOT_ADMIN = 'Usuário não admin!'
    USER_NOT_AUTHORIZED = 'Usuário não autorizado!'
    USER_NOT_CREATED = 'Erro ao criar usuário!'


class OrderErrorMessages(str, Enum):
    ORDER_NOT_FOUND = 'Pedido não encontrado!'
    ORDER_NOT_CREATED = 'Erro ao criar pedido!'
    ORDER_NOT_UPDATED = 'Erro ao atualizar pedido!'
    ORDER_NOT_DELETED = 'Erro ao deletar pedido!'
    ORDER_NOT_CANCELLED = 'Erro ao cancelar pedido!'
    ORDER_ALREADY_CANCELLED = 'Pedido já cancelado!'