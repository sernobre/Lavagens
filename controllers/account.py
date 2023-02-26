@auth.requires_login()
@auth.requires(auth.has_membership('administrador') or auth.has_membership('escritorio') )
def manage():
    isComputerAuth()
    links = [lambda row: A('Delete',_href=URL("default","delete_account",args=[row.id]))] 
 
    
    form = SQLFORM.grid(db.account,deletable=sqlform_on_delete_account,create=False)



    
    return locals()


@auth.requires_login()
@auth.requires(auth.has_membership('administrador') or auth.has_membership('escritorio') )
def sqlform_on_delete_account(id_account):

    isComputerAuth()
    #print "Error"

    if( db(db.movement.account1 == id_account).count()  > 0 ) :
        print "Error"
        return False



    return True

@auth.requires_login()
@auth.requires(auth.has_membership('administrador') or auth.has_membership('escritorio') )
def add():

    isComputerAuth()

    form = SQLFORM(db.account)

    if form.process().accepted:

		 

		if form.vars.account_type == '1' :

			postid = db.post.insert( 
				name = form.vars.name,
				code = form.vars.code,
				account = form.vars.id
				)

			db.user_post.insert( 
				post = 	postid,
				f_user =  auth.user.id
				)


			
			response.flash = 'Registo inserido com sucesso'


    return locals()
