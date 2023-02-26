@auth.requires_membership('administrador')
@auth.requires_login()
def index():

    isComputerAuth()

    return dict()



#def entity_type_manage():
#    form = SQLFORM.smartgrid(db.t_entity_type,onupdate=auth.archive)
#    return locals()
@auth.requires_membership('administrador')
@auth.requires_login()
def account_manage():
    isComputerAuth()
    form = SQLFORM.grid(db.account_type,onupdate=auth.archive,deletable=False)
    return locals()

@auth.requires_membership('administrador')
@auth.requires_login()
def doc_manage():
    isComputerAuth()
    

    form = SQLFORM.grid(db.document_type,onupdate=auth.archive,deletable = sqlform_check_if_doc_can_be_deleted)
    return locals()

@auth.requires_login()
def sqlform_check_if_doc_can_be_deleted(id_account):
 

    if( db(db.movement.document_type == id_account).count()  > 0 ) :
        #print "Error"
        return False



    return True



@auth.requires_membership('administrador')
@auth.requires_login()
def auth_computer():
    isComputerAuth()
    isAuth = ''

    agent = request.env.http_user_agent

    if request.cookies.has_key('lav_session'):
        isAuth = request.cookies['lav_session'].value

    '''        
            response.cookies['lav_session'] = str( 1 + int(value)) #Shouldn't this update the cookie on the clients side?
        else: 
            cookieCreate()
	'''
	
    form = SQLFORM.grid(db.computer,create=False)

	#isAuth = 'teste'
    return locals()

@auth.requires_membership('administrador')
@auth.requires_login()
def add_computer():

    from hashlib import sha1
    import hmac
    import binascii

    isComputerAuth()

    agent = request.env.http_user_agent



    hash_key = calculate_hash(agent)



    return locals()

@auth.requires_membership('administrador')
@auth.requires_login()
def saveComputer():


    name = request.vars.name
    key = request.vars.key
    agent = request.vars.agent
    
    response.cookies['lav_session'] = key
    response.cookies['lav_session']['expires'] = 24 * 3600 * 354 * 10
    response.cookies['lav_session']['path'] = '/'

    cid = db.computer.insert(
        name = name,
        cookie_key = key,
        user_agent = agent
        );



    return "OK"


def test():


    test = False

    # auth.groups():

    for g in  auth.user_groups :

        if g == 2 :
            return True


    #test = auth.groups()


    return test
