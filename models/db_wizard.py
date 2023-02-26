### we prepend t_ to tablenames and  to fieldnames for disambiguity
########################################


db.define_table('account_type',
    Field('name', type='string',
          label=T('Nome')),
     Field('description', type='string',
          label=T('Descrição')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)
 
db.define_table('account',
    Field('name', type='string',
          label=T('Nome')),
    Field('code', type='string',
          label=T('Codigo')),

    #Field('balance', type='float',writable=False,readable=True,default=0,
    #      label=T('Saldo')),
    #Field('pending', type='float',writable=False,readable=True,default=0,
    #      label=T('Pendente')),
    Field('account_type','reference account_type',
          label=T('Tipo Conta')),
  

    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)

#db.define_table('account_archive',db.account,Field('current_record','reference account',readable=False,writable=False))





db.define_table('post',
    Field('name', type='string',
          label=T('Nome')),
    Field('code', type='string',
          label=T('Codigo')),
     Field('account','reference account',
          label=T('Conta')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)

#db.define_table('post_archive',db.account,Field('current_record','reference post',readable=False,writable=False))



########################################
db.define_table('box',
  Field('name', type='string',
          label=T('Nome')),
    Field('post','reference post',writable=False,readable=False,
          label=T('Posto')),
    Field('counter_value', type='string',
          label=T('Valor do Contador')),
    Field('coin_value', type='decimal(10,2)',
          label=T('Valor da moeda')),
    Field('code', type='string',
          label=T('Codigo')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)

#db.define_table('box_archive',db.box,Field('current_record','reference box',readable=False,writable=False))

########################################
db.define_table('category',
    Field('name', type='string',
          label=T('Nome')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)


db.define_table('document_type',
    Field('name', type='string',
          label=T('Nome')),
     Field('description', type='string',
          label=T('Descrição')),
   Field('movement_type', type='list:string',
          label=T('Tipo')),
     Field('manual_available', type='boolean',
          label=T('Criação Manual')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)
db.document_type.movement_type.requires=IS_IN_SET(('DBT','CRD',"TRF"))


#db.define_table('category_archive',db.category,Field('current_record','reference category',readable=False,writable=False))

########################################
db.define_table('movement',
    #Field('from_agent','reference account',
    #      label=T('Conta de origem')),
    Field('m_date', type='date',readable=True,writable=False,
          label=T('Data')),

   Field('account1','reference account',writable=False,
          label=T('Conta')),

   Field('account2','reference account',writable=False,
          label=T('Conta 2')),

  Field('related_movement','reference movement',writable=False,
          label=T('Movimento Associado')),         
    
    
     Field('document_type','reference document_type',writable=False,
          label=T('Tipo Documento')),

    Field('credit', type='decimal(10,2)',writable=True,
          label=T('Valor Credito')),

    Field('debit', type='decimal(10,2)',writable=True,
          label=T('Valor Debito')),


Field('description','text',readable=True,writable=True,label='Descrição'),

auth.signature,format='%(id)s'
,migrate=settings.migrate)

#db.movement.total = Field.Virtual('total',lambda row: row.credit,label=T('Total'))



db.define_table('registration_by_post',

    Field('r_date', type='date',readable=True,writable=False,
          label=T('Data')),

    Field('post',db.post,writable=False,readable=True,
          label=T('Posto')),

Field('movement','reference movement',writable=False,readable=True,label=T('Movimento')),

Field.Virtual('credit' ,  lambda row: db.movement(row.registration_by_post.movement).credit ,label=T('Credito') ),
Field.Virtual('amount_subtract' ,  lambda row: db.movement(row.registration_by_post.movement).debit ,label=T('Debito') ),


Field.Virtual('amount_subtract_description' ,  lambda row: db.movement(row.registration_by_post.movement).description ,label=T('Diferenças Descrição') ),

Field.Virtual('total', lambda row: db.movement(row.registration_by_post.movement).credit- db.movement(row.registration_by_post.movement).debit ,label=T('Total') ),

  #  auth.signature,
    format='%(r_date)s -> %(post)s ',
   migrate=settings.migrate
  # migrate=True ,
  # fake_migrate=True
    )

 

#########################################

db.define_table('registration_line',
    
    Field('counter_value', type='string',
          label=T('Valor do contador')),
    
    Field('prev_counter_value', type='string',
          label=T('Valor do contador Anterior')),
    
    Field('t_box','reference box',writable=False,readable=True,
          label=T('Box')),

    Field('registration_by_post','reference registration_by_post',writable=False,readable=True,
          label=T('Registo')),

    Field('amount', type='decimal(10,2)',readable=True,writable=False,
          label=T('Valor')),

    Field.Virtual('name' ,  lambda row: db.box(row.registration_line.t_box  ).name ,label=T('Nome') ),

    Field.Virtual('coin_value' ,  lambda row: db.box(row.registration_line.t_box  ).coin_value ,label=T('Valor Moeda') ),
 

    auth.signature,
    format='%(counter_value)s',
   migrate=settings.migrate
   # migrate=True ,fake_migrate=True
    )


 
#db.define_table('registration_line_archive',db.registration_line,Field('current_record','reference registration_line',readable=False,writable=False))


 


db.define_table('user_post',
      Field('post','reference post',
          label=T('Posto')),
  Field('f_user','reference auth_user' ,
    label='Utilizador' ),
    auth.signature,
  #  format='%(counter_value)s',
    migrate=settings.migrate)


db.define_table('computer',
    
    Field('name', type='string',
          label=T('Nome Computador')),

    Field('cookie_key', type='string',
          label=T('Chave')),  

 Field('user_agent', type='string',
          label=T('User Agent')),  


    auth.signature,
    format='%(computer_name)s',
    migrate=settings.migrate)
