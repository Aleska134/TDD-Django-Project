from libgravatar import Gravatar

def create_avatar(email_address):
    g = Gravatar(email_address)
    
    return g.get_image(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')
    