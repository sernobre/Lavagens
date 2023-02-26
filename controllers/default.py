# -*- coding: utf-8 -*-
### required - do no delete


if 0:
    from gluon.globals import *
    from gluon.html import *
    from gluon.http import *
    from gluon.sqlhtml import SQLFORM, SQLTABLE, form_factory
    session = Session()
    request = Request()
    response = Response()


def user(): 

    return dict(form=auth())



def download(): return response.download(request,db)
def call(): return service()
### end requires






@auth.requires_login()
def index():


    isComputerAuth()

    postos_ids =  db(db.user_post.f_user == auth.user_id).select(  )

    postos = []

    for pid in postos_ids :
      posto =  db.post(pid.post)
      postos.append(posto)

 

    return locals()

@auth.requires_login()
def edit_last_register():

    isComputerAuth()

    postId = request.args(0)
    
    if postId == None :
        session.flash = 'O posto é inválido'
        redirect(URL('default','view_registration'))
    

    posto =  db.box( db.post.id ==   postId)
    

    last_registo = db(db.registration_by_post.post ==  postId ).select( orderby =~ db.registration_by_post.id).first()
    
    '''
    last_registo = None

    if len(registos) > 0 :
        last_registo  = registos[-1]
    '''


    boxes = db(db.registration_line.registration_by_post  == last_registo.id).select()

    return locals()


@auth.requires_login()
def box_register():

    isComputerAuth()

    postId = request.args(0)

    posto =  db.box( db.post.id ==   postId)

    boxes = db(db.box.post == postId).select()

    registos = db(db.registration_by_post.post ==  postId ).select( orderby =db.registration_by_post.id)

    last_registo = None

    if len(registos) > 0 :
        last_registo  = registos[-1]

    

    return locals()

@auth.requires_login()
@auth.requires(auth.has_membership('administrador') or auth.has_membership('escritorio') )
def view_registration_json():

    isComputerAuth()

     
    registos = db(db.registration_by_post).select(    orderby =db.registration_by_post.id)

    last_registo = None

    if len(registos) > 0 :
        last_registo  = registos[-1]


    postos_ids =  db(db.user_post.f_user == auth.user_id).select(  )

    postos = []


    for pid in postos_ids :
      posto =  db.post(pid.post)
      postos.append(posto)

  
    links = [lambda row: A('Detalhes',_href=URL("default","view_registration_details",args=[row.id]))]

    '''
    grid = SQLFORM.grid(db.registration_by_post,fields=( db.registration_by_post.id, db.registration_by_post.r_date, db.registration_by_post.post ,  db.registration_by_post.credit, db.registration_by_post.amount_subtract,  db.registration_by_post.total ) , deletable=False,  editable=False,   details=False,create=False,links_in_grid=True,links=links)
    '''
    
    
    
    #grid = SQLFORM.grid(db.registration_by_post,fields=( db.registration_by_post.r_date))
    #db(db.user_post.f_user == auth.user_id).select(  )    
    
    return response.json(  db(db.registration_by_post).select()  )

def view_registration():

    isComputerAuth()

     
    registos = db(db.registration_by_post).select(    orderby =db.registration_by_post.id)

    last_registo = None

    if len(registos) > 0 :
        last_registo  = registos[-1]


    postos_ids =  db(db.user_post.f_user == auth.user_id).select(  )

    postos = []

    
    for pid in postos_ids :
      posto =  db.post(pid.post)
      postos.append(posto)
      
    from datetime import timedelta
    import datetime 

    #Mostra só os resultados dos ultimos 90 dias 
    startdate =  datetime.date.today()-timedelta(days=90)
    
    # (db.movement.m_date  >=  startdate) 
  
    #links = [lambda row: A('Detalhes',_href=URL("default","view_registration_details",args=[row.id]))]
    
    #registos = db(db.registration_by_post.r_date > startdate ).select(
    #                                              orderby=~db.registration_by_post.r_date)
    
    registos = db(db.registration_by_post).select(
                                                  orderby=~db.registration_by_post.r_date)    
    #limitby=(0,500))
    
    
    for r in registos :
        r.post_name = db.post(r.post).name
        
        
    
    
    
    return locals()



@auth.requires_login()
def view_registration_details():

    isComputerAuth()

    registration_by_post_id = request.args(0)

    #registration_by_post = db(db.registration_by_post.id  == registration_by_post_id  ).select()
    
    registration_by_post = db.registration_by_post(registration_by_post_id )

    registos = db(db.registration_line.registration_by_post == registration_by_post_id  ).select()


    tipos_registos = db(db.registration_by_post.post ==  registration_by_post.post ).select( orderby =db.registration_by_post.id)

    '''
    last_registo = None

    if len(registos) > 0 :
        last_registo  = registos[-1]

    is_the_last = last_registo.id == registration_by_post_id
    '''

    #grid = SQLFORM.grid(db.registration_line,fields=( db.registration_line.box,   , db.registration_line.registration_by_post , db.registration_line.amount ) , deletable=False,  editable=False,   details=False,create=False )

    #grid = SQLFORM.grid( db.registration_line.registration_by_post == registration_by_post_id  )

    movement = db.movement( registration_by_post.movement ) 

    form_movement = SQLFORM( db.movement , movement , readonly=True   ) 


    return locals()





@auth.requires_login()
def editRecord():


    import gluon.contrib.simplejson

    boxes = request.vars.boxes

    date = request.vars.date
    total = request.vars.total
    postId = request.vars.postId
    diffe = request.vars.diferencas
    difdesc = request.vars.diferencas_desc
    last_registo_id =  request.vars.last_registo_id

    #db( (db.registration_by_post.r_date == date) &  (db.registration_by_post.post == postId) ).count()

    last_registo =  db.registration_by_post( db.registration_by_post.id ==   last_registo_id)

    movement = db.movement( db.movement.id ==   last_registo.movement)

    new_value = float(total) - float(diffe)

    movement.update_record(
        credit =  total,
        debit = float(diffe),
        # total = new_value,
         description = difdesc


    );


    boxes_obj = gluon.contrib.simplejson.loads(boxes)


    # Se acontcer erro isto não vai apagar
    #db(db.registration_line.registration_by_post == last_registo.id).delete()



    for box_obj in boxes_obj :

        line2update = db.registration_line(  db.registration_line.id  ==  box_obj['id']  )


        diferencas =  float(box_obj['counter_value']) -  float( box_obj['prev_counter_value'])

        line2update.update_record( counter_value =     box_obj['counter_value'] ,  amount =  diferencas * box_obj['coin_value'] )

        #db.registration_line.insert(   prev_counter_value =    box_obj['prev_counter_value'] ,    counter_value =     box_obj['counter_value'] , t_box =   box_obj['id'] , amount =  diferencas * box_obj['coin_value'] , registration_by_post = last_registo_id )

        box_update = db.box( db.box.id ==     line2update.t_box )
        box_update.update_record( counter_value = box_obj['counter_value']  )


    '''
   for box_obj in boxes_obj :

        diferencas =  float(box_obj['counter_value_new']) -  float( box_obj['counter_value'])

        db.registration_line.insert(   prev_counter_value =    box_obj['counter_value'] ,    counter_value =     box_obj['counter_value_new'] , t_box =   box_obj['id'] , amount =  diferencas * box_obj['coin_value'] , registration_by_post = rpost_id )

        box_update = db.box( db.box.id ==   int(box_obj['id']) )
        box_update.update_record( counter_value = box_obj['counter_value_new']  )
    '''

    return  "OK"



@auth.requires_login()
def saveRecord():

    import gluon.contrib.simplejson

    #if request.vars.boxes != None :
    #   boxes = gluon.contrib.simplejson.loads(request.vars.boxes)
    
    boxes = request.vars.boxes

    date = request.vars.date
    total = request.vars.total
    postId = request.vars.postId
    diffe = request.vars.diferencas
    difdesc = request.vars.diferencas_desc



    # ver se já existe um registo
    num_registos = db( (db.registration_by_post.r_date == date) &  (db.registration_by_post.post == postId) ).count()

    if(num_registos > 0) :
        return "Já existe um registo criado para este dia "

    records_after = db( (db.registration_by_post.r_date >= date) &  (db.registration_by_post.post == postId) ).count()

    if(records_after > 0) :    
        return "Existem registos com data posterior a: " + str(date)

    '''
    primeiro temos que criar um registo do tipo registration_by_post e depois as linhas do mesmo
    '''


    posto =  db.box( db.post.id ==   postId)
    
    


    new_value = float(total) - float(diffe)

     

    if(  posto.account == None ) :    
        return "O posto não tem nenhuma conta associada"



    movimentoId = db.movement.insert( 
        account1 = posto.account,
        document_type =  1,
        credit =  total,
        debit = float(diffe),
        #total = new_value,
        m_date = date, 
        description = difdesc
        );
    

    rpost_id = db.registration_by_post.insert(  
        post = postId   , 
        r_date = date   ,
        movement = movimentoId,
          
        )
    

    if rpost_id == None :
        return "Não foi possivel gravar o registo"


    diferencas = 0

    box_id = -1
    

    
    boxes_obj = gluon.contrib.simplejson.loads(boxes)
    
    for box_obj in boxes_obj :

        diferencas =  float(box_obj['counter_value_new']) -  float( box_obj['counter_value'])
        
        db.registration_line.insert(   prev_counter_value =    box_obj['counter_value'] ,    counter_value =     box_obj['counter_value_new'] , t_box =   box_obj['id'] , amount =  diferencas * box_obj['coin_value'] , registration_by_post = rpost_id )
        
        box_update = db.box( db.box.id ==   int(box_obj['id']) )
        box_update.update_record( counter_value = box_obj['counter_value_new']  )
        


    return  "OK"

@auth.requires_login()
def get_balance():



    balance = db(db.movement).select( orderby =db.movement.id).last()

    if balance == None or balance['balance'] == None :
        return 0

    return balance['balance']


@auth.requires_login()
@service.json
def getBoxes():

    postId = request.args(0)

    boxes = db(db.box.post == postId).select()
    #postos = "teste"

    return response.json(boxes)

@auth.requires_login()
def error():
    return dict()





@auth.requires_login()
def sqlform_on_delete_account(id_account):


    print("Error")

    if( db(db.movement.account1 == id_account).count()  > 0 ) :
        print("Error")
        return False



    return True





@auth.requires_login()
def box_manage():
    isComputerAuth()
    form = SQLFORM.grid(db.box,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def registration_manage():
    isComputerAuth()
    form = SQLFORM.grid(db.registration_line,onupdate=auth.archive)
    return locals()




@auth.requires_login()
def edit_box():
    isComputerAuth()

    box_id = request.args(0)

    form = SQLFORM(db.box,box_id,readonly=False,deletable=True)

    postId =  db.box( db.box.id ==   box_id).post

    if form.process().accepted:

        session.flash = 'form accepted'
        redirect(URL('add_box2post/' + str(postId) ))
    elif form.errors:
        response.flash = 'form has errors'


    return locals()

@auth.requires_login()
def add_box2post():
    isComputerAuth()
    postId = request.args(0)

    post =  db.box( db.post.id ==   postId)
 

    #form = SQLFORM(db.box,postId,readonly=False)

    form = SQLFORM(db.box)
    form.vars.post = postId

    boxes = db(db.box.post == postId   ).select( )

    if form.process().accepted:

        session.flash = 'form accepted'
        redirect(URL('add_box2post/' + str(postId) ))
    elif form.errors:
        response.flash = 'form has errors'
    #else:
    #   response.flash = 'please fill the form'
 
    return locals()

def error():


     return locals()
