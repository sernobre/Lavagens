

@auth.requires_login()
def index():
    isComputerAuth()
	links = [lambda row: TAG.a('+ Registo', _class="btn", _href=URL('registo', vars=dict(id=row.id)))]

	form = SQLFORM.grid(db.box,deletable=False,editable=False, links = links)



	return locals()

@auth.requires_login()
def registo():
    isComputerAuth()
    #post_id = request.args(0)
    post_id = request.vars.id


    form=SQLFORM(db.registration_line)


    #return locals()

    if form.process().accepted:
    	form.vars.box = 2
        session.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

