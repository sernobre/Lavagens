# -*- coding: utf-8 -*-
### required - do no delete

### end requires
@auth.requires(auth.has_membership('administrador') or auth.has_membership('escritorio') )
def index():
    isComputerAuth()
    return dict()

def error():
    return dict()

@auth.requires_login()
@auth.requires(auth.has_membership('administrador') or auth.has_membership('escritorio') )
def manage():
    isComputerAuth()

    links = [lambda row: A('Boxes',_href=URL("default","add_box2post",args=[row.id]))]

    #grid = SQLFORM.grid(db.registration_by_post,fields=( db.registration_by_post.id, db.registration_by_post.date, db.registration_by_post.post, db.registration_by_post.total,  db.registration_by_post.amount_subtract  , db.registration_by_post.total , db.registration_by_post.account_balance ) , deletable=False,  editable=False,   details=False,create=False,links_in_grid=True,links=links)

    form = SQLFORM.grid(db.post, fields=( db.post.id ,db.post.code ,db.post.name  )    ,deletable=True,  editable=True,   details=False,create=False,links_in_grid=True,links=links)
    

    return locals()
