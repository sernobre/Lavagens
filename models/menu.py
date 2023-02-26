response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Inicio'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Postos'),URL('post','post_manage')==URL(),URL('post','post_manage'),[]),
(T('Box'),URL('default','box_manage')==URL(),URL('default','box_manage'),[]),
(T('Contas'),URL('account','manage')==URL(),URL('account','manage'),[]),
(T('Registos Diários'),URL('default','registration_manage')==URL(),URL('default','registration_manage'),[]),
(T('Movimentos'),URL('movement','manage')==URL(),URL('movement','manage'),[]),
(T('Configurações'),URL('config','index')==URL(),URL('config','index'),[]),
#(T('Utilizadores'),URL('default','list_users')==URL(),URL('default','list_users'),[]),
#(T('Utilizadores por posto'),URL('default','users_post')==URL(),URL('default','users_post'),[]),
#(T('Utilizadores por posto'),URL('default','users_post')==URL(),URL('default','users_post'),[])

]
