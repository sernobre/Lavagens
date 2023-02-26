@auth.requires_membership('administrador')
@auth.requires_login()
def manage() :

    edit_member = [lambda row: A('Editar Grupos',_href=URL("user","manage_membership",args=[row.id]))]

    form = SQLFORM.grid(db.auth_user,links_in_grid=True,links=edit_member)

    return locals()


@auth.requires_membership('administrador')
@auth.requires_login()
def manage_group() :



    form = SQLFORM.grid(db.auth_group)

    return locals()

@auth.requires_membership('administrador')
@auth.requires_login()
def manage_membership():
    isComputerAuth()
    user_id = request.args(0) 
    #or redirect(URL('manage'))
    #db.auth_membership.user_id.default = int(user_id)
    #db.auth_membership.user_id.writable = False
    
    #form = SQLFORM.grid(db.auth_membership.user_id == user_id)

    user_id = request.args(0) or redirect(URL('manage'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=False,
                       details=False,
                       selectable=False,
                       csv=False)

	
    return locals()



#user_post
@auth.requires_membership('administrador')
@auth.requires_login()
def users_post():
    isComputerAuth()
    form = SQLFORM.grid(db.user_post,onupdate=auth.archive)
    return locals()
